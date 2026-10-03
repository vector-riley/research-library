# Standards

Every rule Riley has had to correct. The checker reads drafts against this file before he sees them. Add a rule the first time he corrects something new: next free id, the rule in one line, a real example, the date.

Severity: **Must** rules get fixed or flagged every time. **Style** rules get fixed silently.

## N. Numbers and sourcing (Must)

- **N1** Never invent a number. A missing figure stays a visible blank, and the gap is named in the chat message, not the document.
- **N2** Every figure traces to a source (document and date) or is labeled as an estimate. An estimate never sits in the same clean table format as a sourced figure. *Example: Bespoke Vol 54, a "~250" Wayfair subsample was an estimate presented like a printed N; only N=241 was printed, and it was the base for one question only (2026-10-01).*
- **N3** Attribute precisely: say whether a figure is a company disclosure, management agreeing with analyst math, or Riley's own estimate. Use the source's own word. *Example: the DKNG Q2 letter says customers "engaged," not "acquired"; the ~$700 gross profit per active user was Riley's pre-call framing, not management's (2026-09-28).*
- **N4** Do not restate an industry norm as if it were contractual without the document.
- **N5** Quotes are verbatim. When a speaker contradicts themselves, say so plainly and quote both statements verbatim.
- **N6** An inference is labeled as an inference. Claims headed to Ben, Zach, or outside the firm are verified against a source first, or cut. *Example: Soomla timeline and Meta carve-out were verified before the APP TRO takeaways went out (2026-10-02).*

## D. Document hygiene (Must)

- **D1** No process narration and no restating what Riley told Claude inside a deliverable. *Examples: "no Q2 callback exists, this meeting serves as it", "attendees not recorded in our notes", "check whether he attends", "per Baba", "not in the corpus".*
- **D2** No "Sources:" footers, source lists, or appendix clutter in a document prepared for Riley. Provenance and verification notes go in the chat message. A short derived-figure note is fine.

## V. Voice and wording (Style)

- **V1** No em dashes.
- **V2** Banned words: delve, tapestry, multifaceted, crucial, underscore, leverage (as a verb).
- **V3** Plain short sentences, ordinary words. Answer first, then the reason. No setup or wind-up.
- **V4** Define any term of art in the same sentence it first appears. *Example: not "death benefit leverage" but "if you die young it pays out far more than you paid in".*
- **V5** No abbreviations unless the context makes them obvious. No hedge-fund jargon.
- **V6** No epigram closers ("which is X dressed up as Y" and similar reframes). Stop when the point is made.
- **V7** No named maxims ("Robyn's rule: ...") and no instructions to the reader dressed as analysis ("treat the split as unresolved") (2026-09-09).
- **V8** Slide and deck text in Riley's voice: short bold label, then dense plain prose; numbers first; "~" for approximations; semicolons and inline 1) 2) lists. No full-sentence bold claim lead-ins (asked twice, 2026-09-04).
- **V9** When asked for a simple answer, give the simple answer in the same framing as before. *Example: DASH guidance range, "I wanted this to be simple, just like the Q2 framing" (2026-10-01).*

## Q. Meeting and conference questions (Must)

- **Q1** Questions target long-term thinking, business quality, and durability of earnings growth. No questions about guidance or in-year numbers.

## F. File format (Must)

- **F1** Excel: Times New Roman; percentages stored as fractions.
- **F2** Bloomberg BDH formulas always include "Dates=H". EOP pattern: `=IFERROR(LOOKUP(9.99E+307,BDH(tkr,"PX_LAST",end-7,end,"Days=W","Fill=P","Dates=H","cols=1;rows=0")),NA())`. Average pattern: `=IFERROR(AVERAGE(BDH(tkr,"PX_LAST",start,end,"Days=W","Fill=P","Dates=H","cols=1;rows=0")),NA())`.

## P. Process (not checkable on the draft; followed while working)

- **P1** Baba first for any company data and for Riley's own internal documents: companies_search, then company_overview or corpus_search, before web search, EDGAR, or Dropbox (2026-09-29).
- **P2** Cleaning rough meeting notes: resolve fragments with common sense and apply the reading. Ask only about a fragment with no plausible reading, and quote the raw lines before and after it.
- **P3** No disclosure or compliance flags for public conference group sessions; flag only true one-on-ones.
