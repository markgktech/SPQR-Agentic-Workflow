---
name: quaestor-doc-execute
description: DOC ticket execution skill — DOC-prefixed tickets only; discovery, per-fix verification, ticket creation boundaries
---

INVOKE
Load when the ticket is a DOC ticket (`Ticket type` = Doc) — do not load for SPIKE or FEAT tickets
Load after quaestor-relatio.md pre-flight completes

PRE-FLIGHT
Read full ticket body — all items listed
Map each item to exact file path before starting any edit
If file path is ambiguous: ask owner before proceeding
If item references a file that does not exist: flag to owner — do not create silently

DISCOVERY RULES
For each item: identify target file
Read the full file before making any change
Find the correct insertion point — anchor section first, not end of file unless explicitly instructed
If no suitable section exists: add new section and flag the deviation

EXECUTION RULES
Apply items one at a time — complete one before starting next
After each fix: re-read the modified section to verify the change landed correctly
Do not mark an item done without re-reading
If re-read reveals the fix did not apply correctly: retry once, then flag to owner

TICKET CREATION BOUNDARIES
Agent may propose new tickets for: work clearly out of scope for this DOC ticket; items requiring implementation (not documentation)
Agent may NOT create tickets autonomously — propose only; owner creates
All proposals follow ticket-slicing.md format

OUTPUT — CHANGE MANIFEST (D12)
DOC output is a local change-manifest: `<TICKET-ID>_output.md` in the work_documents/ vault, frontmatter `up: "[[<TICKET-ID>]]"` + `tags: [content/doc-change]` + a `modifies:` property (list of files/docs touched). Body lists:
  each item with DONE / FLAGGED status
  file paths + sections modified
  any ⚠️ flags (per doc-maintenance.md format)
  any deviations from expected structure
After all items complete: create the hub from template if missing (backfill invariant) and append a handover block to `<TICKET-ID>_handover.md` (not a closing Notion comment) — header `### Quaestor — <verdict> | <date>`; add the hub session row.

NEVER
Never append to end of file without finding the correct anchor section first
Never mark an item done without re-reading the modified section
Never create tickets in Notion — propose only
Never skip the handover block at completion
Never start a new item before the previous one is verified
