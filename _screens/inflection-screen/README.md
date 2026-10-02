# Inflection screen (GXO-style setups)

Purpose: find underperforming stocks where a new management team, an acquisition, or a newly stated strategy is
creating a possible but unproven inflection in fundamentals, and where management has publicly put numbers on a
meaningful margin expansion opportunity. GXO Logistics in 2025 to 2026 is the archetype.

The screen has four stages. Stages 1 and 2 are cheap and deterministic and run from Baba's screening grid and
structured SEC data. Stage 3 is the expensive part: one Opus subagent per three or four candidates reads the
primary sources and fills a fixed JSON schema. Stage 4 aggregates and ranks.

## 1. The archetype, in Baba's own fields (GXO, 2026-10-01 close)

| Field (Baba data_comps) | GXO value | What it captures |
|---|---|---|
| drawdown (from Oct 2023 window) | -32% | the stock has underperformed |
| pctile (own-history EV/EBITDA, 60 months) | 1.7% | trading near the bottom of its own range |
| price_ltm_pct | -16% | still underperforming over the last year |
| ebitda_margin (forward-year consensus, FY2027, not LTM) | 7.1% vs industry median 9.8% (LTM actual 6.8% vs 10.4%) | low margin, so each 100 bps matters (about 14% of EBITDA) |
| ebitda_revision (12 months, forward year) | +0.4% | the street has not underwritten the story |
| ebitda_inflection | 0 | consensus does not yet show an inflection |
| ev_ebitda_fy / net_debt_ltm_ebitda | 7.4x / 2.6x | cheap, leverage survivable |
| ebitda_brokers | 14 | consensus is meaningful |

Qualitative fingerprint (from the Baba corpus and 8-K Item 5.02): CEO Patrick Kelleher effective 2025-08-19
(external, ex DHL Supply Chain), CFO 2026-04-01, COO 2026-01-02, new Chairman 2025-12-31; Wincanton acquisition with a
$60 million run-rate cost synergy target by end of 2026; "aiming to deliver at margin levels at or better than
our peer group" (Q4 2025 call) with 20 bps of margin expansion guided for 2026 and an Investor Day promised for
the timeline. The gap between that framing and flat consensus is the setup.

## 2. Pipeline

### Stage 1: quantitative pre-filter (deterministic, free)

Source: `mcp__BQBQ__data_comps` with `us_only=true, limit=2500, sort=ticker`. The result is too large to return
inline, so the host saves it to a file; `stage1_filter.py --dump <file> --out outputs/<date>` reads that file.

Gates (every gate calibrated so GXO passes):

1. Universe hygiene: market cap >= $1bn; >= 3 EBITDA brokers; exclude Financials, Utilities, Energy, Biotech,
   Pharma, and mining industries (margin there is commodity or pipeline driven, not a management lever).
2. Underperforming, two of three: drawdown <= -20%, own-history EV/EBITDA percentile <= 25%, LTM price <= -10%.
3. Room to expand: EBITDA margin (note: the grid's `ebitda_margin` is the forward-year consensus margin, not LTM) <= 15% absolute, or below the industry median (sector median if the industry has
   fewer than 5 names) and <= 30%.
4. Unproven but not broken: 12-month forward EBITDA consensus revision between -30% and +10%.
5. Survivable: net debt / LTM EBITDA <= 5x.

Run on 2026-10-02: 2,079 US rows -> 167 survivors (3 portfolio, 7 pipeline, 157 screen bucket). Rejection counts
are printed by the script. `stage1_ranked.csv` orders survivors by closeness to GXO's fingerprint (`_sim`, lower is
closer: valuation percentile, drawdown depth, margin gap to peers, flatness of revisions).

### Stage 2: catalyst flags (cheap, structured)

Two detectors, both run over the survivors' tickers in batches of about 40:

- Management change: `mcp__sec-api__form-8k` with
  `items:"5.02" AND filedAt:[<18 months ago> TO today] AND item5_02.personnelChanges.type:appointment AND
  item5_02.personnelChanges.positions:("chief executive officer" OR "CEO") AND ticker:(A OR B ...)`.
  Repeat with `("chief financial officer" OR "CFO")`. The structured `item5_02.personnelChanges` block gives the
  person, prior employer, and effective date, which is enough to tell an external hire from an internal promotion.
  Lesson from the pilot: positions are tagged as "CEO" in some filings and "chief executive officer" in others.
  Query both or you miss most of them.
- Acquisition: same tool with `items:"2.01"` (completion of acquisition or disposition) and optionally `items:"1.01"`.
- Margin framework language: `mcp__BQBQ__corpus_search` across the whole corpus (no cid) with k=50, doc_types
  Transcript / Investor Day / Investor Presentation, for phrasings like "targeting margin expansion of basis points by
  2028", "long-term financial framework adjusted EBITDA margin of percent by 2029", and lexical mode for
  "basis points of margin expansion target". Intersect hit tickers with the survivors.

