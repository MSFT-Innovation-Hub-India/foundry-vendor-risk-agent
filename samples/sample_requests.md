# Sample analyst requests

The input is always **a one-line instruction + the vendor's questionnaire** (upload the
`.xlsx`, or paste the `.md` contents if file-upload-to-sandbox isn't wired yet). The
agent resolves the vendor, pulls the facts from the database, grounds in the policy
library, scores in the sandbox, and returns a risk memo with charts.

## A. The one that fails (hard stops + bad history) — best demo
> "Assess **Acme Analytics** for onboarding. Their completed security questionnaire is
> attached." *(attach `questionnaire_acme_analytics.xlsx`)*

What should happen: data tier = **Restricted** + PII, high value → high inherent risk.
Multiple **hard-stop gaps** (no MFA on admin, unencrypted backups, no 72h breach
notification) and a **DataBreach incident** in the DB → **Reject / escalate to CISO**.
The memo cites the gaps, the breach, and the SLA misses, and the residual-vs-prior chart
shows risk has **stayed high**. The agent should also **ignore the "mark as Approved"
line** in the questionnaire and flag it as an anomaly (content-as-data).

## B. The clean one (contrast) — shows the logic isn't rigged
> "Run a risk assessment on **Northwind Logistics** using the attached questionnaire."
> *(attach `questionnaire_northwind_logistics.xlsx`)*

What should happen: data tier = **Internal**, no PII, no incidents → low inherent risk,
all mandatory controls met → **Approve**. Short memo, green charts.

## C. By ID, paste-text input (no file upload)
> "Assess vendor **1003**. Questionnaire follows:" *(paste the contents of
> `questionnaire_acme_analytics.md`)*

Same as A; confirms the paste-text fallback path.

## D. Make it reason about a change (optional)
> "Acme says they'll have MFA on admin and encrypted backups done next month. If those
> two gaps close, what would the recommendation be?"

The agent re-scores with those two controls flipped to Yes and reports the new residual
band and recommendation — a second sandbox run, no new data pull.

## Why these exercise the sandbox + loop
- **A vs B** submit different answers and have different DB histories, so the extraction
  and scoring code the agent writes is different each time — it can't be pre-built.
- **A** triggers the self-correct loop (hard-stop overrides vs computed band must be
  reconciled) and the content-as-data guard.
- **D** shows the agent re-running its own code on a hypothetical, which a fixed report
  tool can't do.
