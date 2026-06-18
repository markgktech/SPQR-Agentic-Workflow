---
up: "[[v1.5]]"
group: "Receipt rule — verbatim tool evidence for build/test/lint claims"
order: 5/5
saw: [SAW-26]
tags: [group]
---

# Group 5 — Receipt rule (SAW-26)

## Brief
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/05-receipt-rule.md
REPO:          SPQR (generic only this run; Foodoire via SAW-38 propagation, sequenced separately)
RATIONALE:     One coherent surface — bind every build/test/lint claim to verbatim tool evidence across the producer (Praetor/Probator) + enforcer (Censura) skill files and the shared handover protocol.
SOURCE_OF_TRUTH: this file (lean run — no separate PoC; decisions inlined below — owner-authorized stage-depth reduction; see [[v1.5]] process-debt "PoC-first step")
PRE_FLIGHT:
  - .claude/rules/AGENT_LAWS.md
  - docs/skills/ticket-comment.md   (shared handover protocol — canonical receipt field lands here)
  - docs/skills/praetor-output.md
  - docs/skills/praetor-impl-doc.md
  - docs/skills/probator-output.md
  - docs/skills/probator-input.md
  - docs/skills/censura-input.md
  - docs/skills/censura-output.md
FILES:
  - docs/skills/ticket-comment.md: add canonical `receipt:` field to FORMAT + FIELD RULES + cost-guard CONSTRAINT (scoped decisive-line definition, whitelist). DO NOT touch the "Max 12 lines" cap (`:2` / `:29`) — that is R1, handled by the master at session-end after the owner picks A/B. The compact receipt line fits within the existing cap, so no conflict.
  - docs/skills/praetor-impl-doc.md: add a `**VERIFICATION (RECEIPT)**` section to the output-doc template (home for verbatim build/lint decisive lines).
  - docs/skills/praetor-output.md: require VERIFICATION receipt in `_output.md` + compact `receipt:` line in the handover block; add CONSTRAINT.
  - docs/skills/probator-output.md: clean-pass/handover must carry `receipt:` with the verbatim test decisive line; add CONSTRAINT.
  - docs/skills/probator-input.md: TEST SUITE RUN — capture the verbatim decisive line for the receipt.
  - docs/skills/censura-input.md: PRE-CHECK — verify a receipt is present for every build/test/lint claim in the trail.
  - docs/skills/censura-output.md: enforcement — no GREEN without receipts; missing receipt = HITL flag + cheap producer bounce (NOT a standalone veto); real build/test failure routes the existing veto/RED path; add to NEVER.

## Decisions
<!-- #decision — lean run: decisions inlined here (no separate PoC), per owner -->

- **D1 — Producer / enforcer split.** Praetor produces `build` + `lint` receipts (runs Bash during implementation); Probator produces the `test` receipt (the tester). Censura **cannot** produce a receipt — Senate runs no shell — so Censura is the **enforcer**, not a producer. This refines the ticket's "Praetor/Probator/Censura output" framing (the three are not symmetric producers).
- **D2 — One canonical definition, no duplication.** The receipt format is defined once in the shared handover protocol (`ticket-comment.md`) as a `receipt:` field; the producer/enforcer skills reference it rather than each restating it.
- **D3 — Scoped to the decisive line, not the full log.** A receipt = `<command> → <decisive stdout line>` (e.g. `BUILD SUCCEEDED`, `Executed 42 tests, 0 failures`, `0 violations`). Verbatim, not paraphrase. **Marked: good for now; if the steady-state cost or under-specification surfaces later, refine** (e.g. exit codes, fuller output). Whitelist: build succeeded · tests ran + result · lint zero-warnings.
- **D4 — Cost-guard (C6 fold-in).** The receipt is a quality floor — never omitted to save tokens. Stated as a CONSTRAINT in the producer skills and enforced by Censura. Skipping a receipt is visible and bounced; that visibility is the deterrent (no nuclear veto needed).
- **D5 — Physical home (brevity-driven, not cap-driven).** Placement is driven by a brevity/signal discipline, NOT by the old hard "12 line" cap (which is Notion-era residue — see RESIDUE FINDING). Praetor's verbatim build/lint receipt lives in `_output.md` (`**VERIFICATION (RECEIPT)**`) because bulk detail belongs in the output doc; the handover `receipt:` carries only the compact decisive line(s). Probator has no output doc (D14) → its decisive test line goes directly in the handover `receipt:` field (one line — terse).

