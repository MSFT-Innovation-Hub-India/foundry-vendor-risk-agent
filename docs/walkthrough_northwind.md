---
title: Walkthrough — Northwind Logistics vendor risk assessment (Approve)
description: Step-by-step trace of the AI vendor risk agent assessing Northwind Logistics — MCP calls, policy searches, sandbox scoring and an Approve verdict.
---

# Walkthrough — Northwind Logistics (V1007) → **Approve**

A step-by-step trace of the same agent procedure on the **clean** vendor, using the
**actual** sample data in this kit. Read it against
[`walkthrough_acme.md`](walkthrough_acme.md) (the **Reject** case): the stages are
identical — only the data differs, and that is what flips the outcome. It is the proof the
logic is driven by evidence, not hard-coded.

---

## The input (what the analyst sends)

> "Run a risk assessment on **Northwind Logistics** using the attached questionnaire."
> *(attach `samples/questionnaire_northwind_logistics.xlsx`, or paste the `.md`)*

Northwind's questionnaire answers **Yes** to all 18 controls, and there is **no** planted
instruction line.

---

## Stage 0 — Stage the questionnaire

**File write** saves the submission to the sandbox (e.g. `questionnaire.md`). No computation
yet.

---

## Stage 1 — Resolve the vendor & ground the rules

**MCP call:**

```
list_vendors(name_like="Northwind")
→ [{ "VendorId": 1007, "VendorName": "Northwind Logistics",
     "Industry": "Logistics", "Country": "Germany" }]
```

**Knowledge (vector) search** — the agent searches the same **policy library** to ground the
rules it applies (the tier's mandatory controls, the scoring methodology, the history
adjustments, the recommendation thresholds). Each hit becomes a `【source:…】` citation in the
memo. What the library contains, and how the agent writes these queries, is catalogued once in
**[`data_sources.md`](data_sources.md)** — here, note only that the tier-specific requirements
are pulled **after** Stage 2, once the tier (**Internal**) is known.

---

## Stage 2 — Establish the facts of record (MCP, read-only)

The **real seed data** for V1007:

```
get_vendor_profile(vendor_id=1007)
→ tier=Internal, criticality=Medium, processes_PII=No, residency=EU,
  annual_contract_value=$120,000, contract_status=Pending,
  service="Cloud hosting"

get_incident_history(vendor_id=1007)   → (no rows)
get_sla_breaches(vendor_id=1007)       → (no rows)

get_prior_assessments(vendor_id=1007)
→ 9002  2025-10-15  inherent Medium  residual Low  recommendation Approve

get_spend_history(vendor_id=1007)
→ 2024 $99,945 · 2025 $109,663 · 2026 $128,167
```

