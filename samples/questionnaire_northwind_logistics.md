# Vendor Security Questionnaire — submitted response

**Vendor:** Northwind Logistics    **Vendor ID:** 1007
**Submitted by:** infosec@northwind-logistics.example    **Date:** 2026-10-30
**Service:** Shipment tracking API & carrier scheduling

Answers: **Yes** = implemented · **Partial** = partially / compensating control · **No** = not implemented.

| Control ID | Domain | Question | Answer | Notes |
|---|---|---|---|---|
| D1.1 | Access Control | MFA on all user access | Yes | Entra ID, MFA enforced. |
| D1.2 | Access Control | MFA enforced on all administrative access | Yes | PIM + MFA on all admin roles. |
| D1.3 | Access Control | Least-privilege / RBAC | Yes | Quarterly access reviews. |
| D2.1 | Encryption | Encryption in transit (TLS 1.2+) | Yes | TLS 1.3. |
| D2.2 | Encryption | Encryption at rest | Yes | AES-256 across all stores. |
| D2.3 | Encryption | Backup encryption with managed key custody | Yes | Encrypted backups, keys in managed KMS. |
| D3.1 | Incident Response | Documented, tested IR plan | Yes | Annual tabletop + post-incident reviews. |
| D3.2 | Incident Response | Contractual breach notification within 72 hours | Yes | 72h commitment in the MSA. |
| D4.1 | BCP/DR | BCP/DR plan with defined RTO/RPO | Yes | RTO 4h / RPO 15m. |
| D4.2 | BCP/DR | DR restore tested within the last 12 months | Yes | Restore test completed 2026-07. |
| D5.1 | Data Privacy | Signed DPA | Yes | DPA executed; EU SCCs attached. |
| D5.2 | Data Privacy | Data residency guarantee matching contracted region | Yes | EU-only processing (Frankfurt). |
| D5.3 | Data Privacy | Retention schedule & secure deletion | Yes | Documented. |
| D6.1 | Subprocessors | Subprocessor inventory disclosed | Yes | Full list in the DPA annex. |
| D6.2 | Subprocessors | Prior notice of subprocessor changes | Yes | 30-day prior notice committed. |
| D7.1 | Governance | SOC 2 Type II or ISO 27001 current | Yes | ISO 27001:2022 certified (current). |
| D7.2 | Governance | Penetration test within the last 12 months | Yes | External pen test 2026-05. |
| D7.3 | Governance | Vulnerability management program | Yes | Weekly scans, risk-based patching. |