## Residue finding (adjacent — owner-authorized session-end fix, no full process)
- **R1 — "12 line" handover cap is Notion-era residue.** `ticket-comment.md:2` ("Max 12 lines") + `:29` ("Never exceed 12 lines in the block body") preserve a cap whose original reason (Notion comment size limit) was removed by the SAW-33 Notion→local-file transport swap. The cap survived only because SAW-33 preserved the field contract "verbatim" (line 3) without re-examining the cap. Referenced descriptively in `retrospector.md:26` (says cap does not apply to retro — reconcile that mention too).
  - Proposed fix (owner to pick A/B): **A (recommended)** — replace the hard "12 line" number with a brevity *principle* ("terse routing/signal record; detail belongs in the output doc; no fixed line count"). **B** — remove the cap outright.
  - **RESOLVED (master, session-end, 1-on-1):** Option **A** applied — `ticket-comment.md:2` + `:29` reframed to a brevity principle (terse routing/signal record; detail → output doc; no fixed line count); `retrospector.md:26` mention reconciled ("block-brevity discipline"). Lightweight inline fix per owner; filed retroactively for traceability as **SAW-39** (https://app.notion.com/p/38368d5de1e88199b898f2f15b4bad2e).
  - **R2 (LOW, resolved same pass):** `censura-input.md` LOAD ORDER did not load `ticket-comment.md` though enforcement references its canonical receipt definition → added as LOAD ORDER item 6 (Censura is enforcer only, no shell). Fold under the same owner SAW ticket.
- **D6 — Missing receipt = HITL flag + cheap bounce, NOT a standalone veto.** A missing receipt is a clerical omission, not a code failure; a full veto/revision cycle (the pipeline's costliest path) is disproportionate. Censura flags the gap; the producer re-attaches the line. Recovery exploits a warm/resumable producer session when available (cheap); falls back to an owner-started fresh session if not (owner-run). A receipt showing an **actual** build/test failure is a real failure and routes through the **existing** Probator-veto / Censura-RED machinery — no new teeth built. Correctness does not depend on session liveness (receipt captured at source, mandatory field); warm-session resume is a cost optimization, not a dependency.
- **D7 — Scope this run: generic SPQR only.** Foodoire receives the rule via the SAW-38 propagation mechanism, sequenced separately (the first Foodoire v1.3→v1.5 propagation is itself still pending). No hand-edits to Foodoire in this run. Generic skill files are CORE surface → they propagate.
- **D8 — Enforcement stays at Censura only (scope-faithful).** Catching a missing receipt only at the final Censura stage is acceptable because the bounce is cheap (D6) — so no need to expand enforcement to Tribunus/Curator. Keeps the ticket's original target scope intact.

## Changes Made — CHECKPOINT 2

Generic SPQR only (D7). No Foodoire / consuming-project files touched; MAIN folder-note (v1.5.md) and sibling sub-docs untouched; no git commit/push. Praetor/Probator agent files read as FORM reference only — confirmed Bash + write scope (praetor.md:42, probator.md:38) and that Senate runs no shell (censura-output.md:18), so the producer/enforcer split (D1) is form-faithful. They were NOT edited.

### 1. docs/skills/ticket-comment.md — canonical `receipt:` field (D2)
- FORMAT: added a `receipt:` line (producer-only, between `impl_doc` and `routing`) pointing to FIELD RULES for the scoped definition.
- FIELD RULES: added the ONE canonical definition of `receipt:` — verbatim `<command> → <decisive stdout line>`, NOT paraphrase; scoped to the decisive line not the full log; whitelist (build succeeded · tests ran + result · lint zero-warnings); producers = Praetor (build+lint) / Probator (test); Censura is enforcer-only (no shell); physical homes (Praetor → output VERIFICATION + compact handover line; Probator → handover line directly); producer-only field.
- CONSTRAINTS: added cost-guard C6 line — never omit a receipt to save tokens (quality floor); missing receipt bounced at Censura.
- **Did NOT touch the "Max 12 lines" cap** (`:2` + the "Never exceed 12 lines" constraint) — that is R1, owner-pending. The compact receipt line fits within the existing cap.

### 2. docs/skills/praetor-impl-doc.md — `**VERIFICATION (RECEIPT)**` template section (D5)
- TEMPLATE: added a new `**VERIFICATION (RECEIPT)**` section (between TEST COVERAGE and KNOWN GAPS) with `build:` / `lint:` verbatim decisive-line slots + a pointer that the canonical definition lives in ticket-comment.md and the compact line also goes in the handover.
- FILL RULES: added a VERIFICATION (RECEIPT) entry (mandatory on any build/lint claim, verbatim, never paraphrased, never omitted to save tokens).
- CONSTRAINTS: added "Never omit VERIFICATION (RECEIPT) on a build/lint claim".

### 3. docs/skills/praetor-output.md — produce build/lint receipt (D1/D4/D5)
- OUTPUT DOC (D3): added instruction to fill VERIFICATION (RECEIPT) with verbatim build/lint decisive line(s); bulk detail in the output doc, compact line in the handover.
- HANDOVER BLOCK Required fields: added `receipt:` (compact verbatim build/lint line; full block in output VERIFICATION).
- CONSTRAINTS: added cost-guard C6 line — never omit the build/lint receipt.

### 4. docs/skills/probator-output.md — produce test receipt (D1/D4/D5)
- CLEAN PASS: added a line — carry the verbatim test receipt in the handover `receipt:` field (Probator has no output doc, D14 → the decisive test line lives directly there).
- HANDOVER BLOCK Required fields: added `receipt:` (verbatim test decisive line, e.g. `Executed 42 tests, 0 failures`).
- CONSTRAINTS: added cost-guard C6 line — never clean-pass/handover without the verbatim test receipt.

### 5. docs/skills/probator-input.md — capture test receipt at source (D3)
- TEST SUITE RUN: added a line — capture the verbatim decisive output line of the run as the receipt carried into the handover; copy exact, not paraphrased; canonical definition referenced (ticket-comment.md).

### 6. docs/skills/censura-input.md — enforcer PRE-CHECK (D6/D8)
- PRE-CHECK: added a "Receipt presence" check — enforcer role (Senate runs no shell, verifies not produces); for every build/test/lint claim confirm a verbatim receipt is attached at its physical home; missing = HITL gap + cheap producer bounce, NOT a standalone veto (D6); a receipt showing an actual failure routes the existing veto/RED machinery.
- NEVER: added "Never accept a build/test/lint claim without its verbatim receipt — but missing = producer bounce, not veto; Censura never produces it (no shell)".

### 7. docs/skills/censura-output.md — enforcement verdict rules (D6/D8)
- Added a `RECEIPT ENFORCEMENT` block after VERDICT OPTIONS: no GREEN without receipts; missing = HITL flag + cheap producer bounce (NOT a standalone veto, D6); a receipt showing an ACTUAL failure routes the existing Probator-veto / Censura-RED machinery (no new path); enforcement lives at Censura only (D8 — Tribunus/Curator do not check receipts).
- NEVER: added "Never set GREEN while any build/test/lint claim lacks its verbatim receipt …".

### Verification
- 12-line cap (R1): `grep -n "12 line" docs/skills/ticket-comment.md` → `Max 12 lines.` (line 2) + `Never exceed 12 lines in the block body` — both VERBATIM, unchanged (line shifted 29→31 only because two CONSTRAINT lines were appended above it). Not touched, per brief.
- Receipt threading present in all 7 files: `grep -rc "receipt\|RECEIPT"` → ticket-comment 3 · praetor-impl-doc 4 · praetor-output 3 · probator-output 3 · probator-input 1 · censura-input 2 · censura-output 6.
- Producer/enforcer split (D1) form-faithful: receipt-PRODUCTION added only to Praetor (build/lint) and Probator (test) skills; Censura received only enforcement (presence-check), never production. No new veto/RED path added (D6). No receipt checks added to Tribunus or Curator (D8).
- Canonical definition stated ONCE (D2): full definition in ticket-comment.md FIELD RULES; the other six files reference it, none restate it.
- Scope: generic SPQR only — no Foodoire, no MAIN folder-note, no sibling sub-docs, no git commit/push.

### Out-of-scope discovery (flagged for master — not acted on)
- None beyond the already-recorded R1 residue finding (the 12-line cap), which is owner-pending and handled separately by the master per the brief.
