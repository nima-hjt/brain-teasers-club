import json,os,html,datetime
def load(p): return json.load(open(p,encoding='utf-8'))
odd=load('content/odd.json')+load('content/odd-new.json')
emoji=load('content/emoji.json')+load('content/emoji-new.json')
logic=load('content/logic.json')+load('content/logic-new.json')
animals=load('content/animals.json')
def lvl(it):  # difficulty level 1-3 (level-based picking in src/index.html)
    l=it.get('lvl',2); assert l in (1,2,3),it; return l
def added(it):  # first date (YYYY-MM-DD) the Daily may use this puzzle; '' = always
    d=it.get('added',''); assert d=='' or (isinstance(d,str) and len(d)==10 and datetime.date.fromisoformat(d)),it; return d
def norm(items,cat=None):
    out=[]
    for it in items:
        c=cat or it.get('cat','')
        assert it['a'] not in it['wrong'] and len(set([it['a']]+it['wrong']))==4, it
        for v in [it['q'],it['a'],c,it.get('why','')]+it['wrong']: assert isinstance(v,str),it
        out.append([it['q'],it['a'],c,it['wrong'],it.get('why',''),lvl(it),added(it)])
    return out
E=norm(emoji);L=norm(logic,'Logic');A=norm(animals)
O=[[p['common'],p['odd'],lvl(p),added(p)] for p in odd]
for name,arr in (('emoji',E),('logic',L),('animals',A)):
    qs=[x[0] for x in arr];assert len(qs)==len(set(qs)),(name,'dup q')
pairs=set()
for c,o,*_ in O:
    k=frozenset([c,o]);assert k not in pairs,('dup odd',c,o);pairs.add(k)
bank='const ODD = %s;\nconst EMOJI = %s;\nconst LOGIC = %s;\nconst FACTS = %s;'%tuple(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in (O,E,L,A))
t=open('src/index.html').read()
assert '/*__BANK__*/' in t and '/*__I18N__*/' in t
page=t.replace('/*__BANK__*/',bank).replace('/*__I18N__*/',open('src/i18n.js').read())
# Puzzle translations (content/i18n/<lang>.json, keyed by bank index) are served as dist/i18n/<lang>.json.
TRANS={}
for f in sorted(os.listdir('content/i18n')) if os.path.isdir('content/i18n') else []:
    if not f.endswith('.json'): continue
    tr=load('content/i18n/'+f)
    for typ,bankarr in (('logic',L),('facts',A)):
        for k,v in tr.get(typ,{}).items():
            assert 0<=int(k)<len(bankarr) and len(v)==4 and len(v[2])==3 and len({v[1],*v[2]})==4 and all(isinstance(x,str) and x for x in [v[0],v[1],*v[2]]),(f,typ,k)
    TRANS[f]=tr
open('index.html','w').write(page)   # artifact version (claude.ai adds the skeleton)

# ---------- standalone site for hosting ----------
SITE_NAME='Brain Teasers Club'
SITE_URL='https://brainteasersclub.app'
DESC='Quick brain-teaser quiz: odd one out, emoji riddles, logic and animal facts. Daily challenge, duel a friend, streaks.'
os.makedirs('dist',exist_ok=True)
def skeleton(title,body,desc=DESC,extra_head=''):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
     '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
     # one address only: www. and the Cloudflare project address forward to the main domain (path, query and #code kept)
     r'<script>if(/^(www\.brainteasersclub\.app|brainteasersclub-git\.pages\.dev)$/.test(location.hostname))location.replace("https://brainteasersclub.app"+location.pathname+location.search+location.hash)</script>'
     f'<title>{title}</title><meta name="description" content="{html.escape(desc)}">'
     '<meta name="theme-color" content="#141430"><link rel="icon" href="icon.svg" type="image/svg+xml">'
     '<link rel="apple-touch-icon" href="icon-180.png"><link rel="manifest" href="manifest.webmanifest">'
     f'<meta property="og:title" content="{title}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{SITE_URL}/og.png"><link rel="canonical" href="{SITE_URL}/"><meta name="twitter:card" content="summary_large_image">'
     '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}body{margin:0}</style>'
     +extra_head+'</head><body>'+body+'</body></html>')
game=page.replace('<title>Brain Teasers Club</title>','',1)
open('dist/index.html','w').write(skeleton(SITE_NAME,game))
# Tracking links: brainteasersclub.app/btc and /wildfacts (YouTube), /fb (Facebook) and /ig (Instagram) serve the same game, so each channel's
# visits show up as its own path in Cloudflare Web Analytics (canonical stays the home page; not in the sitemap).
for src in ('btc','wildfacts','fb','ig'): open(f'dist/{src}.html','w').write(skeleton(SITE_NAME,game))

