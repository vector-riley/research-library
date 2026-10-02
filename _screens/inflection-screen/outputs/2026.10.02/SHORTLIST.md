# Inflection screen shortlist, 2026-10-02 run

Funnel: 2,078 US names in Baba's grid -> 167 pass the stage 1 gates -> 125 pass the stabilization test -> 127 read
by Opus subagents (the 125 plus GXO as the archetype and UPS) -> 12 core setups -> 4 worth Riley's time first.
Full table: ranked.md. Per-name notes with verbatim quotes and Baba document ids: candidates/<TICKER>.md.

Score components: A cheapness (0-2), B catalyst (0-3), C numeric margin framing with horizon (0-3), D unproven vs
the street on the stabilization rule (0-2). Core = catalyst includes a CEO-level change and B, C, D all clear the bar.

## Tier 1: read these first (CEO change, numbers on the table, street not there yet)

| Ticker | Score | LTM | Why | What to check |
|---|---|---|---|---|
| EYE | 9 | -44% | New CEO (2025-08) and CFO; "50 to 150 bps of operating margin a year through 2030" said five times; 2030 consensus 110 bps below the midpoint; bottom of its 5-year range | Revisions already +8%; is the margin gain durable with traffic down 5%? |
| FND | 9 | -38% | External CEO Bradley Paulsen (2025-12, ex Rentokil NA); standing mid-teens EBITDA goal about 230 bps above FY2028 consensus; estimates stabilized after a 14% cut | Goal is inherited and undated; depends on housing; no Investor Day scheduled |
| HOG | 9 | -9% | External CEO Starrs (2025-10, ex Topgolf), new COO and Chairman; dated $150M savings and $350M+ HDMC EBITDA in 2027 | Street already near the 2027 EBITDA target (gap 37 bps); 12m estimates -25% though flat for 4 months |
| GPK | 9 | -52% | External CEO Rietbroek (2026-01, ex Primo Brands), new Chairman; 69% drawdown | Only numbers are 2026 savings swamped by inflation; 4.7x leverage; margin partly board-price driven |

## Tier 2: CEO change but the numbers are not yet there (watch the dated event)

| Ticker | Score | Event to watch | Note |
|---|---|---|---|
| KR | 7 | Investor update 2026-10-20 | External CEO Greg Foran (ex Walmart US, 2026-02), external CFO; CFO said "not going to put a number on it" yet; stock not cheap (A=0) |
| PYPL | 9 | Framework update promised, no date | External CEO Lores (2026-03, ex HP); $1.5B gross savings mostly reinvested; street has margins falling |
| POOL | 8 | New CEO's 2027 targets | External CEO Watwood (2026-05, ex Motion Industries); no margin number yet; cheap |
| TXT | 7 | January 2027 guidance | Internal CEO (2026-01); Industrial separation pending; Aviation $150M / 200 bps quantified without a year; 5-year low multiple |
| PRMB | 9 | Spring 2027 reset | Board-insider CEO Foss (2025-11); 234 bps gap is to an inherited 25% 2027 target he calls under review |
| AOS | 9 (agent) | Q3 2026 call: China review | External CEO Shafer (2025-07, ex 3M), external CFO, new Chairman, 2nd percentile multiple; no company-wide margin target yet |
| SARO | 7 | New CEO's first call | Board member McElhinney CEO 2026-10-01; 2026 margin already in consensus |

AOS does not carry the core flag because its agent recorded the catalyst as a strategy update; on the 8-Ks it is a full
external leadership reset and belongs in this tier.

## Re-weighted view: strategy and deals as peers of management change

The brief put three catalysts on equal footing. The first scoring did not: an external CEO earned 3, a stated strategy
alone earned 1, and the Core flag required a CEO change, which pushed the biggest measured gaps into Tier 3.
`ranked_by_gap.md` corrects that: a dated numeric framework stated inside the window counts as a catalyst equal to a
management change, and the list is ordered by the gap between management's target and consensus. On that view the
names to add to Tier 1, where the gap is large, the target was restated in 2026 and the agents did not flag it as
walked back, are:

| Ticker | Gap bps | Target | Catalyst | Why it belongs |
|---|---|---|---|---|
| JBTM | +299 | 20% EBITDA margin 2028 | Marel combination, 2026 Investor Day | Repeated by CEO, CFO and President in 2026; consensus at 17.0% |
| OSK | +169 | 12% to 14% operating margin 2028 | 2025 Investor Day | Reiterated through Q2 2026; margins fell 400 bps YoY, so execution is the question |
| DXC | +129 | 8% to 10% EBIT FY2029 | 2026 Investor Day, external President | CEO 32 months in; margins still falling |
| RPM | +155 | 16% EBIT, read as FY2028 | Investor Day 2026-11-09 | Board's own pay target is only 14%, so the 16% may be reset |
| OC | +373 | mid-20s EBITDA margin 2028 | 2025 Investor Day, external CFO | Mostly a housing-starts call; margin already above peers |
| EEFT | +178 | 100 to 200 bps by 2028 | 2026 Investor Day | Founder-run, no leadership change |
| KD | +198 | 20% to 22% FY2028 | New external CFO after control failures | Target set by the departed CFO and not repeated in 2026 |
| CNM | +218 | 15% fiscal 2028 | 2023 Investor Day, reaffirmed 2025 | Internal successor team; margin above peers |

