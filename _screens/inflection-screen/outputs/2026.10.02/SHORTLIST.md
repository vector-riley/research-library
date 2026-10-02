# Inflection screen shortlist, 2026-10-02 run

Funnel: 2,078 US names in Baba's grid -> 167 pass the stage 1 gates -> 125 pass the stabilization test -> 126 read
by Opus subagents (the 125 plus GXO as the archetype; UPS pending) -> 12 core setups -> 4 worth Riley's time first.
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

- 12 of 126 names carry the GXO shape proper. The screen's value is the conjunction; 30 names scored 8 or more and
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
