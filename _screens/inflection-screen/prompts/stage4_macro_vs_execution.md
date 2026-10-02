# Stage 4: macro or execution? (for stated-strategy setups with the same management team)

Riley's rule: a stated margin strategy with no change of people still qualifies as a GXO-style setup when (a) the people
are founders or long-tenured operators and (b) there is a credible argument that the margin compression they are now
promising to reverse was mostly the cycle or an external shock, not their own execution. Your job is to test (b) with
numbers, per ticker, and record (a) with dates.

You are given 3 or 4 tickers that already have a stage 3 record in the candidates folder. Read that record's .md first
(it has the target, the gap and the quotes) so you do not redo it.

## Tools (load with ToolSearch "select:<name>")

- mcp__BQBQ__companies_search (ticker -> cid), mcp__BQBQ__data_profile (CEO bio, founder status; parse only profile.ceo,
  profile.summary and the executive-officer paragraphs of profile.description), mcp__BQBQ__data_executives.
- mcp__BQBQ__data_financials with sections=["fundamentals"]: the consensus pivot includes historical actuals by fiscal
  year. Pull revenue and EBITDA (or operating income, whichever the target uses) for the last five fiscal years and the
  current year estimate, and compute the margin path. Note the fiscal-year label offset where it applies.
- mcp__BQBQ__data_comps with industry="<the company's industry>" (and sector), limit 50: the peer set. Pick 4 to 8 peers
  that actually compete or share end markets (use judgment; drop names with margins above 60% or below 0, and drop
  companies the target itself names as not comparable). For each peer pull the same margin history with data_financials
  fundamentals. If more than 8 peers, use the 6 closest by business.
- mcp__BQBQ__corpus_search scoped to the cid, hybrid mode, for management's own attribution of the margin decline:
  phrases like "volume", "destocking", "end market", "housing starts", "freight recession", "tariffs", "input costs",
  "mix", "we did not execute", "self-inflicted", "operational issues", "lost share". Fetch the passages with
  corpus_fetch_document (offset=chunk_index-1, limit=4) and quote verbatim.
- mcp__BQBQ__data_compute for every derived number.
- mcp__sec-api__form-8k only if you need a date for a CEO or CFO start.

## What to compute

1. Company margin path: peak fiscal year and margin, trough fiscal year and margin, latest LTM, in the metric the target
   uses. Decline in bps from peak to trough.
2. Peer median margin path over the same fiscal years, same metric where available (EBITDA margin is fine for all if
   operating margin is unavailable). Peer median decline in bps over the same window.
3. Attribution ratio = peer median decline / company decline. Near 1 or above means the industry fell as much as the
   company (macro). Well below 1 means the company fell more than peers (execution or mix). Record the ratio and the
   inputs; do not round the inputs away.
4. Relative position: company margin minus peer median at the peak year and at the trough year. If the company lost
   relative position through the downturn, that is execution evidence even when the industry also fell.
5. Revenue path: did revenue fall with margin (volume shock) or did margin fall on flat or rising revenue (cost or
   price problem)? Record peak-to-trough revenue change.
6. Track record: did management hit its previous dated targets (check the stage 3 record and transcripts)? Any
   restatement or control weakness? Any share-loss admission?
7. Tenure: CEO start date and whether founder; CFO start date; months in seat for each.

## Verdict

- macro_led: ratio >= 0.7, relative position held or improved, revenue fell with margin, management attribution matches
  the numbers, no missed-target pattern.
- mixed: ratio 0.4 to 0.7, or ratio high but relative position slipped, or one missed target.
- execution_led: ratio < 0.4, or margin fell on rising revenue, or a pattern of missed targets, restatements or share loss.
State the one or two facts that decided it.

## Output

Write `{TICKER}.attribution.json` into the candidates directory given in the task:
```json
{"ticker": "", "metric": "EBITDA margin | operating margin", "fy_label_note": "",
 "company": {"peak_fy": "", "peak_margin_pct": null, "trough_fy": "", "trough_margin_pct": null, "ltm_margin_pct": null,
             "decline_bps": null, "revenue_peak_to_trough_pct": null},
 "peers": {"tickers": [], "median_peak_margin_pct": null, "median_trough_margin_pct": null, "median_decline_bps": null,
           "source": "Baba data_financials fundamentals"},
 "attribution_ratio": null, "relative_position_bps": {"at_peak": null, "at_trough": null},
 "management_attribution": [{"quote": "", "speaker": "", "date": "", "document_id": 0}],
 "track_record": {"prior_dated_targets": [{"target": "", "set": "", "due": "", "outcome": "hit | missed | pending"}],
                  "restatement_or_weakness": false, "share_loss_admitted": false},
 "tenure": {"ceo": "", "ceo_start": "", "ceo_months": null, "founder": false, "cfo_start": "", "cfo_months": null,
            "long_tenured": "ceo_months >= 84 or founder"},
 "verdict": "macro_led | mixed | execution_led", "deciding_facts": ["", ""], "confidence": "high | medium | low",
 "tool_calls": 0}
```
Also append a section titled `## Macro or execution` (at most 6 lines) to the existing `{TICKER}.md`: verdict, ratio with
inputs, relative position, one management quote with document id, tenure line.

Rules: no invented numbers, every figure sourced; verbatim quotes only from fetched passages; no em dashes; budget 15 to
25 tool calls per ticker; state the fiscal-year label you are using.
