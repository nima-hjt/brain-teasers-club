// Local stand-in for the Firebase Realtime Database REST + streaming API, for testing Live Match offline.
// Run: node tools/mockdb.js  (listens on 127.0.0.1:9200), then load the built page with window.DB_URL="http://127.0.0.1:9200".
// Minimal Firebase Realtime Database REST + SSE emulator (GET/PUT/PATCH on /x/y.json, EventSource on /x.json)
const http=require('http');let db={};const subs=[];
const getAt=(p)=>p.reduce((o,k)=>o&&o[k]!==undefined?o[k]:null,db);
function setAt(p,v){if(p.length===0){db=v;return}let o=db;for(let i=0;i<p.length-1;i++){if(typeof o[p[i]]!=='object'||o[p[i]]===null)o[p[i]]={};o=o[p[i]]}if(v===null)delete o[p[p.length-1]];else o[p[p.length-1]]=v}
function patchAt(p,obj){for(const [k,v] of Object.entries(obj)){setAt([...p,...k.split('/').filter(Boolean)],v)}}
function rel(sub,p){if(p.length<sub.path.length)return null;for(let i=0;i<sub.path.length;i++)if(sub.path[i]!==p[i])return null;return '/'+p.slice(sub.path.length).join('/')}
function notify(method,path,v){for(const s of subs){const r=rel(s,path);if(r===null){const d=getAt(s.path);s.res.write(`event: put\ndata: ${JSON.stringify({path:'/',data:d===undefined?null:d})}\n\n`);continue}
  s.res.write(`event: ${method==='PATCH'?'patch':'put'}\ndata: ${JSON.stringify({path:r||'/',data:v})}\n\n`)}}
http.createServer((req,res)=>{
  const url=new URL(req.url,'http://x');const path=url.pathname.replace(/\.json$/,'').split('/').filter(Boolean);
  res.setHeader('Access-Control-Allow-Origin','*');res.setHeader('Access-Control-Allow-Methods','GET,PUT,PATCH,OPTIONS');res.setHeader('Access-Control-Allow-Headers','*');
  if(req.method==='OPTIONS'){res.end();return}
  if(req.method==='GET'&&(req.headers.accept||'').includes('text/event-stream')){res.writeHead(200,{'Content-Type':'text/event-stream','Cache-Control':'no-cache'});const s={path,res};subs.push(s);const d=getAt(path);res.write(`event: put\ndata: ${JSON.stringify({path:'/',data:d===undefined?null:d})}\n\n`);req.on('close',()=>subs.splice(subs.indexOf(s),1));return}
  let body='';req.on('data',c=>body+=c);req.on('end',()=>{
    if(req.method==='GET'){res.end(JSON.stringify(getAt(path)??null));return}
    const v=JSON.parse(body||'null');
    if(req.method==='PUT')setAt(path,v);else if(req.method==='PATCH')patchAt(path,v);
    notify(req.method,path,v);res.end(JSON.stringify(v));
  });
}).listen(9200,'127.0.0.1',()=>console.log('mockdb on 9200'));
