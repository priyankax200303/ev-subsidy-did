# Analysis plan

Written after the panel and the policy table were built, before any treatment effect was estimated.

**Question.** Did state purchase subsidies raise the electric share of two-wheeler registrations, or were those states already moving faster?

**Outcome.** Electric two-wheelers as a percentage of all two-wheeler registrations, state by month.

**Window.** January 2019 to December 2023, 60 months. Before 2019 the share is close to zero everywhere. After 2023 the treatment stops being clean: Maharashtra's and UP's first spells had ended, Delhi's payments froze, and Bihar and Andhra Pradesh started.

**Sample.** States with at least 20,000 two-wheeler registrations in 2019. This removes seven small units. Meghalaya also has no confirmed start date.

**Treatment, primary.** The 7 states with evidence that money reached buyers, dated by the month the subsidy came into force. Treatment is treated as switched on for good inside the window.

**Comparison, primary.** The 17 states with no private e-2W purchase subsidy in the window. The 5 on-paper states are dropped from the primary run so they do not contaminate either side.

**Secondary treatment.** All 12 states, paid plus on paper.

**Main estimate.** Callaway-Sant'Anna ATT with never-treated comparison, aggregated by event time, reported over months 0 to 12 and over all post months.

**Also reported.** Two-way fixed effects, for comparison only. It is biased under staggered timing with growing effects.

**Pass or fail on pre-trends.** The design is credible only if the event study shows no drift across months -12 to -2. If it drifts in levels, the verdict has to say so, and the log-odds and state-trend versions decide what can be claimed.

**Robustness.**
1. Log-odds outcome, because national take-off is multiplicative and states with a higher base rise more in points.
2. State-specific linear trends.
3. Placebo dates 12 months early, on pre-treatment data only.
4. Randomisation inference, because 7 treated clusters is too few for clustered standard errors alone.
5. Leave-one-out on each treated state, plus dropping Karnataka and Tamil Nadu, home to the main e-2W makers.
6. Paid plus on-paper treatment.
7. Chhattisgarh alternative date.
8. Placebo outcome: log non-electric two-wheeler registrations.

**Cost.** Rupees per additional EV, only if the effect survives, using each state's rate and cap at an assumed 3 kWh battery. Stated as an assumption-driven range.

**Stated limits.** National FAME II changes and charging rollout overlap the policies. Month effects absorb the national part, but not city-level rollout by makers. Selection into subsidising is not random.

## Amendments after the plan

The plan above is left as written. Changes made later are listed in `POLICY_NOTE.md` under "Changes from the written plan". One statement above was wrong: not all first spells ran to the end of 2023. Goa's first scheme ended in July 2022, Maharashtra's two-wheeler subsidy stopped during 2022, and UP's ended in October 2023.
