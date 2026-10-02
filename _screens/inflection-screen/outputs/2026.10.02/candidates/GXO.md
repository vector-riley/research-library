GXO | score 9/10 | Archetype holds: external CEO plus new CFO, COO and Chairman, CEO-quantified EBIT gap to peers (3.5% vs above 6%), and FY2027 consensus EBITDA up only 0.4% in 12 months; C is 2 not 3 because no target year until the 2026-11-16 Investor Day.

- "we are at a 3.5%-4% EBIT margin business right now. We really deserve to be above six, and we will share more details on November 16th at the Investor Day in terms of our path to achieve that." Patrick Kelleher, CEO, GXO Q2 2026 Earnings Call, 2026-08-05, document_id 129356
- "We're a 3.5% EBIT business. Our good peers are 6% or better." Patrick Kelleher, CEO, Jefferies Global Industrials Conference 2026, 2026-09-09, document_id 219277
- "If you look into 2026 onwards, our guidance implies in 2026 an EBITDA margin expansion around 20 basis points." Baris Oran, CFO, GXO Q4 2025 Earnings Call, 2026-02-11, document_id 140565 (same call, Kelleher: "at or better than our peer group")

Gap math: 3.5% to 6.0% EBIT is +250 bps; consensus EBITDA margin goes 6.69% (FY2025A) to 7.47% (FY2028), +78 bps, so the street models about 172 bps less than the CEO's floor (cross-metric, assumes D&A/revenue flat); hitting it adds about 35% to FY2027 consensus EBITDA ($1,042M). 12-month FY2027 EBITDA revision +0.39% (Baba revisions), so D=2.

Open questions:
1. What target year and EBITDA-basis level will the 2026-11-16 Investor Day attach to "above six" EBIT?
2. Q2 2026 margin was flat YoY (6.4%) despite Wincanton synergies; how much of the $60M run rate (end 2026) is reinvested in vertical and AI spend?
3. Does consensus FY2028 margin (7.47%) move after the Investor Day, or does the street wait for delivery?

## Calibration notes
- Easy: quant block (one data_comps call fills 8 of 10 fields), catalyst events (form-8k item5_02.personnelChanges gives name, effectiveDate, background, so external_hire is a one-glance call), consensus margins via data_financials summary plus data_compute.
- Trap: data_comps `ebitda_margin` is the forward-FY consensus margin (equals FY2027 EBITDA/revenue), not LTM; compute LTM from the four latest quarterly actuals in data_financials. Also ev_ebitda_fy uses current_fy=2027.
- Hard: margin_framing holds one metric, but GXO framed the level in EBIT (3.5% to above 6%) and the annual rate in EBITDA (20 bps for 2026); add a `metric_basis_note` and let street gap fields carry an `assumption` string, else gap_bps_vs_target stays null whenever the target is EBIT and consensus is EBITDA.
- Hard: Wincanton close date not in the 8-K tool (UK scheme, items 2.01/1.01 and a text query both returned 0); acquisition effective dates for foreign targets need the 10-K or a transcript. The Aug 2026 8-K EX-99.1 (129255) was not reached by doc_types ["8-K","Investor Presentation"] with fiscal_year 2026; fetch by id instead.
- data_guidance `targets` is useful (it surfaced the peer-group and $60M quotes with document_ids) but mislabels field_keys (peer-parity margin filed as lt_gross_margin_target); trust statement and verbatim_quote, not field_key. `current.items` has no low/high for the margin guide.
- Fastest phrasings: hybrid (default) "margin at or better than our peer group" returned the Q4 call, Q2 2026 and Jefferies EBIT-level quotes in one call; hybrid "EBITDA margin expansion basis points 2026 peers" with fiscal_year=2026 found quarterly margin YoY lines. Lexical "basis points of margin expansion" without fiscal_year returned mostly 2021 to 2024 noise; always pair lexical with fiscal_year.
- Rubric: the archetype scores C=2 on a strict read (dated rate stated once; level stated twice but undated). Either accept 9/10 as archetype-level or let C=3 cover "quantified level repeated by CEO with a promised dated plan"; decide before grading others.
