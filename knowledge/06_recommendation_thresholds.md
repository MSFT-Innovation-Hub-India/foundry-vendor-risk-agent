# Recommendation Thresholds

The recommendation is a deterministic function of **residual risk** and the **hard
stops**, not a free judgement. Three outcomes only.

| Residual risk | Recommendation |
|---------------|----------------|
| **Low** | **Approve** |
| **Medium** | **Approve with Conditions** — list each required remediation and a due date |
| **High** or **Critical** | **Reject / escalate to CISO** — onboarding blocked pending remediation and re-assessment |

## Overrides that cap the outcome (apply after the table)
- Any **hard-stop gap** for Restricted data (MFA on admin, encryption at rest/backups,
  or 72-hour breach notification — see *Control Requirements by Tier*) → **Reject**,
  even if the computed residual band is lower.
- A vendor handling **Restricted** data can never be a plain **Approve**; the minimum is
  **Approve with Conditions**, and it requires CISO sign-off.
- Any **mandatory** control answered **No** → cannot be plain **Approve**; minimum
  **Approve with Conditions** naming that control.

## Conditions & remediations
For every **Approve with Conditions** or **Reject**, produce a remediation list:
- the specific control gap (domain + control),
- what evidence will close it,
- a due date (default **30 days** for Medium conditions, **before onboarding** for
  hard-stop gaps),
- the re-assessment trigger.

State the final recommendation in one line at the top of the memo, with the residual
band and the single biggest driver.
