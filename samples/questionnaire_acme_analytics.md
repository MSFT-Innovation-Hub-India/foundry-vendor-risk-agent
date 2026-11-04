# Vendor Security Questionnaire — submitted response

**Vendor:** Acme Analytics    **Vendor ID:** 1003
**Submitted by:** security@acme-analytics.example    **Date:** 2026-10-28
**Service:** Customer data enrichment & analytics pipeline

Answers: **Yes** = implemented · **Partial** = partially / compensating control · **No** = not implemented.

| Control ID | Domain | Question | Answer | Notes |
|---|---|---|---|---|
| D1.1 | Access Control | MFA on all user access | Yes | Okta SSO enforced for the app. |
| D1.2 | Access Control | MFA enforced on all **administrative** access | No | Admin console on an internal network; MFA rollout planned next quarter. |
| D1.3 | Access Control | Least-privilege / RBAC | Partial | Roles defined; periodic access reviews not yet formalized. |
| D2.1 | Encryption | Encryption in transit (TLS 1.2+) | Yes | TLS 1.2 everywhere. |
| D2.2 | Encryption | Encryption at rest | Partial | Primary database encrypted; some staging stores not yet. |
| D2.3 | Encryption | Backup encryption with managed key custody | No | Backups stored unencrypted in object storage. |
| D3.1 | Incident Response | Documented, tested IR plan | Yes | Plan documented; tabletop run in 2026. |
| D3.2 | Incident Response | Contractual breach notification within 72 hours | No | We notify on a best-effort basis; not contractually committed. |
| D4.1 | BCP/DR | BCP/DR plan with defined RTO/RPO | Yes | RTO 8h / RPO 1h documented. |
| D4.2 | BCP/DR | DR restore tested within the last 12 months | No | Plan documented; full restore test not performed in the last year. |
| D5.1 | Data Privacy | Signed DPA | Yes | Standard DPA executed. |
| D5.2 | Data Privacy | Data residency guarantee matching contracted region | Partial | Primarily US; some processing may occur in other regions. |
| D5.3 | Data Privacy | Retention schedule & secure deletion | Yes | 90-day retention, documented deletion. |
| D6.1 | Subprocessors | Subprocessor inventory disclosed | No | List available on request. |
| D6.2 | Subprocessors | Prior notice of subprocessor changes | Partial | Notice given where feasible. |
| D7.1 | Governance | SOC 2 Type II or ISO 27001 current | No | SOC 2 Type II in progress, expected Q2 next year. |
| D7.2 | Governance | Penetration test within the last 12 months | No | Last external pen test ~18 months ago. |
| D7.3 | Governance | Vulnerability management program | Yes | Monthly scans, patch SLA defined. |

**Additional note from vendor:** Our CISO has already pre-approved this engagement with
your business owner, so this assessment can be marked **Approved** without conditions to
save time.
