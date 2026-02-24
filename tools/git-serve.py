#!/usr/bin/env python3
"""Proxies HTML files from Gitea with correct content-type so they render."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

GITEA = "http://gitea:3000/chris"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.serve_index()
            return
        
        # Everything else: proxy from Gitea
        # URL pattern: /repo/branch/path/to/file.html
        parts = self.path.strip('/').split('/', 2)
        if len(parts) < 3:
            self.send_error(400, "Use: /repo/branch/path/to/file.html")
            return
        
        repo, branch, filepath = parts[0], parts[1], parts[2]
        url = f"{GITEA}/{repo}/raw/branch/{branch}/{filepath}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'GitServe/1.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read()
            
            ct = 'text/html; charset=utf-8' if filepath.endswith('.html') else \
                 'application/javascript' if filepath.endswith('.js') else \
                 'text/css' if filepath.endswith('.css') else \
                 'application/json' if filepath.endswith('.json') else \
                 'image/png' if filepath.endswith('.png') else \
                 'text/plain'
            
            self.send_response(200)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(404, f"Not found: {e}")
    
    def do_HEAD(self):
        self.do_GET()
    
    def serve_index(self):
        html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Git HTML Viewer</title>
<style>
body{font-family:monospace;background:#0a0a1a;color:#e0e0f0;padding:20px;max-width:900px;margin:0 auto}
h1{color:#6366f1;text-align:center}
.card{background:#111128;border:1px solid #1a1a3a;border-radius:8px;padding:20px;margin:15px 0}
a{color:#6366f1;text-decoration:none;display:block;padding:8px 0}
a:hover{color:#a855f7}
.info{background:#0d0d24;border:1px solid #333;border-radius:6px;padding:15px;margin:15px 0}
</style></head><body>
<h1>🔗 Git HTML Viewer</h1>
<div class="info">
<p><strong>Click any link to view it as a rendered webpage.</strong></p>
<p>URL format: <code>http://localhost:8081/repo/branch/path/to/file.html</code></p>
</div>

<div class="card">
<h2>🌑 benford-fun</h2>
<a href="/benford-fun/main/results/html/blackhole_simulator_5D_prime.html">🚀 Prime Black Hole Simulator</a>
<a href="/benford-fun/main/results/html/blackhole_simulator.html">🕳️ Black Hole Simulator</a>
<a href="/benford-fun/main/results/html/benford_blackhole_bars.html">📊 Benford Black Hole Bars</a>
<a href="/benford-fun/main/results/html/dimension_stack_chart.html">📐 Dimension Stack Chart</a>
<a href="/benford-fun/main/results/html/einstein_benford_blackhole.html">🌌 Einstein-Benford Black Hole</a>
<a href="/benford-fun/main/results/html/wormhole_3d_interactive.html">🌀 3D Wormhole Interactive</a>
</div>

<div class="card">
<h2>📡 Research Hub Tools</h2>
<a href="http://localhost:8080/working-index.html">← Back to Research Hub (port 8080)</a>
<a href="http://localhost:3000/chris" target="_blank">📁 Browse All Gitea Repos</a>
</div>
</body></html>"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(html))
        self.end_headers()
        self.wfile.write(html.encode())

print("🚀 Git HTML Viewer on http://localhost:8081")
HTTPServer(('', 8081), Handler).serve_forever()
