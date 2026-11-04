# Report viewer

A deliberately minimal store-and-serve web app, **separate from the MCP server**.

The agent assembles the finished risk memo as a **single self-contained HTML file**
(charts embedded as base64) in the sandbox, then `POST`s it here and gets back a public
link to hand the analyst. This service does no analysis, no database access, and holds no
secrets — it only keeps the last few reports in memory and serves them.

| Route | Purpose |
|---|---|
| `POST /reports` | Body `{"html": "...", "title": "..."}` (or raw `text/html`). Returns `{"id","url"}`. |
| `GET /r/{id}` | Serves the stored HTML report. |
| `GET /health` | Liveness + current report count. |

Storage is an in-memory bounded ring (`MAX_REPORTS`, default 200); links live for the
life of the container. Deployed with anonymous external ingress on port 8000, the same
pattern as the MCP server. See `../DEPLOYMENT.md`.
