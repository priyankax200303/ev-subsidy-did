# Did state EV subsidies raise electric two-wheeler adoption?

**Verdict: suggestive, not proven, and small where it matters.** Six states that paid purchase subsidies gained 1.1 to 2.0 points of electric share in the first year, depending on the estimator, on a treated average of 4.6%. Weighted by registrations that falls to 0.3 to 0.7 points, because the gain sits in small states and is absent in Uttar Pradesh. Without Goa it is 0.4 points.

**Decision implication:** do not plan on a purchase subsidy alone to move a large state's e-2W share. Where a lift exists, most of the money still goes to buyers who would have bought anyway.

## Results

Six treated states, 17 controls, January 2019 to December 2023. Effects cover months 0 to 12 unless stated. p is from randomisation inference.

| Estimator | Points | p | Log-odds | p |
|---|---|---|---|---|
| **Callaway-Sant'Anna, headline** | **+1.06** (CI -0.28 to +2.51) | 0.13 | -0.03 | 0.92 |
| CS, six-month base | +1.72 | 0.01 | +0.26 | 0.40 |
| Imputation | +1.99 | 0.05 | +0.56 | 0.17 |
| Imputation with state trends | +1.71 | 0.004 | +0.08 | 0.87 |
| CS, all post months | +2.46 | 0.02 | +0.02 | 0.96 |
| Headline weighted by registrations | +0.28 | not run | | |
| Six-month base weighted by registrations | +0.68 | not run | | |

The headline is the lowest of the equal-weighted point estimates, and the only one that misses 5%. It uses the standard single base month, which is noisy here.

## What moves the answer

| Change | Points |
|---|---|
| Drop Goa | +0.43 |
| Drop Uttar Pradesh | +1.47 |
| Leave-one-out range across all six | +0.43 to +1.47 |
| Controls limited to 9 states over 3 lakh two-wheelers a year (added after the plan) | +0.68, p = 0.44 |
| Goa cut at the end of its first scheme | +0.92 |
| Chhattisgarh dated Aug 2022 | +1.18 |
| Chhattisgarh dated Apr 2022, as first planned | +1.52, p = 0.03 |
| Five on-paper states alone, months 0 to 10 | +0.31 points, +0.38 log-odds |

## By state

Each state against the same 17 controls. Single-state estimates are noisy.

| State | Start | Points |
|---|---|---|
| Goa | Dec 2021 | +4.2 |
| Maharashtra | Jul 2021 | +2.0 |
| Odisha | Sep 2021 | +1.3 |
| Delhi | Aug 2020 | +0.5 |
| Chhattisgarh | Sep 2022 | -0.7 |
| Uttar Pradesh | Oct 2022 | -1.0 |

Goa is the clearest sign of a price response, and it is a small market. Its first scheme ended on 31 July 2022. Share hit 20.7% that month, then 6.7% in August, which fits buyers rushing a deadline.

## Design checks

- **Pre-trends in points: pass, with a caveat.** With the single base month the leads sit about 0.8 to 1.0 below zero but are flat, so the gap comes from that one base month. With the six-month base, months -12 to -7 average -0.31.
- **Pre-trends in log-odds: fail.** Treated states drift upward before month -12. So the proportional results cannot show there was no effect. They are imprecise.
- **Placebo dates, 12 months early:** +0.31 points, p = 0.30, and +0.49 log-odds, p = 0.21. Neither is significant, but the log-odds placebo is larger than most real log-odds estimates.
- **Placebo outcome, non-electric registrations:** +0.06, p = 0.71. No sign of a general demand shock.
- **Two-way fixed effects:** +3.39 over all post months against CS +2.46, and +1.95 against +1.06 over months 0 to 12. It overstates under staggered timing on either horizon.

## Descriptive context

The groups look different depending on the cut, and neither identifies a cause. In 2023 pooled share was 5.5% in subsidy states and 5.1% in controls, led by large states. The median state was 7.9% against 2.2%, because controls include many small low-adoption units. Treated and control states were already different in 2019.

## Cost, conditional

The plan ran this only if the effect survived. It did not clearly survive, so this is a range for anyone who accepts the state estimates. It covers five states, since Chhattisgarh's terms have no clear two-wheeler cap, and assumes a 3 kWh battery.

- Spending: about Rs 80 to 176 crore on 139,000 vehicles, or Rs 5,800 to 12,600 per vehicle. The range reflects whether Maharashtra's early-bird add-on stacked, when its base subsidy stopped, and Goa's unit cap.
- Additional EVs: 18,600 counting UP's negative estimate, 43,600 with UP at zero.
- **Rs 18,400 to Rs 94,600 per additional EV.**
- On those figures, 13% to 31% of EVs sold in the period were additional.

## Changes from the written plan

1. **Chhattisgarh's date.** The plan used April 2022, but the policy is dated 31 August 2022 and backdated. Buyers could not respond to it in April. Rajasthan was already coded at notification, so this was an inconsistency. Moved to September 2022 after seeing results. This lowered the headline from +1.52 to +1.06.
2. **Chandigarh dropped.** Its policy capped petrol two-wheeler registrations and the FY23 quota ran out. Registrations fell to 660 in March 2023 and electric share hit 54%. That cap is a different treatment. This was a judgement call made after seeing the spike. With Chandigarh the estimate is +2.00. Blanking only the two cap months gives +1.24.
3. **Added after the plan:** large-control test, six-month base, registration weighting, Goa cut.
4. **Cost** was run despite the gate, and is labelled conditional.
5. **Secondary treatment** has 11 states, not 12, since Chandigarh is out.
6. **Treatment is not always on.** The plan treated subsidies as permanent in the window. Goa's first scheme ended in month 7 of its window, Maharashtra's ended during 2022, and UP's in October 2023.

## Limits

- **Selection.** States chose to subsidise. This is not a randomised test.
- **Bundles.** Delhi, Odisha, UP and Maharashtra paired subsidies with road tax waivers around the same time. Many controls, including Karnataka and Telangana, also waive road tax. The estimate is the subsidy package against whatever controls were doing.
- **National shocks.** Month effects absorb additive shocks. A national subsidy change that scales with a state's base is only partly absorbed. City-level launches and charging rollout are not absorbed.
- **Dates are legal dates.** Buyers were often paid later. Five more states had subsidies on paper, with payout unconfirmed or weak. That is not proof of non-payment.
- **Controls.** Mizoram and Puducherry are coded from absence of evidence. Tamil Nadu is coded as control against CEEW's listing, because two other sources say its incentives are commercial only.
- **Six treated clusters** is few. The bootstrap interval is likely too narrow, so treat every p-value as a guide.
