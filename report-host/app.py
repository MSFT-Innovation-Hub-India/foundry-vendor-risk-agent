"""
Report-viewer service for the TPRM demo.

This is intentionally *dumb and separate* from the MCP server. Its ONLY job is to
accept a finished, self-contained HTML report (which the agent assembles in the
sandbox) and serve it back at a public URL so the analyst has a clickable link.
No database, no secrets, no managed identity — just store-and-serve.

Routes:
  POST /reports      {"html": "<full self-contained HTML>", "title": "..."}  -> {"id","url"}
  GET  /r/{id}       serve the stored HTML
  GET  /health       liveness

Storage is an in-memory, bounded ring (the demo runs min-replicas=1, so the link
lives as long as the container does). Nothing here is persisted or sensitive.
"""
import os
import secrets
from collections import OrderedDict

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

MAX_REPORTS = int(os.environ.get("MAX_REPORTS", "200"))
MAX_BYTES = int(os.environ.get("MAX_REPORT_BYTES", str(8 * 1024 * 1024)))  # 8 MB

app = FastAPI(title="tprm-report-viewer", docs_url=None, redoc_url=None)

# id -> {"html": str, "title": str}
_STORE: "OrderedDict[str, dict]" = OrderedDict()


def _base_url(request: Request) -> str:
    # Honor the ingress-provided host so we never need a configured public URL.
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    return f"{proto}://{host}"


@app.get("/health")
def health():
    return {"status": "ok", "count": len(_STORE)}


@app.post("/reports")
async def create_report(request: Request):
    # Accept JSON {"html","title"} or a raw text/html body.
    ctype = request.headers.get("content-type", "")
    if "application/json" in ctype:
        body = await request.json()
        html = body.get("html")
        title = (body.get("title") or "Risk memo").strip()
    else:
        html = (await request.body()).decode("utf-8", "replace")
        title = "Risk memo"

    if not html or not isinstance(html, str):
        raise HTTPException(status_code=400, detail="Missing 'html'.")
    if len(html.encode("utf-8")) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Report too large.")

    rid = secrets.token_urlsafe(8)
    _STORE[rid] = {"html": html, "title": title}
    _STORE.move_to_end(rid)
    while len(_STORE) > MAX_REPORTS:
        _STORE.popitem(last=False)  # evict oldest

    return JSONResponse({"id": rid, "url": f"{_base_url(request)}/r/{rid}"})


@app.get("/r/{rid}", response_class=HTMLResponse)
def get_report(rid: str):
    rec = _STORE.get(rid)
    if rec is None:
        raise HTTPException(status_code=404, detail="Report not found (it may have expired).")
    return HTMLResponse(content=rec["html"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8000")),
    )
