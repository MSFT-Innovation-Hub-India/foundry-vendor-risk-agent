# MCP tool contract — TPRM read-only database access

This is the **authoritative spec** for the MCP server the agent calls to reach the
Azure SQL database. The agent does **no** NL2SQL. It calls these bounded,
parameterized, read-only tools; the server owns the SQL (against the `vw*` views
only) and returns JSON rows.

> Governance principle: *vary the data, fix the logic.* The agent chooses the tool
> and the arguments; it never composes SQL. This keeps the DB access deterministic,
> injection-proof, and easy to audit in Traces.

## Connection / security posture (enforce on the server, not in the prompt)
- Connect with a **read-only, least-privilege** SQL login that can `SELECT` only on
  the five `vw*` views — not the base tables.
- Hard caps on every query: `SET LOCKOUT`/statement timeout (e.g. 15s) and a **row
  cap** (TOP 500) so a tool can never stream the whole table.
- Parameterized queries only (`?` / named params). Never string-concatenate args.
- No tool writes. There is intentionally no insert/update/delete surface.

## Tools

### 1. `list_vendors`
Resolve a name to a VendorId (use when the request names a vendor but gives no id).
- **Params:** `name_like` (string, required)
- **SQL:** `SELECT TOP 25 VendorId, VendorName, Industry, Country FROM dbo.vwVendorProfile WHERE VendorName LIKE '%' + ? + '%' ORDER BY VendorName`
- **Returns:** `[{VendorId, VendorName, Industry, Country}]`

### 2. `get_vendor_profile`
The core fact sheet: identity, criticality, data-access tier, PII flag, residency,
and the current/most-recent contract.
- **Params:** `vendor_id` (int, required)
- **SQL:** `SELECT * FROM dbo.vwVendorProfile WHERE VendorId = ?`
- **Returns:** one object with `VendorId, VendorName, Industry, Country, Criticality,
  OnboardingStatus, FirstEngagedDate, DataClassificationTier, ProcessesPII,
  DataResidency, SystemsAccessed, AnnualValueUSD, ContractStatus, ContractStart,
  ContractEnd, ServiceDescription`

### 3. `get_incident_history`
- **Params:** `vendor_id` (int, required), `since` (date `YYYY-MM-DD`, optional — default 36 months back)
- **SQL:** `SELECT TOP 500 IncidentId, IncidentDate, Severity, Category, Description, ResolvedDate FROM dbo.vwIncidentHistory WHERE VendorId = ? AND IncidentDate >= ? ORDER BY IncidentDate DESC`
- **Returns:** `[{IncidentId, IncidentDate, Severity, Category, Description, ResolvedDate}]`

### 4. `get_sla_breaches`
- **Params:** `vendor_id` (int, required), `window_months` (int, optional — default 24)
- **SQL:** `SELECT TOP 500 BreachId, BreachDate, SLAType, TargetValue, ActualValue, PenaltyAppliedUSD FROM dbo.vwSLABreaches WHERE VendorId = ? AND BreachDate >= DATEADD(month, -?, CAST(GETDATE() AS date)) ORDER BY BreachDate DESC`
- **Returns:** `[{BreachId, BreachDate, SLAType, TargetValue, ActualValue, PenaltyAppliedUSD}]`

### 5. `get_prior_assessments`
- **Params:** `vendor_id` (int, required)
- **SQL:** `SELECT AssessmentId, AssessmentDate, InherentRisk, ResidualRisk, Recommendation FROM dbo.vwPriorAssessments WHERE VendorId = ? ORDER BY AssessmentDate DESC`
- **Returns:** `[{AssessmentId, AssessmentDate, InherentRisk, ResidualRisk, Recommendation}]`

### 6. `get_spend_history`
- **Params:** `vendor_id` (int, required)
- **SQL:** `SELECT [Year], SpendUSD FROM dbo.vwSpendHistory WHERE VendorId = ? ORDER BY [Year]`
- **Returns:** `[{Year, SpendUSD}]`

## Why this is six tools and not one `run_sql`
The whole vendor-risk report needs a **known, bounded** set of facts per vendor.
Exposing `run_sql` would force the server to defend against injection, unbounded
scans, hallucinated columns and schema leakage — for zero benefit, because the
questions are not open-ended. If you later add a genuinely open-ended analytics
agent, give *that* agent a separate, sandboxed text-to-SQL tool; keep this one tight.
