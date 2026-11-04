"""Smoke-test the report viewer: health, POST a tiny HTML report, GET it back.
Set REPORT_HOST_URL to the deployed base URL (no trailing slash)."""
import json, os, urllib.request

BASE = os.environ.get("REPORT_HOST_URL", "http://127.0.0.1:8000").rstrip("/")


def _get(path):
    with urllib.request.urlopen(BASE + path, timeout=15) as r:
        return r.status, r.read()


def _post_json(path, obj):
    data = json.dumps(obj).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, json.loads(r.read())


if __name__ == "__main__":
    s, body = _get("/health")
    print("health:", s, body.decode())

    html = ("<!doctype html><meta charset=utf-8><title>Smoke</title>"
            "<h1>Report viewer OK</h1><p>round-trip works</p>")
    s, resp = _post_json("/reports", {"html": html, "title": "Smoke test"})
    print("post:", s, resp)

    url = resp["url"]
    s, got = _get("/r/" + url.rsplit("/r/", 1)[1])
    ok = b"Report viewer OK" in got
    print(f"get: {s} ({len(got)} bytes) served-correct={ok}")
    raise SystemExit(0 if ok else 1)
