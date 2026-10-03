# Session rules for this repo

Read README.md first. It has the layout and the working rules.

## Standards

Before handing Riley any deliverable (document, memo, slide text, notes, spreadsheet, email draft), check it against STANDARDS.md with a reviewer that did not write it, fix what it finds, and put any remaining gaps in the chat message, never in the document. When Riley corrects something STANDARDS.md does not cover, add the rule there in the same session.

## Open items

Before ending any session, append to OPEN_ITEMS.md one line for each thing left hanging:

- a decision Riley deferred
- a step that is waiting on Riley, on Claude Code, on the engineer, or on an outside party
- a question sent to someone with no reply yet
- a number or source flagged as missing that still needs to be found

Format: `YYYY-MM-DD | Owner | What is owed, in one sentence | optional source`

Owner is one of: Riley, Claude Code, Engineer, External.

Only append below the `<!-- items below this line -->` marker. Do not rewrite existing lines. Do not log work that was finished in the session. Commit and push with the rest of the session's changes.

If the session resolved an item already on the Open Items list, add a line with Owner set to `Done` and item text matching the original as closely as possible; the sweep closes it.
