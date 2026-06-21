---
up: "[[v1.5]]"
group: "Warehouse Cutover — runnable-CLI + glossary close (SAW-31)"
order: 10-amend-c/10
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, cutover, brief, amendment]
---

# Group 10-amend-c — runnable-CLI examples + terminology glossary (the FINAL pass)

## Brief
GROUP:          Warehouse Cutover — runnable-CLI + glossary close (SAW-31)
ORDER:          10-amend-c (the final substantive pass — Codex final finding #3; closes the cutover proper)
REPO:           SPQR (generic)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/10-amend-c-runnable-cli.md
RATIONALE:      Owner-facing usability — the semantic-audit how-to's CLI examples are not copy-paste runnable (missing required flags; a generic terminal verdict that would prematurely close the session), and the receipt example reads as literal stdout when the CLI emits JSON. Plus ONE glossary line that ends the "owner-operated" terminology ambiguity (owner deliberately stopped the phrasing treadmill — the meaning is consistent, only one definition is needed).
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md
FILL_CHANGES_MADE: yes

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - warehouse_robot/cli.py                       (the REAL required flags per verb — verify, do not guess)
  - warehouse_robot/docs/QUERY_PROTOCOL.md       (§2 bracket: a TERMINAL verdict closes the SESSION; non-terminal keeps it open)

DEPENDENCY GATE: 10-amend-b GREEN.

## Scope — make the examples runnable + one glossary line. No behaviour change, no new decision.

## FILES (2)
  docs/skills/warehouse-usage.md:
   - §2 semantic-audit how-to — make EVERY CLI example copy-paste runnable, verified against `cli.py`: the `verdict` example needs `--warehouse-root [WAREHOUSE_ROOT]`; the `traverse` examples must show the required flags (not `…`): `--warehouse-root`, `--id <id>`, `--archetype deliberate`, `--session <id>`, `--intent "…"`, `--edge-type <one>`. Fix the verdict semantics per QUERY_PROTOCOL §2: a **terminal** verdict (FOUND-ENOUGH/ABSENT/FOUND-UNLINKED) closes the SESSION — between verbs in one session use a **non-terminal** verdict (WRONG-ENTRY/INSUFFICIENT-TRAVERSE), or run each verb as its own session; replace the generic `<V>` with accurate guidance so an owner following it does not prematurely terminate.
   - Add ONE glossary line (near the matrix, section 1): **"owner-operated / owner-driven = owner-AUTHORIZED (the G7/G4 consent-gate); the agent executes the CLI on that authorization — it does NOT mean the owner types the command."** This is the canonical definition; the term may stand as-is elsewhere.
  docs/skills/ticket-comment.md:
   - The warehouse-write receipt EXAMPLE (`receipt:` def, ~line 28): clarify in one clause that the `→ <state + proposal key>` is the **decisive state+key taken from the CLI's JSON output** (the CLI emits JSON; the receipt records that decisive line) — the arrow is the same readable convention as the build/test receipts, not literal raw stdout.

## Scope fence — do NOT do (flag if found, per Law 1)
- These 2 files ONLY. Do NOT chase "owner-operated"/"owner act" phrasing anywhere else — it is owner-AUTHORIZED framing, now defined by the glossary line (owner's explicit call to stop the phrasing treadmill).
- Do NOT touch the PoC (it is the decision record; it legitimately retains the D2 refinement history).
- Do NOT touch the retro LESSONS.md framing (#5a → residue sweep) or the mode enum (#5b → ticket).
- Do NOT change any decided behaviour, rights, archetype, or the SCRUTINIZE DENY.

## Changes Made

Two-file fix applied. No behaviour change, no new decision. All CLI flags verified against `warehouse_robot/cli.py`; verdict semantics verified against `QUERY_PROTOCOL.md` §2.

### `docs/skills/warehouse-usage.md`
1. **§1 — glossary line added** (blockquote, immediately after the consent-model paragraph where the term is established): *"owner-operated / owner-driven = owner-AUTHORIZED (the G7/G4 consent-gate); the agent executes the CLI on that authorization — it does NOT mean the owner types the command."* Tagged as the canonical definition so the term may stand as-is elsewhere (closes the phrasing treadmill per owner's call).
2. **§2 step 1 — `verdict` example made runnable:** added the missing `--warehouse-root [WAREHOUSE_ROOT]` (it is `required=True` on the `verdict` subparser in `cli.py`).
3. **§2 step 1 — verdict semantics corrected:** replaced the generic `--verdict <V>` with `--verdict INSUFFICIENT-TRAVERSE` plus an explicit "**Verdict choice matters**" note — a **terminal** verdict (`FOUND-ENOUGH`/`ABSENT`/`FOUND-UNLINKED`) CLOSES the session, so between verbs in one session use a **non-terminal** verdict (`WRONG-ENTRY`/`INSUFFICIENT-TRAVERSE`) or run each verb under its own `--session`. Prevents an owner following the how-to from prematurely terminating mid-pass.
4. **§2 step 1 — `traverse` examples made runnable:** replaced the `…` placeholders with the full required flag set verified against `cli.py` (`--warehouse-root`, `--archetype`, `--session`, `--intent`, `--id`, `--edge-type` are all `required=True`), shown once in full and then varied only by edge type (`supersedes` → `derived-from` → `about`). Also re-attributed the `--include-inactive` note to the `open-scope` round, since `traverse` does not accept that flag and ignores the status filter by design (QUERY_PROTOCOL §5) — avoids implying a flag that would error.

### `docs/skills/ticket-comment.md`
5. **Receipt FIELD RULES (line 28) — warehouse-write arrow clarified:** added one clause stating the `→ <state + proposal key>` is the **decisive `state`+key read from the CLI's JSON output** (the write verbs emit JSON, not plain text); the arrow is the same readable `<command> → <result>` convention as the build/test receipts, not literal raw stdout. The canonical receipt definition itself is unchanged.

### Scope fence — honoured
- Touched **only** the 2 briefed files. Did NOT chase "owner-operated"/"owner act" phrasing elsewhere (now defined by the glossary line).
- Did NOT touch the PoC, the retro LESSONS.md framing, or the mode enum.
- No decided behaviour, rights, archetype, or the SCRUTINIZE DENY changed.

### Out-of-scope discovery (reported, not handled — per Law 1 / execution.md)
- `docs/skills/warehouse-ingest.md` RECEIPT (lines 104–107) carries the parallel phrasing "the `propose` CLI stdout line: state + proposal key". Mild residual ambiguity (a "line" of what is JSON), but that file already states **"JSON on stdout"** explicitly at line 83 directly above, so it is materially clearer than the ticket-comment.md spot was. Left untouched (scope fence: 2 files only). Master decides whether a one-clause alignment there is worth a follow-up.
