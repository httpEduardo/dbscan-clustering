import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .engine import dbscan

BASE_DIR = Path(__file__).resolve().parents[1]
WEB_DIR = BASE_DIR / "web"


def _safe_points(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return []
    return []


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def log_message(self, format, *args):
        return

    def _send_json(self, payload, status=HTTPStatus.OK):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode("utf-8"))

    def do_POST(self):
        if self.path == "/api/cluster":
            payload = self._read_json()
            points = _safe_points(payload.get("points", []))
            eps = float(payload.get("eps", 1.2))
            min_pts = int(payload.get("min_pts", 3))
            labels = dbscan(points, eps=eps, min_pts=min_pts)
            clusters = {}
            for point, label in zip(points, labels):
                clusters.setdefault(str(label), []).append(point)
            self._send_json({"clusters": clusters, "labels": labels})
            return
        self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        super().do_GET()


def run(host="127.0.0.1", port=5173):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"ClusterSprout running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run ClusterSprout")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5173)
    args = parser.parse_args()

    run(host=args.host, port=args.port)
