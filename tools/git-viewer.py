#!/usr/bin/env python3
"""
Git HTML Viewer - Serves HTML files from Gitea repos as rendered webpages
Usage: python3 git-viewer.py
Then access: http://localhost:8081/repo/branch/path/to/file.html
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
from urllib.error import HTTPError
import os
import sys

PORT = 8081
GITEA_BASE = "http://gitea:3000/chris"

class GitViewerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/view/'):
            self.serve_git_html()
        elif self.path == '/' or self.path == '/index.html':
            self.serve_index()
        else:
            # Serve static files from research-hub
            self.path = '/root/.openclaw/workspace/research-hub' + self.path
            super().do_GET()
    
    def serve_git_html(self):
        """Serve HTML files from Git repos with proper content-type"""
        try:
            # Parse path: /view/repo/branch/path/to/file.html
            parts = self.path.strip('/').split('/', 4)
            if len(parts) < 5:
                self.send_error(400, "Invalid path format. Use: /view/repo/branch/path/to/file.html")
                return
            
            _, repo, branch, *file_parts = parts
            file_path = '/'.join(file_parts)
            
            # Construct Gitea raw URL
            gitea_url = f"{GITEA_BASE}/{repo}/raw/branch/{branch}/{file_path}"
            
            print(f"Fetching: {gitea_url}")
            
            # Fetch from Gitea
            with urllib.request.urlopen(gitea_url) as response:
                content = response.read()
            
            # Serve with proper HTML content-type
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            
        except HTTPError as e:
            self.send_error(404, f"File not found in repository: {e}")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")
    
    def serve_index(self):
        """Serve index page with quick links"""
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Git HTML Viewer</title>
    <style>
        body { font-family: monospace; background: #0a0a1a; color: #e0e0f0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #6366f1; text-align: center; }
        .link-box { background: #111128; border: 1px solid #333; border-radius: 8px; padding: 20px; margin: 20px 0; }
        .link-box h3 { color: #22c55e; margin-bottom: 10px; }
        .link-box a { color: #6366f1; text-decoration: none; display: block; margin: 5px 0; }
        .link-box a:hover { color: #a855f7; }
        .format { background: #0d0d24; padding: 15px; border-radius: 6px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Git HTML Viewer</h1>
        
        <div class="format">
            <h3>📝 URL Format:</h3>
            <code>http://localhost:8081/view/REPO/BRANCH/PATH/TO/FILE.html</code>
            <p>This will fetch HTML files from your Gitea repos and serve them as rendered webpages.</p>
        </div>
        
        <div class="link-box">
            <h3>🌑 benford-fun Repository</h3>
            <a href="/view/benford-fun/main/results/html/blackhole_simulator_5D_prime.html">Black Hole Simulator 5D</a>
            <a href="/view/benford-fun/main/results/html/metric_visualization.html">Metric Visualization</a>
            <a href="/view/benford-fun/main/results/html/analysis_tools.html">Analysis Tools</a>
        </div>
        
        <div class="link-box">
            <h3>💻 optical-computing-workspace</h3>
            <a href="/view/optical-computing-workspace/main/simulator.html">N-Radix Simulator</a>
            <a href="/view/optical-computing-workspace/main/visualization.html">Optical Visualization</a>
        </div>
        
        <div class="link-box">
            <h3>🌍 Other Repositories</h3>
            <a href="/view/Climate_Benford/main/visualization.html">Climate Benford Analysis</a>
            <a href="/view/nradix-chip-package/main/docs/index.html">Chip Package Docs</a>
        </div>
        
        <div style="text-align: center; margin-top: 40px;">
            <a href="http://localhost:8080/working-index.html" style="background: #6366f1; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none;">← Back to Research Hub</a>
        </div>
    </div>
</body>
</html>"""
        
        content = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__ == "__main__":
    print(f"Starting Git HTML Viewer on port {PORT}")
    print(f"Access: http://localhost:{PORT}")
    print(f"URL format: http://localhost:{PORT}/view/repo/branch/path/to/file.html")
    print(f"Fetching from: {GITEA_BASE}")
    print()
    
    with socketserver.TCPServer(("", PORT), GitViewerHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            httpd.shutdown()