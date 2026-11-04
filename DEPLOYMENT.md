# Deployment guide

This kit deploys in three parts:
1. a **serverless Azure SQL** database (schema + seed),
2. an **MCP server** on **Azure Container Apps** that reads the DB over its **managed
   identity** (no passwords), and
3. a **Foundry Copilot-harness prompt agent** that uses the MCP tool + a policy Knowledge
   source + the sandbox.

Replace every `<...>` placeholder with your own values. Scripts read these from env vars
(see `deploy/.env.example`); CLI commands below show the variables inline.

## Prerequisites
- `az` CLI logged in (`az login`) with rights to create an Azure SQL DB, an ACR build, and
  a Container App, and to assign roles on the Foundry account.
- You are (or can set yourself as) the **Microsoft Entra admin** on the SQL server — the DB
  scripts authenticate with your AAD token, no SQL admin password needed.
- Python 3.12+ with the Microsoft **ODBC Driver 18** (for the local DB-load scripts).

## 1. Azure SQL database
```bash
az sql db create -g <sql-rg> -s <sql-server> -n tprmdb \
  --edition GeneralPurpose --family Gen5 --capacity 2 \
  --compute-model Serverless --auto-pause-delay 60 --backup-storage-redundancy Local
```
Load schema + seed (uses your AAD token; needs the SQL firewall to allow your client IP —
most tenants already have a rule, or add one in the portal):
```bash
export TPRM_SQL_SERVER=<sql-server>.database.windows.net
python deploy/load_db.py          # runs schema.sql + seed_data.sql
```

## 2. MCP server on Container Apps
Build the image into your registry and deploy it with a **system-assigned managed identity**
and anonymous external ingress on port 8000:
```bash
az acr build -r <acr-name> -t tprm-mcp:v1 ./mcp

CONN='Driver={ODBC Driver 18 for SQL Server};Server=tcp:<sql-server>.database.windows.net,1433;Database=tprmdb;Encrypt=yes;TrustServerCertificate=no;Authentication=ActiveDirectoryMsi;Connection Timeout=30;'

az containerapp create -n tprm-mcp -g <aca-rg> --environment <aca-env> \
  --image <acr-name>.azurecr.io/tprm-mcp:v1 \
  --system-assigned --registry-server <acr-name>.azurecr.io --registry-identity system \
  --ingress external --target-port 8000 --transport http \
  --min-replicas 1 --max-replicas 1 --cpu 0.5 --memory 1.0Gi \
  --env-vars "TPRM_SQL_CONNECTION=$CONN"
```
Grant that managed identity read-only DB access (creates a contained user for it, grants
`SELECT` on the 5 views, and drops any leftover password login):
```bash
export MI_NAME=tprm-mcp            # = the Container App name for a system-assigned identity
python deploy/setup_db_identity.py
```
Smoke-test the endpoint (lists tools + calls two so the MI path is exercised):
```bash
export MCP_URL=https://<app-fqdn>/mcp
python deploy/smoke_test.py
```

> The MCP server exposes 6 **read-only, parameterized** tools (see `mcp/tool_contract.md`):
> `list_vendors`, `get_vendor_profile`, `get_incident_history`, `get_sla_breaches`,
> `get_prior_assessments`, `get_spend_history`. The agent writes no SQL.

## 3. Foundry Copilot-harness agent (portal)
In your Foundry project:
1. **Agents → New → Use the Microsoft Copilot harness** (Text). Pick a reasoning+tools model.
2. **Instructions:** paste `agent/agent_instructions.md`.
3. **Harness tools:** enable **File system read**, **File system write**, **Shell**.
4. **Tools → Add → MCP:** URL `https://<app-fqdn>/mcp`, auth **None**.
5. **Knowledge → Upload files:** all 7 `knowledge/*.md`.
6. **Save.**

### Agent identity needs Foundry Files write
So the agent can upload the finished memo + charts, grant its account identity the
**Foundry User** role (data-plane role `53ca6127-db72-4b80-b1b0-d745d6d5456d`):
```bash
az role assignment create --role "Foundry User" \
  --assignee-object-id <foundry-account-principal-id> --assignee-principal-type ServicePrincipal \
  --scope "/subscriptions/<subscription-id>/resourceGroups/<foundry-rg>/providers/Microsoft.CognitiveServices/accounts/<foundry-account>"
```
(The `<foundry-account-principal-id>` is the Foundry AIServices account's system-assigned
identity: `az cognitiveservices account show -n <foundry-account> -g <foundry-rg> --query identity.principalId -o tsv`.)

## Verify end to end
`deploy/verify_agent.py` sends the Acme questionnaire, **auto-approves the MCP tool calls**
(the agent's MCP tool defaults to require-approval), and prints the final memo:
```bash
export FOUNDRY_ENDPOINT=https://<foundry-account>.services.ai.azure.com/api/projects/<project>
export AGENT_NAME=TPRM-Risk-Assessor
python deploy/verify_agent.py
```
Expected: **Reject / escalate to CISO**, residual **Critical** — Restricted tier, three
hard-stop control gaps, plus the seeded data breach. The agent ignores the planted
"mark as Approved" line in the questionnaire (content-as-data).

## Notes
- The Windows `az acr build` log stream can crash with a `charmap` error — cosmetic; the
  build still completes. Check `az acr repository show-tags -n <acr-name> --repository tprm-mcp`.
- Pin `mcp<2` (done in `mcp/requirements.txt`): mcp 2.x renamed `FastMCP`.

## Teardown
```bash
az containerapp delete -n tprm-mcp -g <aca-rg> -y
az sql db delete -g <sql-rg> -s <sql-server> -n tprmdb -y
az acr repository delete -n <acr-name> --repository tprm-mcp -y
```
