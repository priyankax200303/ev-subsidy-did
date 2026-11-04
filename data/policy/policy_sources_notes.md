# State e-2W purchase subsidy table: source notes

Companion to `state_policy_table.csv`. As of 2026-11-04. All values came from pages fetched while compiling the table. The shell could not reach source sites, so PDFs were read through WebFetch text extraction, not by eye. Image-only tables were unreadable.

## Conventions

- **Spell split:** a new row only where the effective date of a change is confirmed. Chandigarh's 2025 rate rise has no confirmed date, so it stays in one row.
- **`subsidy_end` is blank** if the spell is still running or the end is unknown. Scheduled future ends are in `notes`.
- **`notified_date` is blank** where only a cabinet or announcement date exists (Bihar 2023 and 2026, Gujarat 2021, Meghalaya 2021).
- **`amount_per_kwh_inr` is blank** for percentage or lump-sum schemes. The rate is in `notes`.
- **`notes` opens with a STATUS token.** Use it to separate legal treatment from money actually reaching buyers:
  - `DISBURSAL_EVIDENCED`, `DISBURSAL_EVIDENCED_VIA_OEM`: a source shows buyers paid, or the discount passed on by the OEM.
  - `ON_PAPER_DISBURSAL_UNCONFIRMED`: legally in force, no payment evidence found. This is not proof of non-payment.
  - `ON_PAPER_DISBURSAL_WEAK`: sources show little or no money moving.
  - `ON_PAPER_THEN_DELAYED`, `RETROACTIVE_DISBURSAL_STALLED`, `LEGAL_EXTENSION_PAYMENT_FROZEN`: a legal window where buyers could not rely on payment at purchase.
  - `TARGETED_SUBSET_STUDENTS`: not a general scheme.
  - `NO_PRIVATE_2W_PURCHASE_SUBSIDY`: positive evidence of none. `NO_SUBSIDY_FOUND`: absence of evidence only. `DRAFT_ONLY`: never confirmed notified.
- **`confidence`** rates the dates and terms, not implementation. Implementation is in STATUS.
- **`source_type`** describes the document. `official_gazette` is used for government text hosted by a third party (Rajasthan on rajras.in, Punjab on Simpliance, AP on apchambers.in), and the host is named in `notes`.

## Prior-attempt CSV (`Dim_State_Policy.csv`): corrections

Treat it as unreliable. Its status and dates mostly copy CEEW at month level, as first-of-month dates.

| State | Lead says | Finding |
|---|---|---|
| Tamil Nadu | e-2W subsidy from 2023-02-01 | Commercial e-2W only |
| Punjab, Jharkhand, Bihar | no policy | All three have notified purchase subsidies |
| Andhra Pradesh | no incentive | 5% from G.O.88, 2024-12-11 |
| Odisha | start 2021-02-01, road tax buses only | Resolution 2021-09-01, road tax for all BOVs |
| Rajasthan | 2022-08-01, no road tax | 2022-09-01, MV tax exempt, plus a missing 2021 spell |
| Maharashtra | single 2021-09-01 start | GR July 2021, plus 2018 and 2025 spells |
| Gujarat, Goa, Delhi, UP | no end dates to 2026 | Ends and later spells are in the table |
| Chandigarh, Ladakh | no tax waivers | Both have road tax waivers |

## Conflicts between sources