(What each profile field means and drives — tier, criticality, PII, residency, contract
value/status, service — is catalogued once in
[`data_sources.md`](data_sources.md#what-the-get_vendor_profile-fields-drive).)

Written to **`facts.json`**:

```json
{
  "vendor_id": 1007, "name": "Northwind Logistics",
  "tier": "Internal", "criticality": "Medium", "pii": false,
  "residency": "EU", "annual_contract_value": 120000, "contract_status": "Pending",
  "service_of_record": "Cloud hosting",
  "incidents": [],
  "sla_breaches": [],
  "prior_assessment": {"date": "2025-10-15", "inherent": "Medium", "residual": "Low", "recommendation": "Approve"},
  "spend": {"2024": 99945.19, "2025": 109663.27, "2026": 128167.28}
}
```

> **Spend note the agent should surface:** 2026 spend **$128,167 exceeds** the stated
> **$120,000** annual contract value — worth one line in *Facts of record* even though it
> does not change the risk score.

Tier is **Internal**, so the agent pulls the *Internal* requirements from
`03_control_requirements_by_tier.md` (a much shorter mandatory set than Restricted).

---

## Stage 3 — Extract the questionnaire (code written on the fly)

Bespoke Python → **`answers.csv`** (all Yes here):

```csv
domain,control,question,answer,score,notes
Access Control,D1.1,MFA on all user access,Yes,1.0,Entra ID MFA enforced.
Access Control,D1.2,MFA on administrative access,Yes,1.0,PIM + MFA on admin roles.
Access Control,D1.3,Least-privilege / RBAC,Yes,1.0,Quarterly access reviews.
Encryption,D2.1,Encryption in transit,Yes,1.0,TLS 1.3.
Encryption,D2.2,Encryption at rest,Yes,1.0,AES-256 across stores.
Encryption,D2.3,Backup encryption w/ managed keys,Yes,1.0,Keys in managed KMS.
Incident Response,D3.1,Documented, tested IR plan,Yes,1.0,Annual tabletop.
Incident Response,D3.2,Contractual 72h breach notification,Yes,1.0,72h in the MSA.
BCP/DR,D4.1,BCP/DR plan w/ RTO/RPO,Yes,1.0,RTO 4h / RPO 15m.
BCP/DR,D4.2,DR restore tested in last 12 months,Yes,1.0,Restore test 2026-07.
Data Privacy,D5.1,Signed DPA,Yes,1.0,DPA + EU SCCs.
Data Privacy,D5.2,Data residency matches region,Yes,1.0,EU-only (Frankfurt).
Data Privacy,D5.3,Retention & secure deletion,Yes,1.0,Documented.
Subprocessors,D6.1,Subprocessor inventory disclosed,Yes,1.0,Full list in DPA annex.
Subprocessors,D6.2,Prior notice of subprocessor changes,Yes,1.0,30-day notice.
Governance,D7.1,SOC 2 Type II / ISO 27001 current,Yes,1.0,ISO 27001:2022 current.
Governance,D7.2,Pen test in last 12 months,Yes,1.0,External pen test 2026-05.
Governance,D7.3,Vulnerability management program,Yes,1.0,Weekly scans.
```

---

## Stage 4 — Score (code written on the fly) + self-correct

### 4a. Inherent risk

| Factor | Value | Points |
|---|---|---|
| Data tier | Internal | 2 |
| Criticality | Medium | 2 |
| Annual contract value | $120,000 ($100k–$300k) | 2 |
| Processes PII | No | 0 |
| **Total** | | **6 → Medium** (4–6) |

### 4b. Control effectiveness — over **mandatory** controls only

For **Internal**, `03_…by_tier.md` makes only the baseline mandatory: **D1** least-privilege
access, **D2.1** encryption in transit, **D3.1** documented IR plan, and the **D7.1**
governance baseline (SOC 2 / ISO). That is **4 mandatory controls** — everything else
(MFA, encryption at rest, DR testing, subprocessor rules, pen testing…) is *informational*
at this tier. Northwind answered **Yes** to all four:

```
effectiveness = 4 / 4 = 1.00  → Strong ( ≥ 0.90 )
```

(The vendor also meets the above-tier controls, which is why the coverage radar is full —
but only the 4 mandatory ones enter the denominator.)

### 4c. Residual risk

- Inherent = **Medium**; effectiveness **Strong → down 1 band → Low**.

### 4d. History adjustments

`get_incident_history` and `get_sla_breaches` returned **no rows**, so **no adjustment
applies**. Residual stays **Low**.

### 4e. Hard stops / caps

Tier is **Internal**, not Restricted → **no hard stops apply**, and there is **no mandatory
control answered No**. So a plain **Approve** is permitted (unlike Restricted, which can
never be a plain Approve).

### 4f. Trend

Prior residual was **Low**; current residual is **Low** → the trend is **unchanged** (not
"improved").

### 4g. Verify-before-trust

Checks pass on the first run: mandatory count = 4 ✓, `0 ≤ 1.00 ≤ 1` ✓, bands valid ✓, no
gaps ✓. No self-correction loop needed.

---

## Stage 5 — Charts

Same three charts, rendered from the computed values: a **full** control-coverage radar
(vendor meets the target on every domain), a **gap-severity** chart that is **0.0 across all
domains** (axis pinned 0–1 so "no gaps" reads clearly), and a **residual trend** that is
flat **Low → Low**.

---

## Stage 6 — Assemble, publish, reply

Identical to the Acme flow: assemble the self-contained HTML (charts in-context with
interpretation), **POST** it to the report viewer, get a link, and reply in chat with a
short summary plus the link. On a clean Approve the memo still **enumerates the mandatory
controls checked** and shows the prior-assessment and spend facts — an Approve is as
auditable as a Reject.

---

## Sandbox files at a glance

Everything below is written inside the **ephemeral** sandbox and discarded when the run ends;
only the final report is published to the viewer.

| File | Written in | What it contains |
|---|---|---|
| `questionnaire.md` / `.xlsx` | Stage 0 | The vendor's submission exactly as received — the unstructured input. |
| `facts.json` | Stage 2 | The system-of-record facts from the MCP calls (profile, incidents, SLA breaches, prior assessment, spend) in one JSON the scoring code reads. |
| `answers.csv` | Stage 3 | The questionnaire parsed into one row per control: `domain, control, question, answer, score, notes`. |
| `score.py` | Stage 4 | The bespoke scoring code the agent writes and runs: inherent points, control effectiveness over the mandatory controls, residual band, history adjustments, hard stops, and the verify checks. |
| `control_coverage_radar.png`, `gap_severity_by_domain.png`, `residual_vs_prior_trend.png` | Stage 5 | The three charts, rendered from the computed values. |
| `report.html` | Stage 6 | The self-contained memo (charts embedded as base64) that is POSTed to the report viewer and served at the link. |

## The outcome

> **Approve** — residual **Low**. Inherent risk is Medium and strong mandatory-control
> coverage moves it down one band to Low; no incidents or SLA breaches, and no hard stops
> at the Internal tier. Trend unchanged (Low → Low).

Same procedure as Acme, opposite data, opposite verdict — which is the point.