Output: `stage2_catalyst_flags.csv` (30 flags on 2026-10-02: 13 CEO events, 6 CFO events, 3 acquisitions, 8 corpus
flags). Known recall limits: the structured 8-K fields exist only where the vendor parsed the filing, and the
cross-corpus sweep returns only the top 50 hits across thousands of companies, so a per-company scoped search in
stage 3 is the real test. `data_executives` has no start dates, so it cannot replace the 8-K query.

### Stage 3: subagent read (Opus, the metered step)

Prompt: `prompts/stage3_candidate_read.md`. Each subagent gets 3 tickers, the stage 1 row, and the stage 2 flags,
and must fill the JSON schema from primary sources only: Baba `corpus_search` scoped to the cid (lexical for
"basis points", "margin target", "by 2028"), `corpus_fetch_document` around the hit for a verbatim quote,
`data_guidance` (its `targets` list holds Baba's own extraction of long-term targets with verbatim quotes),
`data_financials` summary for the consensus margin path, `data_comps` for the quant row, and the 8-K tool for
dates. Budget: 12 to 20 tool calls per ticker.

Scoring, 0 to 10: A underperformance and cheapness (0-2), B catalyst recency and quality (0-3, external CEO plus
other changes scores highest), C numeric margin framing by management (0-3, a level or annual rate with a year,
repeated, scores highest), D unproven (0-2, consensus-implied margin at the target year at least 100 bps below
management's target). Disqualifiers: catalyst older than 18 months, target already in consensus, covenant stress,
commodity-driven margin.

Why Opus and not the top model for this stage: the work is extraction against a fixed schema with explicit
scoring rules, and the sources are short passages. Cost scales with candidate count, not with judgment depth.
The calibration run on GXO (the archetype) checks that the prompt recovers the known answer before trusting it on
unknown names.

### Stage 4: aggregate

`python3 aggregate.py --run outputs/<date>` collects `candidates/*.json` into `ranked.md` and `ranked.csv`.
Riley reads the top of the table and the per-ticker `.md` notes (verbatim quotes with document ids), then decides
what goes to the pipeline bucket in Baba. Nothing is written to Baba by the screen.

## 3. Cost and cadence (estimates, not measured)

- Stages 1, 2 and 4: a few minutes and no model spend beyond the orchestrating session.
- Stage 3: roughly 15 tool calls and 60k to 120k tokens per ticker on Opus is the planning estimate; the pilot's
  `tool_calls` field in each JSON records the actual count.
- Suggested cadence: monthly full run; weekly stage 2 only (new 8-K Item 5.02 and 2.01 filings against the standing
  stage 1 list) so new CEO announcements surface within days.

## 4. Known gaps and next steps

Calibration run on GXO (2026-10-02): the archetype scored 9/10 on its own rubric (A2 B3 C2 D2). It lost the point on C
because the CEO's quantified level ("3.5% to 4% EBIT ... deserve to be above six", Q2 2026 call and Jefferies
conference) carries no year yet; the dated plan is promised for the 2026-11-16 Investor Day. Decision: keep C strict.
A 9 for the archetype is the reference point, and a candidate that already has a dated level is a better setup than
GXO was. Other calibration lessons now folded into the prompt: management may state the level in EBIT and the rate in
EBITDA, so the schema records the metric basis and any assumption behind the gap; `data_guidance` field labels are
unreliable but its verbatim quotes are good; hybrid search on the peer-parity phrasing found the key quotes in one
call, while lexical search needs a fiscal_year filter or it returns 2021 to 2024 material; the run took 30 tool calls,
9 of them data_compute, so the budget is now 20 to 30.


- Baba's composite score recipes (`score_config`) only offer FCF yield, growth, leverage, and founder-led legs, so
  this screen cannot live as a Baba recipe today. The drawdown, pctile, ebitda_revision and ebitda_inflection fields
  are in the comps grid though, so stage 1 could become a saved Baba screen if the Screens page gains those filters.
- Non-US names are excluded by `us_only=true`; the 8-K detector is US-only anyway. A non-US variant would need the
  corpus "first call as CEO" detector instead.
- The stage 2 CEO detector found 13 events among 167 names over 21 months. The base rate suggests more; the
  structured 8-K fields may be incomplete. Backstop: a per-company `corpus_search` for "first earnings call" or
  "since joining" in stage 3, and `data_board` for board refresh.
- Activist involvement (13D filings) is not yet a detector. `mcp__sec-api__form-13d-13g` can add it.

## 5. Files

    README.md                 this design
    stage1_filter.py          stage 1 gates and GXO-similarity ranking
    aggregate.py              stage 4 ranking table
    prompts/stage3_candidate_read.md   subagent prompt and JSON schema
    outputs/<date>/           universe_us.csv, stage1_survivors.csv, stage1_ranked.csv,
                              stage2_catalyst_flags.csv, candidates/<TICKER>.json|.md, ranked.md
    LOG.md                    dated run log
