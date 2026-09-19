"""Крошечный HTTP-сервер для Render Web Service.

Render требует, чтобы приложение слушало порт, иначе считает его упавшим.
Этот сервер отвечает 200 OK на любой GET — Render доволен.
"""

from __future__ import annotations

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        # не спамим логи
        pass


def start_healthcheck() -> None:
    """Запустить HTTP-сервер в фоновом потоке."""
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"✅ Healthcheck server on port {port}")
