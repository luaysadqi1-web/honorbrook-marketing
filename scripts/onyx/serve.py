#!/usr/bin/env python3
"""Local preview server that mimics the host's clean URLs (/medicare-advantage serves medicare-advantage.html).
    python3 scripts/onyx/serve.py <dir> <port>"""
import http.server, os, sys
root = os.path.abspath(sys.argv[1]); port = int(sys.argv[2])

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=root, **k)
    def send_head(self):
        p = self.path.split('?')[0].split('#')[0]
        fs = os.path.join(root, p.lstrip('/'))
        if not os.path.exists(fs) and os.path.exists(fs + '.html'): self.path = p + '.html'
        return super().send_head()
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()
    def log_message(self, *a): pass

http.server.ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
