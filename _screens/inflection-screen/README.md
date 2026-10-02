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
4. Unproven, and the cutting has stopped: 12-month forward EBITDA revision between -30% and +10%, AND the 4-month
   revision (grid field `ebitda_turn_pct`) at or above -3%. The size of the prior cut is not the test. GXO's own
   FY2026 EBITDA consensus (Baba `data_financials` consensus_history, pid 4250) fell 20% from May 2023 to Feb 2024,
   was still -8% over the twelve months before the new CEO's first call, and has moved less than 1% in any four-month
   window since mid-2025. A cut is often the early part of the story; what distinguished GXO was stabilization.
5. Survivable: net debt / LTM EBITDA <= 5x.

Run on 2026-10-02: 2,079 US rows -> 167 survivors (3 portfolio, 7 pipeline, 157 screen bucket) under the original -30%
floor with no stabilization test; 125 of those pass the 4-month >= -3% test added after the pilot. Rejection counts
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
management's target, and 0 whenever the 4-month revision is below -3% because estimates are still falling; a deep
12-month cut that has stabilized does not zero it). Disqualifiers: catalyst older than 18 months, target already in
consensus, covenant stress, commodity-driven margin. `aggregate.py` recomputes D mechanically on the stabilization rule
(column D2) beside the subagent's own D, so a rule change re-ranks past runs without re-running the agents.

Why Opus and not the top model for this stage: the work is extraction against a fixed schema with explicit
scoring rules, and the sources are short passages. Cost scales with candidate count, not with judgment depth.
The calibration run on GXO (the archetype) checks that the prompt recovers the known answer before trusting it on
unknown names.

### Stage 4a: macro or execution (same-team strategy setups only)

Riley's rule, added after the full run: a stated strategy with no change of people qualifies when the people are founders
or long-tenured (CEO 84+ months) and the margin compression was mostly the cycle. Prompt: `prompts/stage4_macro_vs_execution.md`.
Each subagent computes the company's peak-to-trough margin decline against the peer median over the same fiscal years
(attribution ratio), the change in relative position, the revenue path, management's own attribution verbatim, the record
on prior dated targets, and tenure. Output: `candidates/<TICKER>.attribution.json` and a section appended to the note;
`attribution.md` is the table. On 2026-10-02, 19 names: 1 macro-led, 4 mixed, 14 execution-led.

### Stage 4b: aggregate

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

## 5. Pilot results (2026-10-02, 13 names, 5 Opus subagents)

Full table: `outputs/2026.10.02/ranked.md`. Per-name notes with verbatim quotes and document ids: `outputs/2026.10.02/candidates/`.

- Three names meet the conjunction test (B >= 2, C >= 2, D >= 1, no disqualifier): GXO (archetype, 9), EYE (9) and
  ACI (8, and the subagent itself says the mechanical score overstates the fit because management never stated a
  margin level).
- EYE (National Vision) is the cleanest new analogue: down 44%, at the bottom of its own five-year EV/EBITDA range,
  new CEO 2025-08-01 and new CFO, and a repeated "50 to 150 basis points of operating margin a year through 2030"
  path with 2030 consensus about 110 bps below the midpoint. Weak point: forward EBITDA revisions are already +8%.
- JBTM (8) has the strongest numeric framing in the batch (20% adjusted EBITDA margin in 2028, $150M synergies,
  consensus about 300 bps short) but the Marel close is 21 months old and leadership is unchanged. Worth a look
  even though it fails the catalyst window.
- Six names (HOG, GPK, AVAV, PRIM, DRVN, LPX) carry 12-month estimate cuts of 15% to 27%. The first pass treated a cut
  deeper than 10% as a broken story and zeroed D. That was wrong on GXO's own history (its FY2026 consensus fell 20% in
  2023-24), so the rule became a stabilization test: D is zero only when the 4-month revision is still below -3% (LPX at
  -12.5%, ACI at -7.8%) or the target is already in consensus (AVY, ZS). On that basis HOG and GPK re-enter as setups and
  DRVN and PRIM rise, while ACI drops out because its estimates are still falling.
- Two names show numeric framing with no management catalyst (AVY, CNM) and the street already models the target in
  AVY's case. They calibrate the screen: C alone is not the setup.
- Cost actually observed: 12 to 30 tool calls per name; the five subagents used about 1.2 million tokens in total,
  so roughly 90k tokens per name on Opus.

### Second batch (2026-10-02, the 10 stage 2 flagged names not yet read)

Ten names carried a stage 2 flag, passed the stabilization gate and had not been read: CHWY, LYFT, TOST, NOC, BWXT,
HLIT, ZS, OMCL, KNF, BURL. Three subagents, about 940k tokens. Results on the stabilization-based score:

- Three more setups: CHWY (9: 10%+ adjusted EBITDA margin target restated 2026-09-09 and a roughly 100 bps a year
  pace, consensus 141 bps short by Baba FY2031, but the catalyst is only an internal CFO), LYFT (8: about 4% of gross
  bookings in 2027, 39 bps above consensus, internal CFO), BWXT (7: 17.5% to about 20% by 2030 set at the 2026-09-29
  Investor Day, 133 bps above FY2030 consensus, but stated once, three days old, and the stock is not cheap).
- Numeric framing without a catalyst: KNF (20% goal with no year, 404 bps above FY2028 consensus, but estimates still
  falling at the 4-month horizon), BURL (Burlington 2.0 mostly priced in), TOST (target already in consensus).
- Catalyst without framing: NOC (external CFO, flat guide), OMCL (external CFO, no target), HLIT (Video sale closed,
  no target).
- ZS: external CFO but the street already models the margin; an Investor Day on 2026-10-06 could change that.

Two scoring inconsistencies the subagents flagged, left for Riley to rule on: CHWY's C=3 rests on a one-year guide
repeated on three calls while GXO's single one-year guide earned C=2, so repetition is doing the work; and the
mechanical D2 zeroes KNF on a -3% four-month move even though its stated target is 404 bps above consensus.

### Full run (2026-10-02, all 125 stabilized survivors)

The remaining 105 names ran through 27 Opus subagents in three waves. Results and lessons are in
`outputs/2026.10.02/SHORTLIST.md`; the table is `outputs/2026.10.02/ranked.md`, now with a Core column (a Setup whose
catalyst includes a CEO-level change). Twelve names carry the core flag; four are worth reading first (EYE, FND, HOG,
GPK), seven more have the leadership change but not yet the numbers and each has a dated event to watch (KR
2026-10-20, PYPL, POOL, TXT, PRMB, AOS, SARO). The structured 8-K detector missed about half the CFO changes; stage 2
should query by CIK without the appointment-type clause, and deal detection should move to Baba transcripts.

## 6. Files

    README.md                 this design
    stage1_filter.py          stage 1 gates and GXO-similarity ranking
    aggregate.py              stage 4 ranking table
    prompts/stage3_candidate_read.md   subagent prompt and JSON schema
    outputs/<date>/           universe_us.csv, stage1_survivors.csv, stage1_ranked.csv,
                              stage2_catalyst_flags.csv, candidates/<TICKER>.json|.md, ranked.md, SHORTLIST.md
    BABA_WISHLIST.md          what to build into Baba so stages 2 and 3 get cheaper
    LOG.md                    dated run log
