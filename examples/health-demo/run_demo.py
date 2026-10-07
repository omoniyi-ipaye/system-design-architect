#!/usr/bin/env python3
"""Serve synthetic onboarding evidence over HTTP and generate a health report."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import threading

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from collect_evidence import collect_report, write_outputs  # noqa: E402

DEMO = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "demo-output", help="where JSON and HTML reports are written")
    args = parser.parse_args()
    payload = json.loads((DEMO / "sample-payload.json").read_text(encoding="utf-8"))
    payload["generated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    body = json.dumps(payload).encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            if self.path != "/api/health":
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format: str, *_args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        config_path = DEMO / "config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["sources"][0]["endpoint"] = f"http://127.0.0.1:{server.server_port}/api/health"
        report = collect_report(config, config_path)
        output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
        json_path = output_dir / "system-health.json"
        html_path = output_dir / "system-health.html"
        write_outputs(report, json_path, html_path)
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()

    print(f"Synthetic live-source demo: {report['status']}")
    print(f"Observed signals: {len(report['observations'])}; inferences: {len(report['diagnoses'])}; response plans: {len(report['response_plan'])}")
    print(f"HTML report: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
