---
title: Data sources — vendor database and TPRM policy library
description: The two data sources the Foundry vendor risk agent uses — the Azure SQL vendor database (via MCP) and the TPRM policy library (vector search).
---

# Data sources — the vendor database and the policy library

The agent draws on two sources, the same for every vendor. This doc describes what each
**contains** and how the agent **uses** it. The per-scenario walkthroughs
([Acme](walkthrough_acme.md), [Northwind](walkthrough_northwind.md)) don't repeat this —
they only show the specific rows retrieved for their vendor.

---

## 1. Vendor database (read-only, via MCP)

The system of record for vendor facts. The agent **never writes SQL**; it reads bounded,
parameterized views through six MCP tools (full spec:
[`../mcp/tool_contract.md`](https://github.com/MSFT-Innovation-Hub-India/foundry-vendor-risk-agent/blob/main/mcp/tool_contract.md)).

| MCP tool | Returns | Used for |
|---|---|---|
| `list_vendors` | vendor id / name / industry / country matching a name | resolve the vendor named in the request to an id |
| `get_vendor_profile` | tier, criticality, PII, residency, contract value + status, service | the core facts that set inherent risk and the mandatory-control set |
| `get_incident_history` | security / compliance incidents (date, severity, category, resolution) | history adjustments (breach, high severity, compliance) |
| `get_sla_breaches` | availability / resolution-time breaches (target, actual, penalty) | history adjustments (operational track record) |
| `get_prior_assessments` | prior inherent / residual band + recommendation | the trend — did risk move since last time? |
| `get_spend_history` | annual spend per year | context (exposure; spend vs contract value) |

### What the `get_vendor_profile` fields drive

| Field | Significance |
|---|---|
| **tier** (data classification) | Highest sensitivity of data the vendor will handle. The **most consequential field**: it sets inherent-risk points, **which controls are mandatory**, and **whether hard stops apply**. |
| **criticality** | How badly a vendor failure would hurt the business. Inherent-risk points. |
| **processes_PII** | Whether personal data is in scope. Inherent-risk point + regulatory weight. |
| **residency** | Where data is processed; checked against the contracted region (control D5.2). |
| **annual_contract_value** | Financial exposure / blast radius. Inherent-risk points. |
| **contract_status** | Engagement lifecycle. `Pending` = prospective onboarding, i.e. a pre-onboarding gate — context, not a scoring input. |
| **service** | What the vendor does, per the system of record. Context, and cross-checked against the questionnaire's stated service to catch mismatches. |

The point values for tier / criticality / contract value / PII are defined in
[`../knowledge/04_risk_scoring_methodology.md`](https://github.com/MSFT-Innovation-Hub-India/foundry-vendor-risk-agent/blob/main/knowledge/04_risk_scoring_methodology.md).

---

## 2. Policy library (the Knowledge / vector source)

Seven Markdown docs loaded into the agent's **Knowledge (vector) source**. The agent searches
them to **ground every rule it applies**, and each search hit is surfaced in the memo as a
`【source:…】` citation — which is why memos reference names like `04_risk_scoring_methodology.md`.

| Document | What it's about | How the agent uses it |
|---|---|---|
| `01_tprm_policy_overview.md` | Program overview: purpose, scope, the assess → decide flow | general framing of the task |
| `02_control_domains.md` | The seven control domains D1–D7 and what each covers | map the questionnaire's answers onto domains |
| `03_control_requirements_by_tier.md` | Which controls are **mandatory** per data tier, and the Restricted **hard stops** | pick the mandatory-control set and hard-stop gates for this vendor's tier |
| `04_risk_scoring_methodology.md` | Inherent-risk points, the effectiveness formula, residual banding | compute inherent, effectiveness, and residual |
| `05_incident_and_sla_adjustments.md` | How incidents and SLA breaches move residual risk | apply history adjustments, each cited to a DB row |
| `06_recommendation_thresholds.md` | Residual band → recommendation, plus the override caps | turn the residual band into Approve / Approve-with-Conditions / Reject |
| `07_report_standards.md` | Memo structure, required charts, tone and integrity rules | assemble the report |

### How the agent forms its searches

The agent is **not** given query strings — it writes them itself. Its instructions name only
the *topics* to ground (control domains, tier requirements, scoring methodology, history
adjustments, thresholds, report standards); the model turns each topic into a natural-language
query and **specializes it to the case** (e.g. once the tier is known, it searches for *that
tier's* mandatory controls and hard stops). The query is embedded and matched **semantically**
against the chunked docs, so it needn't match any filename or wording — the document that comes
back is the match **result**, and also the citation. The number and wording of searches vary
from run to run. This is why the policy lives in a vector store rather than the prompt: the
agent pulls focused slices per step instead of carrying all seven docs in context.