Large gaps that are not setups even on this view: PLUG (+987, loss-making), PVH (+652, target missed and not repeated),
FOUR (+512, gross-revenue artifact), HIMS (+497, margins down by choice), EFOR (+255, CEO since 2019, margins falling).

## Stage 4: macro or execution, for the same-team strategy names

Riley's refinement: a stated strategy with the same people qualifies when the people are founders or long-tenured
operators AND the margin compression they promise to reverse was mostly the cycle, not them. Five Opus agents tested
that on the 19 same-team names with a measurable gap, comparing each company's peak-to-trough margin decline with its
peer median over the same years. Full table: `attribution.md`.

Result: 1 macro-led, 4 mixed, 14 execution-led. In most of these stories the company lost margin that its peers did
not, which is the opposite of the GXO shape and explains why the first-pass weighting on management change was not as
wrong as it looked. The names that survive the rule, in order:

| Ticker | Verdict | Ratio | Tenure | Gap bps | Read |
|---|---|---|---|---|---|
| EEFT | mixed, leaning macro | 2.73 | founder CEO since 1994 | +178 | Peers fell 160 bps vs its 59 bps and it closed the gap to peers; still 455 bps below its 2019 peak while peers rose, and margin is slipping on rising revenue. Closest fit to the rule. |
| LOW | mixed, leaning macro | 1.30 | CEO 99 months | +181 | Peers fell as much; Lowe's lead over peers widened; but it missed its 14.5% fiscal 2025 goal and the 14%+ is undated; December 2026 is the event. |
| EFOR | mixed, leaning macro | 1.25 | CEO 89 months | +255 | Peers fell as much and the gap narrowed; but the decline is still running after peers stabilized and Q1 2026 was called a mix miss. |
| UFPI | macro-led | 4.91 | CEO 21 months but 28 years at the company; CFO 22 years | +329 | Peers (lumber and OSB mills) fell five times as far; UFPI gained relative position. Fails the strict tenure test on the CEO date only. Ratio is inflated by mill peers (about 3.6 on a stricter set). |

Failed on execution despite long tenure: CVNA (founder, but the 2022 trough was self-inflicted and peers barely moved),
RPM (CEO since 2002, 16% target missed since 2018, performance shares vested at zero), STRA (margin fell 1,200 bps
while peers rose), OC (organic ratio 0.34, premium to peers nearly gone), BWXT (acquisition mix, not cycle).
Failed on both: JBTM (ratio 0.17, missed FoodTech guides, the 2028 target mostly reverses Marel dilution), OSK (peers
rose while it fell, two EPS guide cuts), CNM (SG&A on rising revenue, two missed years against its own 30 to 50 bps
rule), DXC, KD, TNET, ADNT, NWL, WWW, KNF.

## Tier 3: numbers without a CEO change (framing stories; a CFO or deal is the only catalyst)

DXC (9: 8% to 10% EBIT by FY2029 vs 7.7% street, external President, CEO 32 months in), KD (9: forced finance
clean-up, 20% to 22% FY2028 target set by the departed CFO), ADNT (8: pending CFO, 8% target 168 bps above street,
margins falling), CHWY (8: 10%+ target restated Sept 2026, internal CFO), GEHC (8: external CFO, 17% to 20% EBIT by
2028 vs 16.4%), LYFT (8), OC (8: mid-20s by 2028 vs 21.3%, external CFO, housing call), FUL (8), KBR (8), TNET (8),
BWXT (7: 20% by 2030 set three days ago), and the no-catalyst framing names OSK, JBTM, RPM (Investor Day 2026-11-09),
STRA, CNM, EEFT, JJSF, CVNA. Useful as a watch list for when a management change arrives.

## Mechanical highs that are not the setup

HUN (10, commodity margins, Olin merger), IP (9, containerboard prices), FOUR (9, low-margin flag is a gross-revenue
artifact), ALKT, AVAV, CDW, SMG, UBER (targets already in consensus), PLUG (loss-making, positive-EBITDA promise),
AI (returning founder cutting costs at a shrinking business), HIMS (margins down by choice).

## What the full run taught

- 12 of 127 names carry the GXO shape proper (UPS, read last, scored 7 and is not one: six-year CEO, walked-back 12% target, margin above peers). The screen's value is the conjunction; 30 names scored 8 or more and
  most are not the setup, which is why the table shows the components, not just the total.
- The structured 8-K Item 5.02 feed missed roughly half the CFO changes and several CEO changes the subagents found
  by querying per ticker or per CIK (UAA is filed under "UA"; IBP returns nothing). Stage 2 must query by CIK and
  without the appointment-type clause. The Item 2.01 acquisition feed missed most deals (Lowe's FBM, Hub Group,
  Lippert and Patrick, Olin and Huntsman); deal detection should come from Baba transcripts instead.
- Visible Alpha had not loaded the latest reported quarter for most names, so LTM margins in the records run one
  quarter stale; the notes say so where it applies.
- Fiscal-year label offsets (Chewy, Burlington, Albertsons, Olli's, Core & Main, Home Depot, Lowe's) were handled by the
  prompt note and caused no scoring errors this time.
- Two Baba document summaries were attached to the wrong company (CARR doc 107396 reads as Carrefour, IP doc 112156
  as Interpump). The transcript text is correct; the summaries are not.
- Cost: about 11.7 million subagent tokens for 126 names plus the pilot and re-reads, about 91k per name on Opus.