# shared style for the text pages (reuses the game's tokens)
style_start=page.index('<style>');style_end=page.index('</style>')+8
tokens=page[style_start:style_end]
textcss='<style>.doc{max-width:640px;margin:0 auto;padding:20px 16px 40px;line-height:1.6}.doc h1{font-family:var(--display);font-size:2rem;margin:0 0 6px}.doc h2{font-family:var(--display);font-size:1.3rem;margin:28px 0 6px}.doc p,.doc li{color:var(--fg)}.doc a{color:var(--accent)}.doc .back{display:inline-block;margin-bottom:16px;font-weight:800}.doc .fact{background:var(--surface);border-radius:14px;padding:12px 14px;margin:10px 0}.doc .fact b{display:block;font-family:var(--display);font-weight:600}.doc .fact small{color:var(--muted)}</style>'
fonts='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700;800&display=swap">'
head_extra=fonts+tokens+textcss
nav='<a class="back" href="./">← Back to the game</a>'
today=datetime.date.today().strftime('%B %d, %Y')

about=f'''<main class="doc">{nav}<h1>About Brain Teasers Club</h1>
<p>Brain Teasers Club is a free, fast quiz game made for the <a href="https://www.youtube.com/@BrainTeasersClub">Brain Teasers Club</a> and <a href="https://www.youtube.com/@wildfactsdaily-q3z">Wild Facts</a> YouTube channels. Ten puzzles, a ticking clock, limited lives, and a score to beat.</p>
<h2>How to play</h2>
<p>Pick a difficulty and a mode. Each round is ten puzzles. Answer before the timer runs out: the faster you are, the more points you score, and consecutive correct answers raise your multiplier up to 2×. Run out of lives and the round ends early.</p>
<p><strong>Odd One Out</strong> shows a grid of identical emoji with one look-alike hiding among them; tap it. <strong>Emoji Riddles</strong> spell out a movie, saying or word in emoji; pick the answer. <strong>Quick Logic</strong> has trick questions and number patterns. <strong>Animal Facts</strong> are surprising-but-true questions about the natural world. <strong>Random Mix</strong> and <strong>Custom Mix</strong> combine them.</p>
<h2>Daily Challenge</h2>
<p>Everyone in the world gets the same ten puzzles each day, always on Normal, with one attempt. Finish it to keep your streak alive. Every seventh day earns a streak freeze that covers one missed day.</p>
<h2>Playing with friends</h2>
<p><strong>Duel</strong> puts two players on one phone, face to face, racing for the same puzzle. <strong>Pass &amp; Play</strong> lets you take turns on one phone with the same ten puzzles. <strong>Live Match</strong> puts each player on their own phone, anywhere: you play the same ten puzzles at the same time and watch each other's score live. <strong>Challenge by Link</strong> gives you a code and a link so a friend can play the identical round later and compare scores.</p>
<h2>Difficulty</h2>
<p>Easy gives longer timers, five lives and smaller grids (scores ×0.75). Normal is the standard round. Hard shortens timers, gives two lives and bigger grids (×1.5). Impossible is one life, very short timers and the biggest grids (×2.5).</p>
<h2>Accuracy</h2>
<p>Every animal fact in the game was checked against reference sources such as National Geographic, the Smithsonian, Guinness World Records and NOAA before publication, and we do not use invented statistics. If you spot a mistake, tell us in the comments of any Brain Teasers Club video.</p>
<p><a href="privacy.html">Privacy policy</a> · <a href="facts.html">Animal facts</a></p></main>'''
notfound=f'''<main class="doc">{nav}<h1>Page not found</h1>
<p>That page doesn't exist. <a href="./">Go back to the game</a>.</p></main>'''
open('dist/404.html','w').write(skeleton('Not found · Brain Teasers Club',notfound,extra_head=head_extra))
open('dist/about.html','w').write(skeleton('About · Brain Teasers Club',about,extra_head=head_extra))

