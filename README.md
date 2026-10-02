# research-library

Riley's personal research library. Working context, drafts, notes and outputs, one folder per company.

## Rules

- Baba is the system of record for firm IP. Finished firm work (memos, models, call notes) goes to Baba.
- This repo is the working layer: context, drafts, prompts, working notes.
- Filings, transcripts and earnings releases are not stored here. Query Baba for them.
- No passwords, API keys or tokens.
- Files over 100 MB will not upload to GitHub.

## Layout

    TICKER/
      THESIS.md    current view on the company
      LOG.md       dated log of work, newest first
      context/     notes, call notes, models, working files
      outputs/     documents produced
    _template/     copy this folder to start a new company
    _screens/      cross-company screens (design, scripts, prompts, dated outputs)

## Instructions for Claude sessions

1. Work inside the company folder named in the request.
2. Read THESIS.md and LOG.md first, then context/.
3. Use Baba for company data before any other source.
4. Save finished documents to outputs/ and add a dated entry to LOG.md.
5. Commit and push before ending the session.