- **CEEW matrix vs primary documents.** The fetched CEEW text is flattened and misaligned. Odisha Feb 2021 conflicts with the official Resolution of 2021-09-01. Assam Jul 2021 conflicts with 2021-09-04. Maharashtra Sep 2021 conflicts with the GR of July 2021. Manipur's "30%, 1,000" is a tax waiver. Tamil Nadu's figures match the commercial E2W line. Punjab shows 50,000 units against EVreporter's 1,00,000. The four-pager text was too scrambled to use except as a pointer.
- **Tamil Nadu.** CEEW lists a 2W incentive and also lists TN under "no consumer incentives". Autocar Pro and ITDP say demand incentives are for commercial vehicles only. e-vehicleinfo's table says commercial E2W. The policy PDF was not readable.
- **Delhi lapse timing.** Inc42 says the policy expired 2025-01-01. Autocar Pro and Outlook Business (Sept 2025) say Aug 2023. Outlook Business says subsidies were pending since 2024-01-01. The table uses Aug 2023 as nominal expiry and 2023-12-31 as an inferred split.
- **Maharashtra 2021 end.** The GR runs to 2025-03-31. Press says withdrawn by mid-2022 with no order cited. Autocar Pro (Oct 2026) attributes it to the 1 lakh ceiling being used up.
- **Gujarat students.** Vibes of India says discontinued (Mar 2022). PTI (Sep 2024) describes it as live.
- **Gujarat 2019.** No fetched page supports a 2019 student scheme. Sources show FY2015-16 for Rs 10,000 and Sept 2020 for Rs 12,000.
- **Rajasthan eligibility.** Drishti says purchases from 2022-01-01. Three other sources say 2022-09-01.
- **UP extension.** Press says the subsidy was extended to 2027. The official FAQ, updated 2026-11-04, still shows only the Oct 2022 to Oct 2023 window, and bolt.earth says it ended Oct 2023.
- **UP road tax.** Autocar Pro (2025-10-16) says it lapsed. Later reports show a Made-in-UP-only continuation to 2027-10-13.
- **Bihar 2023 amounts.** Four different descriptions (see row).
- **Chandigarh.** Fourth amendment dated 24 Sep (TeamLease) vs 25 Sep (press). Rate reported as Rs 10,000/kWh after Aug 2025, while Newsbytes still says Rs 5,000/kWh.
- **Ladakh cap.** CEEW Rs 15,000; official note Rs 30,000 at the 20% tier. Unit count 28 vs 35.
- **Jharkhand notification date.** 6, 7 or 19 Oct 2022.
- **Himachal notification date.** 10 or 20 Jan 2022.
- **MP notification date.** 27 or 29 Mar 2025.
- **Haryana.** Revolt blog's Rs 5,000/kWh claim is contradicted by the official scheme. meraev state pages mostly cover cars, so they were used only as weak negatives.

## Could not confirm

- **Official texts not read:** Delhi 2020 policy, Maharashtra 2018 and 2025 GRs, Tamil Nadu 2023, Jharkhand 2022, Bihar 2023 and 2026, Punjab 2023, Chhattisgarh 2022, Meghalaya gazette notice.
- **Dates:** Meghalaya 2021 gazette date; Bihar gazette dates; Gujarat GR number and date; exact date Maharashtra's 2W incentive stopped; UP subsidy status from 2023-10-14 to 2024-07-15; effective date of Chandigarh's 2025 revision; J&K 2026 and Meghalaya 2026 start dates; Assam after the 5-year term (about Sep 2026); end of Gujarat's student scheme.
- **Disbursal:** no evidence either way for Punjab, Jharkhand, Ladakh, Maharashtra 2018 and 2025, Bihar 2023, Gujarat 2021, or actual 2W payouts in Rajasthan.
- **Road tax:** extensions in Odisha after 2025-12-31 and West Bengal after 2025-03-31. Start dates for Karnataka and Tamil Nadu pre-2023 waivers are not established.
- **Unknown or negative-only states:** Nagaland, Sikkim, DNHDD, Mizoram, Puducherry rest on search absence and CEEW omission. Lakshadweep's draft attachment was not read.
- **Failed fetches:** MAIT Delhi PDF, Moneylife, Gujarati Zee News, Statesman UP Oct 2027, ICCT Maharashtra fact sheet, New Kerala MP headline, BEE Sikkim and Lakshadweep PDFs, Jharkhand portal PDF (binary), coezet TN PDF.

## For the DiD design (data facts only)

- **Retroactive windows:** Goa relaunch (2024 notice covers from 2022-08-01), Rajasthan 2021 (from 2021-04-01), Maharashtra 2025 (from 2025-04-01), Chhattisgarh (possibly from 2022-04-01), Delhi 2024 extension (from 2024-01-01).
- **Claim access later than eligibility:** Odisha portal 2022-04-01, UP portal 2023-07-19, Assam guidelines 2022-01-29, Meghalaya portal 2025-11-18.
- **Waivers often move with subsidies.** Road tax dates differ in several states, for example Delhi 2020-10-10, Chandigarh 2023-03-18.
- **Other policy shifts in the window:** Chandigarh's ICE 2W registration quotas from 2023, and PM E-DRIVE's reported 2W end on 2026-07-31.
