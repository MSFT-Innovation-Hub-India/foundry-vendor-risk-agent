# Risk Scoring Methodology

Risk is computed in three steps: **inherent risk** (how much is at stake), **control
effectiveness** (how well the vendor mitigates it), and **residual risk** (what remains,
after adjustments for history). All figures must be computed from the data — never
estimated.

## 1. Inherent risk
Score each factor, sum, then band.

| Factor | Points |
|--------|--------|
| Data tier | Public 1 · Internal 2 · Confidential 3 · Restricted 4 |
| Criticality | Low 1 · Medium 2 · High 3 |
| Annual contract value | < $100k: 1 · $100k–$300k: 2 · > $300k: 3 |
| Processes PII | No 0 · Yes 1 |

**Inherent band** by total points (max 11): `<=3 Low · 4–6 Medium · 7–9 High · >=10 Critical`.

## 2. Control effectiveness
Consider only the controls **mandatory for the vendor's tier** (see *Control
Requirements by Tier*). For those controls:

```
effectiveness = sum(answer_score) / count(mandatory_controls)
# answer_score: Yes=1.0, Partial=0.5, No=0.0
```

**Effectiveness band:** `>=0.90 Strong · 0.70–0.89 Adequate · 0.50–0.69 Weak · <0.50 Poor`.

## 3. Residual risk
Start from inherent, then move it by control effectiveness:

| Effectiveness | Move inherent band by |
|---------------|-----------------------|
| Strong | down 1 band |
| Adequate | no change |
| Weak | up 1 band |
| Poor | up 2 bands |

Then apply **history adjustments** (next doc) and the **hard stops** from the tier
requirements. Residual bands are the same four: Low / Medium / High / Critical (clamp
at Low and Critical).

## Control checks the analysis must satisfy (verify in code before trusting output)
- Mandatory-control count matches the tier definition exactly.
- `0 <= effectiveness <= 1`; no NaN (a tier with zero mandatory controls = Strong by
  convention, effectiveness reported as N/A).
- Every band is one of the four allowed values.
- The gap list and the effectiveness denominator are consistent (gaps ⊆ mandatory).
