---
up: "[[v1.5]]"
group: "FDP Ticketing Alignment (SAW-33)"
order: 3/3
tags: [group]
---

# Group 3 — FDP Ticketing Alignment (SAW-33)

## Brief

GROUP: FDP Ticketing Alignment — re-point generic SPQR agent/skill/retro definitions from Notion-comment work-trace to the DOC-21 local-file model
ORDER: 3/3
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/03-fdp-ticketing-alignment.md
RATIONALE: one homogeneous transport swap (Notion → local hub+output+handover) applied consistently across one coherent surface; single mental model, no cross-file conflicts — owner-confirmed single-agent run (deviates from the 7-FILES brief cap by explicit owner decision)
FILL_CHANGES_MADE: yes

SOURCE_OF_TRUTH:
  docs/spqr_self/poc/SAW-33 FDP Ticketing Alignment — PoC.md   ← AUTHORITATIVE for CONTENT (decisions D1–D15). If this brief and the PoC ever disagree, the PoC wins. Do not re-decide; apply.

PRE_FLIGHT (load before editing):
  - docs/spqr_self/poc/SAW-33 FDP Ticketing Alignment — PoC.md   (the decisions — read in full first)
  - docs/upgrade/execution.md   (execution protocol)
  - /Users/kovacsmark/Documents/RecipeAPP/Foodoire/docs/work_documents/dev_logs/opus_outputs/FDP-36_App_Entry_+_Navigation/   (FORM exemplar — the real hub + output + handover + output_revN; mirror this shape exactly)
  - docs/skills/ticket-comment.md   (the field contract that is PRESERVED; only its transport changes)
  - docs/CONFIGURE.md   (token catalogue — for the <TICKET-ID> and Notion-ID placeholders)

CONVENTIONS (mandatory — match existing form, invent no new shape):
  - Agents keep their IDENTITY / PIPELINE / STAGE SKILLS / LAWS / ALLOWED TOOLS / NEVER structure. Edit in place; do not restructure.
  - Skills keep their existing section style and length. This is a transport/convention swap, not a rewrite.
  - The handover block format is the FDP-36 exemplar: `---` delimiter between blocks; block header `### <Agent> — <verdict> | <date>`; the ticket-comment.md fields below it, verbatim contract.
  - Output frontmatter is the tiny computed block `up: "[[<TICKET-ID>]]"` + one content tag — inline it in the skill; do not delegate to a template fetch.
  - The PoC is authoritative for CONTENT; the FDP-36 files + existing file forms are authoritative for FORM.

GUARDRAIL — DO NOT CONFUSE TWO LEVELS:
  - YOUR job now IS to edit docs/agents/, docs/skills/, docs/retro/ in THIS repo. You are authorised to do so.
  - D10's "never modify SPQR process files / CLAUDE.md, never delete files, append-only" is a RUNTIME rule you WRITE INTO the agent definitions for the consuming-project agents (Praetor, Tribunus, …). It is NOT a constraint on you, the execution agent, right now.
  - Never touch a consuming project (Foodoire); never create or ship template files; never commit or push.

EXECUTION ORDER (resumable passes — report per pass, then continue):
  PASS 1 — Foundations + agent mandates (everything else depends on these)
  PASS 2 — OPUS skill chain (Praetor + reviewers)
  PASS 3 — Senate + ticketing skills
  PASS 4 — Spike/DOC/BUG + Retro
  If context runs low: finish the current file, write Changes Made for completed passes, and report which pass to resume from.