privacy=f'''<main class="doc">{nav}<h1>Privacy Policy</h1><p><small>Last updated {today}</small></p>
<p>Brain Teasers Club ("the game", "we") is a browser game. This page explains what information is handled when you play.</p>
<h2>What we store on your device</h2>
<p>The game saves your settings and progress (chosen difficulty, sound on or off, best scores, daily streak, XP and level, custom-mix selection, which puzzles you have already seen so they don't repeat, and whether today's Daily Challenge has been played) in your browser's local storage. This data stays on your device and is deleted if you clear your browser data. Player names typed for Duel and Pass &amp; Play are used only on screen during that round.</p>
<h2>Live Match</h2>
<p>When you play a Live Match, the name you enter, your scores for that match and a list of the puzzle numbers you have already seen are shared through our match server (Google Firebase) with the other player in that room, so the game can pick puzzles neither of you has seen. This contains no other personal information, and the room code is the only way to reach it.</p>
<h2>Anonymous play statistics</h2>
<p>To learn which puzzles and modes people enjoy, the game sends a small anonymous record to our Firebase database for each visit: where the visit came from (for example our YouTube channel or a shared link), the language, whether it is a phone or a computer, how many rounds were started and finished, which modes were played and the active playing time. It includes a random device number stored in local storage so we can count players rather than page loads. It contains no name, no account and no cookie, and we never combine it with anything else. You can turn it off for your device by opening <a href="/?notrack">brainteasersclub.app/?notrack</a> once.</p>
<h2>What we do not collect</h2>
<p>We do not have user accounts, and we do not ask for email addresses or any other personal information. Names typed into the game are used only as described above. The game has no server of its own.</p>
<h2>Advertising</h2>
<p>We use Google AdSense to show advertisements. Google and its partners may use cookies and similar technologies to serve ads based on your prior visits to this or other websites, and to measure ad performance. You can opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads">Google Ads Settings</a>, and learn how Google uses information from sites that use its services at <a href="https://policies.google.com/technologies/partner-sites">policies.google.com/technologies/partner-sites</a>. Where required by law, you will be asked for consent before personalised ads are shown.</p>
<h2>Hosting and logs</h2>
<p>The site is served by a hosting provider that may record standard technical logs (such as IP address, browser type and pages requested) for security and performance. We do not use this data to identify you.</p>
<h2>Analytics</h2>
<p>We use Cloudflare Web Analytics to count visits and to see which pages are read and which websites (such as YouTube or a search engine) people arrive from. It does not use cookies or store anything on your device, and it does not identify individual visitors. See <a href="https://www.cloudflare.com/web-analytics/">Cloudflare Web Analytics</a> for details.</p>
<h2>Children</h2>
<p>The game is intended for a general audience and does not knowingly collect personal information from children.</p>
<h2>Changes</h2>
<p>If this policy changes, the new version will be posted here with an updated date.</p>
<h2>Contact</h2>
<p>Questions about this policy can be left as a comment on any <a href="https://www.youtube.com/@BrainTeasersClub">Brain Teasers Club</a> video.</p></main>'''
open('dist/privacy.html','w').write(skeleton('Privacy Policy · Brain Teasers Club',privacy,'Privacy policy for the Brain Teasers Club quiz game.',head_extra))

# facts page: 60 animal facts as readable content (why lines), without quiz framing
import random
rnd=random.Random(7);sample=rnd.sample(animals,60)
items=''.join(f'<div class="fact"><b>{html.escape(f["q"])}</b><span style="color:var(--accent);font-weight:800">{html.escape(f["a"])}</span> — {html.escape(f["why"])}<br><small>{html.escape(f["cat"])}</small></div>' for f in sample if f.get('why'))
facts=f'''<main class="doc">{nav}<h1>60 Surprising Animal Facts</h1><p>A selection of the checked facts behind the Animal Facts mode, from the <a href="https://www.youtube.com/@wildfactsdaily-q3z">Wild Facts</a> channel. Think you know them? <a href="./">Play the quiz</a>.</p>{items}<p><a href="about.html">About the game</a> · <a href="privacy.html">Privacy</a></p></main>'''
open('dist/facts.html','w').write(skeleton('60 Surprising Animal Facts · Brain Teasers Club',facts,'Sixty checked, surprising animal facts from the Brain Teasers Club quiz.',head_extra))

# manifest, sw, robots, icon
json.dump({"name":SITE_NAME,"short_name":"Brain Teasers","start_url":"./","display":"standalone","background_color":"#141430","theme_color":"#141430","description":DESC,
  "icons":[{"src":"icon.svg","sizes":"any","type":"image/svg+xml"},{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]},open('dist/manifest.webmanifest','w'))
open('dist/stats.html','w',encoding='utf-8').write(open('src/stats.html',encoding='utf-8').read())  # owner's private stats page (noindex, unlinked)
os.makedirs('dist/i18n',exist_ok=True)
for f,tr in TRANS.items(): json.dump(tr,open('dist/i18n/'+f,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
open('dist/sw.js','w').write('''// Minimal offline cache: the game works without a connection once visited.
const C="btc-v23";const FILES=["./","index.html","about.html","privacy.html","facts.html","manifest.webmanifest","icon.svg"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(u.origin!==location.origin)return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request)))});''')
open('dist/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
open('dist/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE_URL}/{p}</loc></url>' for p in ['','about','facts','privacy'])+'</urlset>')
import shutil
for f in ['icon-180.png','icon-192.png','icon-512.png','og.png']: shutil.copy('assets/'+f,'dist/'+f)
open('dist/icon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="112" fill="#141430"/><text x="256" y="330" font-size="300" text-anchor="middle">🧠</text><circle cx="400" cy="112" r="56" fill="#ffb347"/><text x="400" y="134" font-size="64" font-weight="700" text-anchor="middle" fill="#2a1a00" font-family="Arial,sans-serif">?</text></svg>')
print('odd',len(O),'emoji',len(E),'logic',len(L),'facts',len(A),'total',len(O)+len(E)+len(L)+len(A));print('dist:',sorted(os.listdir('dist')))
