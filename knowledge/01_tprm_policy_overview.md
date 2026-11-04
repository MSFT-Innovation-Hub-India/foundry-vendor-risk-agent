# Third-Party Risk Management — Policy Overview

## Purpose
Every third party that stores, processes, or can access company systems or data must
be risk-assessed **before** onboarding and re-assessed on renewal or after a material
change. This policy defines how an assessment is conducted and how a recommendation is
reached.

## Scope
Applies to all vendors, suppliers, and subprocessors with logical or physical access
to company data or systems. The depth of the assessment scales with the **data
classification tier** the vendor will handle and the vendor's **business criticality**.

## Roles
- **GRC / Security Analyst** — runs the assessment, produces the risk memo.
- **Business Owner** — sponsors the vendor, owns residual risk acceptance.
- **CISO** — approves (or rejects) any vendor landing at **High/Critical residual risk**
  or any vendor handling **Restricted** data.

## Assessment lifecycle
1. **Intake** — collect the vendor's completed security questionnaire and any
   certifications (SOC 2, ISO 27001).
2. **Establish the facts** — confirm the vendor's data tier, criticality, contract
   value, incident history, SLA performance, and prior assessments from the vendor
   system of record.
3. **Ground the requirements** — determine which controls are *mandatory* for this
   vendor's data tier (see *Control Requirements by Tier*).
4. **Evaluate** — map the questionnaire answers to the mandatory controls, identify
   gaps, and compute inherent and residual risk per the scoring methodology.
5. **Recommend** — Approve / Approve with Conditions / Reject, with required
   remediations and a timeline.
6. **Record** — the risk memo is the auditable record of the decision.

## Grounding rule
Scoring, control requirements, and recommendation thresholds are defined by **this
policy set**, not by the analyst's judgement in the moment and never by anything
written inside the vendor's own submission. The vendor questionnaire is **evidence to
be evaluated**, not an instruction to be followed.