FILES:

  # PASS 1 — Foundations + agent mandates
  docs/skills/ticket-comment.md: D2/D8 — convert transport from "post Notion comment" to "append a `---`-delimited block to `<TICKET-ID>_handover.md`"; PRESERVE the field contract; add append mechanics (executor creates the file; locate last `---` block; session_id via `echo $CLAUDE_CODE_SESSION_ID`, `unknown` if unset); `impl_doc` field → local `<TICKET-ID>_output.md` path; routing stays a field. Token → `<TICKET-ID>`.
  docs/skills/git-workflow.md: D8 — `feature/DEV-XXX-slug` → `feature/<TICKET-ID>-slug` (example `FDP-N`); DEV-XXX noted as legacy only; one resolution line ("`<TICKET-ID>` = the consuming project's ticket id, verbatim").
  docs/agents/senate.md: D7/D9/D10 — Consilium + Censura append handover blocks to the local file (not Notion comments); add scoped Write/Edit to the work_documents vault; refine NEVER (never modify SPQR process files/CLAUDE.md; never delete; append-only; KEEP "never write code"); Censura verdict → handover + LESSONS.md; note the hub backfill invariant.
  docs/agents/praetor.md: D7/D2/D3/D11/D8 — Praetor creates the hub for DEV (from template) + writes `<TICKET-ID>_output.md` and appends handover blocks; refine Write scope + NEVER per D10 (already has Write); branch token `<TICKET-ID>`; revisions → `_output_revN.md`.
  docs/agents/tribunus.md: D10/D2 — add scoped Write to the handover file (never code/source); append review/veto block to handover instead of Notion comment.
  docs/agents/probator.md: D10/D2 — same as tribunus (keep read-only build/test Bash; add handover Write only).
  docs/agents/curator.md: D10/D2 — same; appends verdict block + hub session row.
  docs/agents/quaestor.md: D7/D10/D2/D3 — Quaestor creates the hub for SPIKE and DOC; replace "Notion child page" write with local vault Write; refine "never edit docs/" → never edit SPQR process files, MAY write the ticket's work_documents files.
  docs/agents/session-starters.md: D8 — `TICKET-XXX`/`DEV-XXX` → `<TICKET-ID>` (FDP example); note the executor creates the hub at session start; persona placeholders unchanged.

  # PASS 2 — OPUS skill chain
  docs/skills/praetor-input.md: D2 — load context from ticket + local `<TICKET-ID>_handover.md`/`_output.md`, not Notion comments.
  docs/skills/praetor-output.md: D3/D2/D6/D7 — create local `<TICKET-ID>_output.md` (not Notion child page); NOTES removed; append Praetor handover block; write hub + session row.
  docs/skills/praetor-impl-doc.md: D3/D14 — becomes the `<TICKET-ID>_output.md` spec: minimal frontmatter (`up:` + `content/implementation-doc`); REMOVE the `--- TRIBUNUS/PROBATOR/CURATOR NOTES ---` sections; local file, not Notion child page.
  docs/skills/praetor-revision.md: D11/D14 — delta → `<TICKET-ID>_output_revN.md` (CHANGED/NOT TOUCHED/SCOPE NOTE); read veto from handover; drop the "Delta Doc" Notion child page; remove all "NOTES section" references.
  docs/skills/praetor-discussion.md: D8 — token refs only (`[TICKET-ID]` → `<TICKET-ID>`); otherwise check, likely minimal.
  docs/skills/tribunus-input.md: D2/D14 — load Praetor context from local handover/output (impl doc = local file); no NOTES annotation — append to handover.
  docs/skills/tribunus-output.md: D2/D6 — append findings/verdict/veto block to handover (not Notion comment); write hub session row.
  docs/skills/probator-input.md: D2 — local handover/output context.
  docs/skills/probator-output.md: D2/D6 — append block to handover; hub session row.
  docs/skills/curator-input.md: D2 — local handover/output context.
  docs/skills/curator-output.md: D2/D6 — append verdict block to handover; hub session row.
  docs/skills/collegium-veto.md: D11 — veto format → a handover block, not a Notion comment.

  # PASS 3 — Senate + ticketing skills
  docs/skills/consilium-input.md: D2 — ticket + local handover, not "all Notion comments".
  docs/skills/consilium-output.md: D2/D7 — handoff → append a handover block (not Notion comment / ticket body); hub may not exist yet — append handover only.
  docs/skills/censura-input.md: D2 — load prior stages from the local handover file; update the Law-3 framing (external record = the on-disk/committed handover file, not the Notion comment).
  docs/skills/censura-discussion.md: D2 — load from handover, not Notion comment.
  docs/skills/censura-output.md: D2/D6 — verdict → handover block + LESSONS.md; drop "post Notion ticket comment" for the work-trace; hub session row.
  docs/skills/censura-ticketing-input.md: D9 — KEEP Notion ticket creation; update to FDP-N central numbering + new Notion templates; type in the `Ticket type` field.
  docs/skills/censura-ticketing-discussion.md: D9 — REJECT finding → handover; ticket creation stays Notion.
  docs/skills/censura-ticketing-output.md: D9 — Notion ticket creation on new templates/numbering; plain-description titles + type field.
  docs/skills/ticket-slicing.md: D9 — Notion ticket creation; FDP-N numbering; plain-description titles + `Ticket type`; native template IDs.

  # PASS 4 — Spike/DOC/BUG + Retro
  docs/skills/quaestor-relatio.md: D2/D3 — spike research; output is local; Notion-internal verify refs → local file refs.
  docs/skills/quaestor-relatio-output.md: D3/D6 — spike output = local `<TICKET-ID>_output.md` (minus top metadata block); remove the Notion parent-page indirection; append handover block; hub session row.
  docs/skills/spike-document.md: D3 — the spike document = the local output file structure minus its top metadata block; replace "Notion child page"/parent with the local vault file; Notion-write-failure clause → file-write failure handling.
  docs/skills/quaestor-doc-execute.md: D12 — DOC output = local change-manifest (files/sections touched, DONE/FLAGGED, ⚠️ flags) with a `modifies:` property; append handover block instead of the closing Notion comment.
  docs/skills/doc-maintenance.md: D12/D4 — Curator scans handover blocks for the ⚠️ prefix (not Notion comments); CLAUDE.md flag flow unchanged but sourced from the handover.
  docs/skills/debugging-tribunus-input.md: D15 — BUG standalone; "Notion ticket comment optional" → local handover optional; chain roles otherwise owner-deferred.
  docs/retro/retrospector.md: D13 — output = local retro file (not Notion child page); add scoped Write; remove the "Notion child page" mandate; frontmatter + tickets_reviewed hub links.
  docs/retro/input.md: D13 — RE-POINT: read the Censura verdict from the tickets' local `<TICKET-ID>_handover.md` (not Notion comments); previous retro = local file; LESSONS.md unchanged.
  docs/retro/discussion.md: D13 — check refs; align any Notion-comment / token references.
  docs/retro/output.md: D13 — output = local retro file mirroring the retro template; frontmatter `content: retro`, `retro_n` (start 1, increment — read prior retro), `phase` (project phase), `verdict` (the retro template's own vocabulary — NOT Censura GREEN/RED), `tickets_reviewed: [[<TICKET-ID>]]`; `Retroactio.md` as the retro MOC; remove the Notion child page.
  docs/retro/session-starter.md: D13/D8 — local retro file refs; token `<TICKET-ID>`.

OUT OF SCOPE (do not do):
  - Touch any consuming project (Foodoire), or create/ship any template file.
  - Create or renumber Notion tickets; change ticket properties.
  - Resolve POC/BUG handover-chain ROLES (owner-deferred — leave the structure, do not assign roles).
  - Commit or push.
  - Modify the MAIN folder-note (v1.5.md) or sibling sub-docs — master-only.

REPORTING:
  - Report at the end of each PASS (files touched, anything ambiguous).
  - Fill ONLY this sub-md's "## Changes Made" section. Flag any out-of-scope discovery for the master; do not act on it.

## Changes Made

Single-agent run, 4 ordered passes. Transport/convention swap (Notion work-trace → local hub + `<TICKET-ID>_output.md` + `<TICKET-ID>_handover.md`); form follows the real FDP-36 files, content follows PoC D1–D15. Edited in place — structure/length preserved. 35 files touched; no out-of-scope files modified; no commit/push.

### PASS 1 — Foundations + agent mandates (9 files)
- `docs/skills/ticket-comment.md` (D2/D8) — retitled to HANDOVER BLOCK protocol; transport → append a `---`-delimited block to `<TICKET-ID>_handover.md`; added APPEND MECHANICS (executor creates file w/ `up:`+`content/handover` frontmatter + `## <TICKET-ID> Handover Chain` + `*Append-only.*`; locate last `---`; block header `### <Agent> — <verdict> | <date>`; session_id via `echo $CLAUDE_CODE_SESSION_ID`, `unknown` if unset); field contract preserved verbatim; `impl_doc` → local `<TICKET-ID>_output.md` path; append-only constraint added.
- `docs/skills/git-workflow.md` (D8) — `feature/DEV-XXX-slug` → `feature/<TICKET-ID>-slug` (example `FDP-N`); resolution line added; `DEV-XXX` demoted to legacy alias; open + detect commands re-tokenised.
- `docs/agents/senate.md` (D7/D9/D10) — Censura verdict → LESSONS.md then handover block (not Notion comment); backfill invariant noted; ALLOWED TOOLS gained scoped Write/Edit to work_documents vault, Notion MCP narrowed to Censura TICKETING; NEVER refined (never modify SPQR process files/CLAUDE.md; never delete; append/add-new; kept "never write code" + "never run shell commands").
- `docs/agents/praetor.md` (D7/D2/D3/D11/D8) — added HUB + WORK-TRACE section (creates hub, writes `_output.md`, appends handover, revisions → `_output_revN.md`); branch token; ALLOWED TOOLS Write scope extended to vault + `echo` Bash; Notion narrowed to read ticket definition; SENSITIVE OP + NEVER refined per D10.
- `docs/agents/tribunus.md` (D10/D2) — added scoped Write to handover file only; Read/Notion re-pointed to local; NEVER refined.
- `docs/agents/probator.md` (D10/D2) — same pattern; kept read-only build/test Bash; handover Write only.
- `docs/agents/curator.md` (D10/D2) — handover verdict block + hub session row Write; Read/Notion re-pointed; NEVER refined.
- `docs/agents/quaestor.md` (D7/D10/D2/D3) — added HUB + WORK-TRACE (SPIKE/DOC executor); ALLOWED TOOLS Notion-write → vault Write/Edit + `echo` Bash; "never edit docs/" → never edit SPQR process files, MAY write the ticket's vault files.
- `docs/agents/session-starters.md` (D8) — TICKET ID resolution note + executor-creates-hub-at-session-start; `TICKET-XXX`/`DEV-XXX` → `<TICKET-ID>`; tab names + Praetor pre-step re-tokenised.

### PASS 2 — OPUS skill chain (12 files)
- `praetor-input.md` (D2) — LOAD ORDER reads ticket + local handover/output; Consilium comment → Consilium handover block; halt-rule + approach-block wording.
- `praetor-output.md` (D3/D2/D6/D7) — OUTPUT DOC = local `_output.md`; HUB creation + session row (cost_total owner-filled); TICKET COMMENT → HANDOVER BLOCK; impl_doc → local path.
- `praetor-impl-doc.md` (D3/D14) — becomes the `_output.md` spec: minimal frontmatter (`up:` + `content/implementation-doc`); `---`-delimited section form per FDP-36; removed `--- TRIBUNUS/PROBATOR/CURATOR NOTES ---`; fill/constraint rules updated.
- `praetor-revision.md` (D11/D14) — delta → local `_output_revN.md` (frontmatter `up:`+`content/implementation-doc`+`rev: N`); veto read from handover; dropped Notion "Delta Doc"; removed NOTES-preservation refs; HANDOVER BLOCK + local paths.
- `praetor-discussion.md` (D8) — `[TICKET-ID]` → `<TICKET-ID>`.
- `tribunus-input.md` (D2/D14) — LOAD ORDER local; OUTPUT DOC load from local path; findings recorded in handover (no NOTES).
- `tribunus-output.md` (D2/D6) — veto/clean-pass/findings → handover block; hub session row added.
- `probator-input.md` (D2) — LOAD ORDER local; OUTPUT DOC local; results recorded in handover.
- `probator-output.md` (D2/D6) — veto/clean-pass → handover block; hub session row.
- `curator-input.md` (D2) — LOAD ORDER local; OUTPUT DOC local; verdict recorded in handover.
- `curator-output.md` (D2/D6) — verdict → handover block; hub session row.
- `collegium-veto.md` (D11) — veto format = a handover block; added `routing` line; transport language swapped from Notion comment to handover append.

### PASS 3 — Senate + ticketing skills (9 files)
- `consilium-input.md` (D2) — LOAD ORDER ticket + local handover (usually absent — first in pipeline).
- `consilium-output.md` (D2/D7) — handoff → append handover block; hub may not exist yet (executor seeds it); `expected_outputs` moved from ticket-body Handoff into the block; EXPLORACIO two-pass note re-pointed.
- `censura-input.md` (D2) — Law-3 framing → on-disk handover file is the external record; LOAD ORDER + executor output + pre-check re-pointed; NEVER updated.
- `censura-discussion.md` (D2) — load from on-disk handover file (Law 3).
- `censura-output.md` (D2/D6) — verdict → LESSONS.md then handover block; hub session row (Censura session_id `—`, Senate runs no shell); backfill invariant; RED-EXPLORACIO recovery re-pointed.
- `censura-ticketing-input.md` (D9) — added NUMBERING + TYPE (central Notion-assigned, Foodoire→FDP-N; `Ticket type` field; plain-description titles); Notion ticket creation KEPT.
- `censura-ticketing-discussion.md` (D9) — REJECT finding → handover; creation stays Notion.
- `censura-ticketing-output.md` (D9) — `Ticket type` field + plain titles + central Notion-assigned numbering; REJECT protocol → handover; NEVER updated.
- `ticket-slicing.md` (D9) — `Ticket type` field + plain titles; central Notion-assigned numbering; REJECT → handover; NEVER updated; Quaestor "no prefix/number" title rule retained.

### PASS 4 — Spike/DOC/BUG + Retro (10 files; discussion.md reviewed, no edit)
- `quaestor-relatio.md` (D2/D3) — Consilium handover block; DOC detection via `Ticket type`=Doc; FETCH STRATEGY → local file-write verification.
- `quaestor-relatio-output.md` (D3/D6) — spike output = local `_output.md` (frontmatter `up:`+`content/spike-document`, no top metadata block); hub creation; Notion parent-page indirection removed; file-write-failure fallback; HANDOVER BLOCK + hub session row.
- `spike-document.md` (D3) — structure = spec minus top metadata block (hub owns identity); minimal frontmatter; file-write-failure handling; NEVER → keep `up:` hub link.
- `quaestor-doc-execute.md` (D12) — DOC output = local change-manifest (`up:`+`content/change-manifest`+`modifies:` property; items DONE/FLAGGED, files/sections, ⚠️ flags); DOC detection via `Ticket type`; closing Notion comment → handover block + hub session row.
- `doc-maintenance.md` (D12/D4) — flags live in handover blocks; Curator scans handover for ⚠️ (not Notion comments); CLAUDE.md flag flow unchanged but handover-sourced.
- `debugging-tribunus-input.md` (D15) — BUG standalone; Notion ticket comment optional → local handover optional; BUG chain roles noted owner-deferred.
- `retro/retrospector.md` (D13) — PRODUCES = local retro file (frontmatter + `tickets_reviewed` hub wikilinks; `Retroactio.md` MOC); reads Censura verdict from local handover; ALLOWED TOOLS gained scoped vault Write/Edit, Notion narrowed to template-structure fetch; NEVER refined.
- `retro/input.md` (D13) — previous retro = local file via `Retroactio.md`; Censura verdict block from local handover; session_id → frontmatter; NEVER updated.
- `retro/output.md` (D13) — output = local retro file; frontmatter `content: retro`, `retro_n` (start 1, increment via prior retro), `phase`, `verdict` (template's own vocabulary, not Censura GREEN/RED), `tickets_reviewed: [[<TICKET-ID>]]`, `session_id`; `Retroactio.md` MOC; Notion child page removed; description line fixed.
- `retro/session-starter.md` (D13/D8) — tickets-in-scope + previous-retro re-pointed local; `<TICKET-ID>` token; FLOW → local retro file.

### Flags for the master (out-of-scope discoveries / inferences — not acted on beyond noting)
- **Senate has no shell access.** senate.md keeps "never run shell commands" (brief did not direct adding Bash). Consequence: Consilium/Censura cannot capture `$CLAUDE_CODE_SESSION_ID`, so their handover/hub session rows record `—` — matches the FDP-36 exemplar and is consistent with D6. No conflict; left as-is.
- **Cross-brief inference on REJECT transport.** `censura-ticketing-output.md` and `ticket-slicing.md` REJECT findings were redirected Notion-comment → handover block. The per-file brief for `-output` didn't name REJECT, but the `-discussion` brief says "REJECT finding → handover" and D2 forbids work-trace Notion comments. Ticket *creation* stays Notion (D9). Flagging the inference.
- **Content-tag naming coined.** Used `content/spike-document` (spike output) and `content/change-manifest` (DOC output) by analogy to the FDP-36 `content/implementation-doc` / `content/handover` / `content/ticket-hub` tags. No exemplar existed for these two; chosen for consistency. Confirm against the Foodoire vault tag vocabulary if one is canonical.
- **Retro template source untouched.** retro/output.md still fetches the Notion `[RETRO_TEMPLATE_ID]` for section structure; only the output write and previous-retro read went local (faithful to "transport swap, don't reship templates"). If the retro template itself is migrating local, that's a separate change (CONFIGURE.md is out of scope here).
- **CONFIGURE.md not updated.** It still documents the old token set (`DEV-XXX`, 4 separate `*_TEMPLATE_ID`s, `[RETRO_PARENT_ID]`, Notion-comment assumptions) and was out of scope for this group. The `<TICKET-ID>` placeholder, the `Ticket type`-field template model, and the removed `[RETRO_PARENT_ID]`/`[SPIKE_DOC_PARENT_PAGE_ID]` indirections will need a CONFIGURE.md/token-catalogue reconciliation in a later group.
