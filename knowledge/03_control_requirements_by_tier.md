# Control Requirements by Data Classification Tier

Which controls are **mandatory** depends on the highest data classification tier the
vendor will handle (from the vendor system of record). Mandatory controls are the ones
whose gaps matter; non-mandatory controls are informational for that tier.

Tiers, lowest to highest sensitivity: **Public → Internal → Confidential → Restricted**.
Requirements are cumulative (Restricted includes everything below it).

## Public
- D7 governance baseline only (a current SOC 2 **or** ISO 27001, or a documented
  security program). No other mandatory controls.

## Internal (adds)
- **D1** Access control with least-privilege.
- **D2** Encryption **in transit**.
- **D3** Documented incident-response plan.

## Confidential (adds)
- **D1** **MFA** on all access to company data.
- **D2** Encryption **at rest**.
- **D4** BCP/DR plan with defined RTO/RPO.
- **D5** Signed **DPA**; documented retention & secure deletion.
- **D6** Subprocessor inventory **disclosed**.
- **D7** **SOC 2 Type II or ISO 27001 current** (not merely "in progress").

## Restricted (adds — the strict tier)
- **D1** MFA on **all administrative** access specifically, enforced (no exceptions).
- **D2** **Backup encryption** with managed key custody/rotation.
- **D3** Contractual **breach-notification within 72 hours** to the company.
- **D4** DR **restore-tested within the last 12 months** (a plan alone is insufficient).
- **D5** **Data residency** guarantee matching the contracted region.
- **D6** **No undisclosed subprocessors**; prior-notice of changes contractually bound.
- **D7** **Penetration test within the last 12 months**.

## Hard stops (Restricted only)
For Restricted data, a **gap (No)** on any of the following cannot be waived at analyst
level and forces at most a **Reject / escalate-to-CISO** outcome:
- MFA on administrative access (D1),
- Encryption at rest **and** backup encryption (D2),
- 72-hour breach-notification commitment (D3).
