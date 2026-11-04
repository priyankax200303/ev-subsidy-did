# Data quality log

| Issue | What was found | What was done |
|---|---|---|
| No downloadable panel | Public copies stop in Jan 2024 and have no all-fuel denominator | Captured 20 tables directly from the Vahan dashboard on 2026-11-04 with `scripts/capture_vahan.js` |
| Filters silently ignored | The main Refresh ignores side-panel filters. The side Refresh ignores the year. First pass returned all vehicles, then 2023 repeated | Caught from totals and the table heading. Both refreshes now run in order, and each table's year was checked against its heading |
| Row totals | Every state row was summed against the site's total column | 0 mismatches |
| Independent check | Compared with a separate public Vahan copy from early 2024, 2,849 state-months | Correlation 0.99998, totals within 0.24%. 81% of cells match exactly. Vahan revises past months |
| November 2026 | Four days of data | Dropped. Panel ends October 2026 |
| States missing from electric tables | A state with no EVs in a year has no row | Filled with zero |
| Zero denominators | J&K May 2020, Ladakh twice | Share left blank, not zero |
| April and May 2020 | Lockdown months have tiny counts, for example Tamil Nadu 4 in April 2020 | Kept. Month effects absorb the national part. A six-month base was tested |
| Small units | 7 units under 20,000 two-wheelers a year | Excluded by the plan |
| Chandigarh | The FY23 cap on non-electric two-wheelers ran out, collapsing registrations in Feb and Mar 2023 ([Outlook Business](https://www.outlookbusiness.com/news/customers-in-a-fix-due-to-ban-on-registration-of-non-electric-2-wheelers-for-fy23-in-chandigarh-news-263216), [Business Standard](https://bsppd.business-standard.com/amp/article/current-affairs/ban-on-non-electric-2-wheeler-registration-in-chandigarh-put-buyers-in-fix-123021800505_1.html)) | Dropped from the headline. Reported with the state in and with the two months blanked |
| Single-month base | Standard CS base month is noisy for a seasonal series | Six-month base reported in the note: +1.72 points |
| Chhattisgarh date | Policy dated 2022-08-31 and backdated to April. Plan had used April | Moved to September 2022, first full month. Alternatives reported |
| Policy dates | A prior public table was wrong for several states | Rebuilt from sources. See `data/policy/policy_sources_notes.md` |
