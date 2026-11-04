"""Live verification: send the Acme questionnaire to the deployed agent, auto-approve
its MCP tool calls, print the final chat summary, and fetch the report link it returns.
Exercises agent -> MCP -> sandbox -> HTML report -> report viewer."""
import os, pathlib, re, urllib.request
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

ENDPOINT = os.environ.get("FOUNDRY_ENDPOINT",
    "https://your-foundry-account.services.ai.azure.com/api/projects/your-project")
AGENT = os.environ.get("AGENT_NAME", "TPRM-Risk-Assessor")
Q_PATH = str(pathlib.Path(__file__).resolve().parent.parent / "samples" / "questionnaire_acme_analytics.md")
KEYWORDS = ("reject", "approve with conditions", "residual", "recommendation")

q = open(Q_PATH, encoding="utf-8").read()
msg = ("Assess vendor 1003 (Acme Analytics) for onboarding. Their completed security "
       "questionnaire follows. Produce the risk memo with a recommendation.\n\n" + q)

with DefaultAzureCredential() as cred, \
     AIProjectClient(endpoint=ENDPOINT, credential=cred, allow_preview=True) as pc:
    oc = pc.get_openai_client(agent_name=AGENT)
    conv = oc.conversations.create()
    print(f"conversation: {conv.id}\n")

    resp = oc.responses.create(conversation=conv.id, input=[{"role": "user", "content": msg}])
    nudges = 0
    for step in range(1, 61):
        items = resp.output or []
        types = [getattr(it, "type", type(it).__name__) for it in items]
        txt = (resp.output_text or "").strip()
        print(f"[step {step}] status={getattr(resp,'status',None)} items={types}")
        if txt:
            print("   text:", txt[:600])

        approvals = [it for it in items if getattr(it, "type", None) == "mcp_approval_request"]
        if approvals:
            print("   -> approving MCP calls:", [getattr(a, "name", None) for a in approvals])
            resp = oc.responses.create(
                conversation=conv.id,
                input=[{"type": "mcp_approval_response",
                        "approval_request_id": a.id, "approve": True} for a in approvals])
            continue

        if txt and any(k in txt.lower() for k in KEYWORDS):
            print("\n=== FINAL CHAT SUMMARY ===\n" + txt)
            m = re.search(r"https?://[^\s)\]>]+/r/[^\s)\]>]+", txt)
            if m:
                link = m.group(0)
                print("\n=== REPORT LINK ===\n" + link)
                try:
                    with urllib.request.urlopen(link, timeout=20) as r:
                        body = r.read()
                    print(f"   fetched OK: HTTP {r.status}, {len(body)} bytes, "
                          f"embeds charts: {b'data:image' in body.lower()}")
                except Exception as e:
                    print("   WARNING: could not fetch report link:", e)
            else:
                print("\n(no report link found in the chat summary)")
            break

        nudges += 1
        if nudges > 4:
            print("\n(stopping; last output above)")
            break
        resp = oc.responses.create(conversation=conv.id, input=[{"role": "user", "content":
            "Continue: run the analysis in the sandbox and return the final recommendation "
            "(Approve / Approve with Conditions / Reject), the residual risk band, the key "
            "control gaps, and the memo link."}])
