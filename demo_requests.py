"""Exercise a running API with real HTTP requests and save evidence."""

import argparse
import html
import json
import platform
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import requests


def run_demo(base_url, output_dir):
    """Check successful calls and errors against a live Flask server."""
    records = []
    session = requests.Session()
    session.trust_env = False

    def call(method, path, expected_status, **kwargs):
        response = session.request(
            method, f"{base_url}{path}", timeout=5, **kwargs
        )
        assert response.status_code == expected_status, response.text
        assert response.headers["Content-Type"].startswith("application/json")
        body = response.json()
        assert isinstance(body, dict), "Expected a JSON object."
        if expected_status >= 400:
            assert body.get("error") and body.get("message")

        records.append(
            {
                "method": method,
                "url": response.url,
                "request_body": response.request.body.decode("utf-8")
                if isinstance(response.request.body, bytes)
                else response.request.body,
                "status": response.status_code,
                "content_type": response.headers["Content-Type"],
                "response": body,
            }
        )
        print(f"PASS  {method:4} {path:12} HTTP {response.status_code}")
        print(json.dumps(body, indent=2))
        return body, response

    welcome, _ = call("GET", "/hello", 200)
    assert welcome["message"] == "Welcome to the Flask Micro-API!"

    before, _ = call("GET", "/data", 200)
    assert before["count"] == len(before["items"])
    assert before["count"] >= 2

    created, _ = call(
        "POST",
        "/data",
        201,
        json={"id": -99, "name": "  Pencil  ", "category": "school"},
    )
    expected_id = max(item["id"] for item in before["items"]) + 1
    assert created["item"] == {
        "id": expected_id,
        "name": "Pencil",
        "category": "school",
    }

    after, _ = call("GET", "/data", 200)
    assert after["count"] == before["count"] + 1
    assert after["items"] == before["items"] + [created["item"]]

    call("POST", "/data", 400, json={"name": "Missing category"})
    call("POST", "/data", 400, json={"name": " ", "category": "school"})
    call("POST", "/data", 400, json={"name": "Pencil", "category": 7})
    call("POST", "/data", 400, json=[])
    call(
        "POST",
        "/data",
        400,
        data="{",
        headers={"Content-Type": "application/json"},
    )
    call("POST", "/data", 415, data="not JSON")
    call("GET", "/missing", 404)
    _, unsupported = call("PUT", "/data", 405)
    assert "GET" in unsupported.headers["Allow"]
    assert "POST" in unsupported.headers["Allow"]

    final, _ = call("GET", "/data", 200)
    assert final == after, "Rejected requests must not change the collection."
    session.close()

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "client": "Python requests (real HTTP calls)",
        "python_version": platform.python_version(),
        "flask_version": version("Flask"),
        "requests_version": version("requests"),
        "result": "PASS",
        "requests_passed": len(records),
        "checks": [
            "Welcome message and structured sample data",
            "Creation, trimming, server-assigned ID, and GET persistence",
            "JSON errors for invalid input, media type, route, and method",
            "Allow header preserved and rejected writes do not mutate data",
        ],
        "calls": records,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    report_json = json.dumps(report, indent=2)
    results_path = output_dir / "results.json"
    results_path.write_text(report_json + "\n", encoding="utf-8")
    success_path = output_dir / "successful_calls.html"
    validation_path = output_dir / "validation_calls.html"
    write_html_report(report, success_path, records[:4])
    write_html_report(report, validation_path, records[4:])
    print(f"\nAll {len(records)} HTTP checks passed. Evidence: {output_dir}")


def write_html_report(report, destination, records):
    """Render captured responses verbatim as a readable evidence page."""
    sections = []
    for record in records:
        request_body = record["request_body"]
        request_text = request_body or "(no request body)"
        response_text = json.dumps(record["response"], indent=2)
        sections.append(
            "<section>"
            f"<h2>{html.escape(record['method'])} "
            f"{html.escape(record['url'])}</h2>"
            f"<p><strong>PASS | HTTP {record['status']}</strong> | "
            f"{html.escape(record['content_type'])}</p>"
            f"<pre>Request body: {html.escape(request_text)}\n\n"
            f"Response JSON:\n{html.escape(response_text)}</pre>"
            "</section>"
        )

    document = (
        "<!doctype html><html lang='en'><meta charset='utf-8'>"
        "<title>Flask Micro-API | Live HTTP evidence</title>"
        "<style>body{max-width:1050px;margin:28px auto;padding:0 24px;"
        "font:16px system-ui;color:#17212b;background:#fff}"
        "h1{font-size:26px}h2{font-size:18px}"
        "section{border-top:1px solid #aaa;"
        "padding:8px 0}pre{font:15px/1.35 Consolas,monospace;"
        "white-space:pre-wrap}p{margin:8px 0}strong{color:#146433}</style>"
        "<h1>MC - SDIR | Flask Micro-API</h1>"
        "<p>Actual responses captured by "
        "<code>python demo_requests.py</code>.</p>"
        f"<p>Run: {html.escape(report['generated_at_utc'])}<br>"
        f"Python {report['python_version']} | "
        f"Flask {report['flask_version']} | "
        f"requests {report['requests_version']}<br>"
        f"Overall result: <strong>{report['requests_passed']} "
        "HTTP checks passed"
        "</strong></p>"
        + "".join(sections)
        + "</html>"
    )
    destination.write_text(document, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:5000")
    parser.add_argument("--output", type=Path, default=Path("evidence"))
    arguments = parser.parse_args()
    run_demo(arguments.base_url.rstrip("/"), arguments.output)


if __name__ == "__main__":
    main()
