# Control Domains

Assessments are organized into seven control domains. The vendor questionnaire is
structured into the same seven sections, so each questionnaire section maps to exactly
one domain. Each control is answered **Yes** (implemented), **Partial** (partially /
compensating control), or **No** (not implemented), with notes.

| # | Domain | Covers |
|---|--------|--------|
| D1 | **Access Control & Authentication** | MFA, least-privilege, admin-access controls, joiner/mover/leaver, session management |
| D2 | **Encryption & Key Management** | Encryption in transit, encryption at rest, backup encryption, key custody/rotation |
| D3 | **Incident Response & Breach Notification** | IR plan, tested, breach-notification commitment and timeline to customer |
| D4 | **Business Continuity & DR** | BCP/DR plan, RTO/RPO defined, backups taken and **restore-tested**, failover |
| D5 | **Data Privacy & Protection** | DPA in place, data residency, retention & secure deletion, data-subject request handling |
| D6 | **Subprocessor & Supply-Chain** | Subprocessor inventory disclosed, flow-down of obligations, prior-notice of changes |
| D7 | **Security Governance & Certifications** | SOC 2 Type II or ISO 27001 current, annual penetration test, vulnerability management |

## Scoring an answer
- **Yes** = control met (effectiveness 1.0)
- **Partial** = control partially met / compensating control present (effectiveness 0.5)
- **No** = control gap (effectiveness 0.0)

A control's weight depends on whether it is **mandatory** for the vendor's data tier
(see *Control Requirements by Tier*). Gaps on mandatory controls drive residual risk
and can cap the recommendation regardless of the overall score.
