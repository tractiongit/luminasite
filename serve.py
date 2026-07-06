#!/usr/bin/env python3
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).parent / "clone"
INDEX = ROOT / "index.html"
PORT = 8080

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        # Try to serve the requested file/directory
        path = self.translate_path(self.path)
        if path != self.path and not os.path.exists(path):
            # Fallback to index.html for SPA routes (e.g. /procedimentos, /post/...)
            self.path = "/index.html"
        super().do_GET()

    def end_headers(self):
        # Disable caching for local development
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Serving clone at http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
        server.shutdown()
