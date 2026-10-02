# What to build into Baba so the inflection screen gets cheaper and better

Written 2026-10-02 after running the GXO-style inflection screen on 23 names with Opus subagents. Each item names the
gap the subagents hit, what it cost, and the Baba change that removes it. Ordered by payoff.

## 1. Structured management-change fields on the company record

Gap: nothing in Baba says when the CEO or CFO started or whether they came from outside. `data_executives` has names
and pay but no dates. Stage 2 had to go to the SEC 8-K Item 5.02 feed, whose structured `positions` field is
inconsistent ("CEO", "chief executive officer", "President and CEO", "CEO-elect"), so recall was poor and every
subagent re-ran the query. Build: ingest 8-K Item 5.02 for every tracked company (Baba already ingests 8-Ks) and
extract `ceo_start_date`, `ceo_external_hire` (prior employer), `cfo_start_date`, `cfo_external_hire`,
`chair_change_date`, `board_adds_12m` into the company record and the comps grid. Then "new external CEO in the last
18 months" becomes a grid filter and stage 2 disappears.

## 2. Long-term targets as a first-class, queryable table

Gap: `data_guidance.targets` already extracts long-term statements with verbatim quotes, but the `field_key` labels
are unreliable (GXO's peer-parity margin statement is filed under `lt_gross_margin_target`), there is no metric basis
(EBIT vs EBITDA vs percent of gross bookings), no target year field, and it is per-company only, inside a 150K-character
payload. Build: a `targets` table with `metric`, `basis`, `level_pct`, `annual_bps`, `target_year`, `synergy_usd`,
`first_stated`, `times_repeated`, `speaker_role`, `document_id`, plus a cross-company query ("every tracked company
whose CEO or CFO stated a margin level with a year, since 2025-01-01"). Stage 3's leg C becomes a lookup. Also a
`sections=["targets"]` selector on `data_guidance` so a caller can fetch just that table.

## 3. Target-versus-consensus gap computed in the grid

Gap: the "unproven" test is management's target margin minus the consensus margin at the target year. Subagents
computed it by hand from `data_financials` with inconsistent sign conventions and fiscal-year label slips. Build: once
item 2 exists, add `target_gap_bps` (target minus consensus at target year, positive when the target is above the
street), `consensus_margin_at_target_year`, and `ebitda_uplift_if_target_hit_pct` to the comps grid. The whole D leg
becomes a filter.

## 4. Fix the margin field and the fiscal-year labels in the comps grid

Gap: `data_comps.ebitda_margin` is the forward-year consensus margin but is not labelled as such; every subagent
assumed trailing and had to compute LTM. Visible Alpha fiscal-year labels are keyed to the fiscal-year end, so Baba's
FY2027 is Chewy's fiscal 2026, and every subagent rediscovered this. Build: rename to `ebitda_margin_fwd`, add
`ebitda_margin_ltm` (last four reported quarters) and `industry_median_margin_ltm`, and expose `fy_label_offset`
(months between the company's fiscal year end and the calendar year) on the company record with a plain-language
note in `about_baba`.

## 5. Revision momentum at more than one horizon

Gap: the screen needed "estimates have stopped falling". `ebitda_revision` (12 months) and `ebitda_turn_pct` (one
fixed 4-month window) exist but the turn window is a single hard-coded date pair. Build: `ebitda_rev_3m`,
`ebitda_rev_6m`, `ebitda_rev_12m` and the same for revenue, all rolling, plus `months_since_estimate_trough` (how long
since forward EBITDA consensus last made a 12-month low). GXO's own history (down 20% in 2023-24, flat since mid-2025)
is the calibration case.

## 6. Next-event calendar

Gap: the names that converted from vague to numeric framing did so at Investor Days (GXO 2026-11-16, BWXT 2026-09-29,
EYE 2025-11-17, ZS 2026-10-06). Baba has no forward event field. Build: pull the Quartr events calendar (Baba already
ingests Quartr transcripts) into `next_event_type`, `next_event_date` on the company record and the grid. "New CEO
with an Investor Day inside six months" is then a filter.

## 7. Cross-company corpus search that returns companies, not passages

Gap: `corpus_search` without a cid returns the top 50 passages across thousands of companies, so a sweep for
"margin expansion target by 2028" surfaces mostly names that are not in the screen. There is no date filter other than
fiscal_year, and conference and investor-day transcripts carry no fiscal year, so they drop out of a fiscal_year query.
Build: an `aggregate=company` mode that returns ticker, hit count, latest date and best snippet, with `filed_after` /
`filed_before` date filters, and a `cids=[...]` list filter so a sweep can be scoped to a screen's survivors.

## 8. Save a screen as a bucket and let score recipes use these legs

Gap: the 125 stage-1 survivors live in a CSV in this repo. `data_comps bucket=` and the Screens page cannot see them,
and `score_config` legs are limited to FCF yield, growth, leverage and founder-led, so the screen cannot be a recipe.
Build: an import that turns a ticker list into an additional bucket with a run date, and new recipe legs for
`drawdown`, `pctile` (own-history valuation percentile), `ebitda_rev_12m`, `ebitda_rev_3m`, `ebitda_margin_ltm` vs
industry median, and the item 1 and 3 fields once they exist.

## 9. Register the screen's questions in the knowledge map

Gap: `data_knowledge` answers registered research questions from the fact store, but none of the screen's questions
are registered, so stage 3 reads transcripts instead of reading Baba. Build: register "What margin level or rate has
management stated, with what horizon, and when was it first said?", "Who on the management team or board is new since
<date>, and from where?", "What synergy or savings target is attached to the latest acquisition, and the deadline?",
and "When is the next Investor Day or framework update?". Then the subagent's job is to read `data_knowledge` and
quote `data_fact_context`, which is a fraction of the tool calls.

## 10. Store screen runs back in Baba

Gap: the 23 candidate records (verbatim quotes with document ids, scores, open questions) sit in this repo only. Build:
accept the per-ticker JSON as an `AI-Generated Research` document of doc_type `Screen` so corpus_search finds it later,
and feed the quoted statements through `facts_propose` into the review queue so the knowledge base learns from each run.

## 11. Smaller fixes seen along the way

- `data_financials consensus_history` returned empty for GXO FY-2024 and FY-2025 while FY-2026 had a full series; the
  earlier years should be there.
- Quarterly Visible Alpha EBITDA did not sum to the annual figure for HLIT 2025; flag such mismatches in the payload.
- Baba fiscal_year on earnings-call documents for off-calendar companies (CNM) runs a year ahead of the company's own
  label; the document title should carry the company's label.
- `data_profile` returns about 15K tokens per call because it embeds the full 10-K business description; a
  `sections=["summary"]` selector would make the one-line business description a cheap lookup.
- `corpus_search` timed out at 60 seconds once on a long hybrid query across the whole corpus; a cheaper lexical
  pre-pass with a company filter would avoid that.
