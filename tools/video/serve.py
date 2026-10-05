# Local helper: serves this folder (with byte ranges for video seeking) and accepts PUT /out/<name> uploads.
import http.server, os, re
ROOT = os.path.dirname(os.path.abspath(__file__))
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def do_PUT(self):
        m = re.fullmatch(r'/out/([\w.-]+)', self.path)
        if not m: self.send_error(400); return
        os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
        n = int(self.headers['Content-Length'])
        with open(os.path.join(ROOT, 'out', m.group(1)), 'wb') as f: f.write(self.rfile.read(n))
        self.send_response(201); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', 8768), H).serve_forever()
