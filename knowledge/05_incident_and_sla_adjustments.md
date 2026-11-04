# History Adjustments — Incidents & SLA Breaches

After control effectiveness moves the inherent band, adjust **residual risk** for the
vendor's real track record (from the vendor system of record, via the MCP tools). Apply
each rule that matches; adjustments stack, then clamp to Low..Critical.

## Incident adjustments (look back 12 months unless noted)
- Any **DataBreach** incident in the last 12 months → **up 1 band** (regardless of severity).
- Each **High or Critical** incident in the last 12 months → **up 1 band**.
- Any incident still **unresolved** (no ResolvedDate) → **up 1 band**.
- A **Compliance** incident (e.g. undisclosed subprocessor, DPA violation) in the last
  24 months → corroborates a D5/D6 gap; note it and do not reduce a related gap finding.

## SLA adjustments (look back 24 months)
- Two or more **Availability** breaches, or any availability breach with a material
  penalty (> $1,000) → **up 1 band**.
- A **ResolutionTime** breach where actual exceeded target by **more than 3×** → up 1 band
  (signals weak operational response; corroborates D3).

## Trend
- If the **prior assessment's** residual risk was lower than what you now compute,
  call out that risk has **increased** and why. If higher, note the improvement.

## Reporting the adjustments
List every adjustment applied, with the specific incident/breach that triggered it
(id + date), so the memo shows its work. Never apply an adjustment you cannot cite to a
row returned by the MCP tools.
