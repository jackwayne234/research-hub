#!/usr/bin/env python3
"""
Git HTML Viewer - Serves HTML files from Gitea repos as rendered webpages
Usage: python3 git-viewer-fixed.py
Then access: http://localhost:8081/view/repo/branch/path/to/file.html
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
from urllib.error import HTTPError
import ssl
import os
import sys

PORT = 8081
GITEA_BASE = "http://gitea:3000/chris"

class GitViewerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Request: {self.path}")
        
        if self.path.startswith('/view/'):
            self.serve_git_html()
        elif self.path == '/' or self.path == '/index.html':
            self.serve_index()
        else:
            # Try to serve from research-hub directory
            try:
                # Remove leading slash and construct path
                rel_path = self.path.lstrip('/')
                full_path = f'/root/.openclaw/workspace/research-hub/{rel_path}'
                
                if os.path.isfile(full_path):
                    with open(full_path, 'rb') as f:
                        content = f.read()
                    
                    # Determine content type
                    if rel_path.endswith('.html'):
                        content_type = 'text/html; charset=utf-8'
                    elif rel_path.endswith('.js'):
                        content_type = 'application/javascript'
                    elif rel_path.endswith('.css'):
                        content_type = 'text/css'
                    elif rel_path.endswith('.json'):
                        content_type = 'application/json'
                    else:
                        content_type = 'text/plain'
                    
                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    return
                else:
                    self.send_error(404, f"File not found: {rel_path}")
                    return
            except Exception as e:
                self.send_error(500, f"Error serving file: {e}")
                return
    
    def serve_git_html(self):
        """Serve HTML files from Git repos with proper content-type"""
        try:
            # Parse path: /view/repo/branch/path/to/file.html
            path_parts = self.path.strip('/').split('/')
            print(f"Path parts: {path_parts}")
            
            if len(path_parts) < 4:
                self.send_error(400, "Invalid path format. Use: /view/repo/branch/path/to/file.html")
                return
            
            # Remove 'view' and extract repo/branch/file parts
            _, repo, branch, *file_parts = path_parts
            file_path = '/'.join(file_parts)
            
            print(f"Repo: {repo}, Branch: {branch}, File: {file_path}")
            
            # Construct Gitea raw URL
            gitea_url = f"{GITEA_BASE}/{repo}/raw/branch/{branch}/{file_path}"
            print(f"Fetching from: {gitea_url}")
            
            # Create request with headers
            req = urllib.request.Request(gitea_url)
            req.add_header('User-Agent', 'GitViewer/1.0')
            
            # Fetch from Gitea
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
            
            print(f"Successfully fetched {len(content)} bytes")
            
            # Determine content type based on file extension
            if file_path.endswith('.html'):
                content_type = 'text/html; charset=utf-8'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.json'):
                content_type = 'application/json'
            else:
                content_type = 'text/plain'
            
            # Serve with proper content-type
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'public, max-age=300')  # 5 minute cache
            self.end_headers()
            self.wfile.write(content)
            
        except HTTPError as e:
            print(f"HTTP Error: {e}")
            self.send_error(404, f"File not found in repository: {e}")
        except Exception as e:
            print(f"General Error: {e}")
            self.send_error(500, f"Server error: {e}")
    
    def serve_index(self):
        """Serve index page with quick links"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Git HTML Viewer - Click & View</title>
    <style>
        body {{ font-family: 'JetBrains Mono', monospace; background: #0a0a1a; color: #e0e0f0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ 
            background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-align: center; font-size: 2.2rem; margin-bottom: 10px;
        }}
        .subtitle {{ text-align: center; color: #8888aa; margin-bottom: 30px; }}
        .repo-section {{ background: #111128; border: 1px solid #1a1a3a; border-radius: 12px; padding: 25px; margin: 20px 0; }}
        .repo-section h2 {{ color: #6366f1; margin-bottom: 15px; }}
        .file-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }}
        .file-card {{ background: #0d0d24; border: 1px solid #333; border-radius: 8px; padding: 15px; }}
        .file-card h3 {{ color: #22c55e; margin-bottom: 8px; font-size: 1rem; }}
        .file-card p {{ color: #8888aa; font-size: 0.85rem; margin-bottom: 10px; }}
        .file-card a {{ 
            color: #6366f1; text-decoration: none; font-weight: bold; 
            display: inline-block; padding: 6px 12px; background: rgba(99,102,241,0.1);
            border-radius: 4px; margin-top: 5px; transition: all 0.2s;
        }}
        .file-card a:hover {{ background: rgba(99,102,241,0.2); color: #a855f7; }}
        .hero {{ 
            background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(168,85,247,0.1));
            border: 1px solid rgba(99,102,241,0.3); border-radius: 12px;
            padding: 25px; text-align: center; margin-bottom: 30px;
        }}
        .back-link {{ 
            background: #6366f1; color: white; padding: 10px 20px; border-radius: 6px; 
            text-decoration: none; display: inline-block; margin-top: 20px;
        }}
        .back-link:hover {{ background: #a855f7; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Git HTML Viewer</h1>
        <div class="subtitle">Click any link below to view HTML files as rendered webpages!</div>
        
        <div class="hero">
            <h2>✅ Solution Active</h2>
            <p>This service fetches HTML files from your Gitea repositories and serves them with the correct content-type so they render as actual webpages instead of source code.</p>
        </div>

        <div class="repo-section">
            <h2>🌑 benford-fun Repository</h2>
            <div class="file-grid">
                <div class="file-card">
                    <h3>🌑 5D Prime Black Hole Simulator</h3>
                    <p>Interactive 5D prime-modified metric visualization</p>
                    <a href="/view/benford-fun/main/results/html/blackhole_simulator_5D_prime.html" target="_blank">🚀 View Live</a>
                </div>
                <div class="file-card">
                    <h3>🕳️ Black Hole Simulator</h3>
                    <p>Standard black hole physics simulator</p>
                    <a href="/view/benford-fun/main/results/html/blackhole_simulator.html" target="_blank">🚀 View Live</a>
                </div>
                <div class="file-card">
                    <h3>📊 Benford Black Hole Analysis</h3>
                    <p>Benford's Law analysis of black hole data</p>
                    <a href="/view/benford-fun/main/results/html/benford_blackhole_bars.html" target="_blank">🚀 View Live</a>
                </div>
                <div class="file-card">
                    <h3>📐 Dimension Stack Chart</h3>
                    <p>Multi-dimensional metric analysis</p>
                    <a href="/view/benford-fun/main/results/html/dimension_stack_chart.html" target="_blank">🚀 View Live</a>
                </div>
                <div class="file-card">
                    <h3>🌌 Einstein-Benford Black Hole</h3>
                    <p>Combined relativity and Benford analysis</p>
                    <a href="/view/benford-fun/main/results/html/einstein_benford_blackhole.html" target="_blank">🚀 View Live</a>
                </div>
                <div class="file-card">
                    <h3>🌀 3D Wormhole Interactive</h3>
                    <p>Interactive wormhole geometry visualization</p>
                    <a href="/view/benford-fun/main/results/html/wormhole_3d_interactive.html" target="_blank">🚀 View Live</a>
                </div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <a href="http://localhost:8080/working-index.html" class="back-link">← Back to Research Hub</a>
            <a href="http://gitea:3000/chris" class="back-link" target="_blank">📁 Browse All Repos</a>
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
    print(f"🚀 Starting Git HTML Viewer on port {PORT}")
    print(f"📡 Access: http://localhost:{PORT}")
    print(f"🔗 URL format: http://localhost:{PORT}/view/repo/branch/path/to/file.html")
    print(f"📂 Fetching from: {GITEA_BASE}")
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), GitViewerHandler) as httpd:
            print(f"✅ Server running! Try: http://localhost:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)