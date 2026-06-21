---
up: "[[v1.5]]"
group: "Warehouse Cutover — final doc reconciliation (SAW-31)"
order: 12/12
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, cutover, brief, doc-reconciliation]
---

# Group 12 — final doc reconciliation (wake → list-pending · contradiction-safety · retro lesson-source)

## Brief
GROUP:          Warehouse Cutover — final doc reconciliation (SAW-31)
ORDER:          12/12 (the closing SAW-31 doc pass; depends on Group 11 — the `list-pending` verb now exists)
REPO:           SPQR (generic)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/12-final-doc-reconciliation.md
RATIONALE:      Close the three remaining SAW-31 doc issues in one pass: the wake pending-check (F5/#1-doc), the unsafe by-hand contradiction flag (F5/#2), and the retro lesson-source under warehouse-primary (#5a).
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md  (F5, #5a)
FILL_CHANGES_MADE: yes

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md
  - warehouse_robot/docs/WRITE_PROTOCOL.md   (the new `list-pending` verb + states the wake/retro reference)
  - warehouse_robot/docs/AUDIT_PROTOCOL.md   (flag emission is the robot's ID-allocation primitive — never by-hand)

DEPENDENCY GATE: Group 11 GREEN — `list-pending` exists in `cli.py` (the session-starter will point to it). STOP if absent.

## Scope — three reconciliations, no new behaviour beyond pointing docs at reality

## FILES (wake + usage + the retro suite)
  docs/agents/session-starters.md (F5/#1-doc): the WAREHOUSE WAKE pending-check currently calls `check` and claims it "lists proposals" — FALSE (`check` is divergence-only). Re-point to the new verb: `python3 -m warehouse_robot list-pending --warehouse-root [WAREHOUSE_ROOT] --state pending-senate` — lists the proposals awaiting Senate judgment. Keep `audit` for heat.
  docs/skills/warehouse-usage.md (F5/#2 + matrix): in §2, REMOVE the "by-hand audit-plane write, owner-executed" instruction for a contradiction flag — a hand-written flag node = hand-minting an id = violating the ID-monopoly the gate enforces (AUDIT_PROTOCOL: flags are emitted only through the robot's ID-allocation primitive). Replace: a contradiction that needs a knowledge change becomes a **superseding proposal** via `warehouse-ingest.md` (gate-safe); a contradiction worth tracking but not yet actionable is surfaced to the owner as a note. NAME the missing flag-emission verb as a follow-up (no by-hand write). Also reconcile any `check`-as-pending-lister reference to `list-pending`.
  docs/retro/retrospector.md + docs/retro/input.md + docs/retro/session-starter.md (+ light: output.md, discussion.md) (#5a): under warehouse-primary, Censura writes lessons to the warehouse (not LESSONS.md), so the retro's LESSONS.md framing is stale. Reconcile: the **PRIMARY lesson signal is the Censura verdict blocks in the per-ticket handovers** (intact, always available); **new lessons live as warehouse lesson-nodes** (queried post-migration when the warehouse is populated); **LESSONS.md = historical / pre-cutover lessons, read-only** (not the live sink). Re-base the "retro-due counter" from "LESSONS.md 10-entry" to **Censura-verdict-block count since the last marker** (LESSONS.md no longer grows) — still a SIGNAL, owner still starts the session. Keep the no-standing-store guard + the SAW-27 derived-at-harvest discipline unchanged.

## Scope fence — do NOT do (flag if found, per Law 1)
- Do NOT delete LESSONS.md (retirement = separate owner SAW); it stays as the historical read.
- Do NOT touch warehouse_robot code, the agent query-policy blocks, or any decided right/archetype.
- Do NOT build a standing telemetry store (SAW-27 guard holds).
- Do NOT chase "owner-operated" phrasing (closed by the glossary).

## Changes Made

Dependency gate verified GREEN before any edit: `list-pending` exists in `warehouse_robot/cli.py` (parser at :259–:272, handler `cmd_list_pending` at :490 → `write_gate.list_pending`). Proceeded.

### Reconciliation 1 — wake → `list-pending` (F5/#1-doc)
`docs/agents/session-starters.md`:
- **SENATE PRE-STEP — WAREHOUSE WAKE** (line 23–24): re-pointed the antechamber pending-check from the broken `check` (a divergence-only check that lists nothing when consistent) to `python3 -m warehouse_robot list-pending --warehouse-root [WAREHOUSE_ROOT] --state pending-senate`. Updated the lead-in ("the Senate agent runs `list-pending`/`audit`") and added an explicit note that `check` is dir-vs-mirror divergence, NOT a pending lister — do not use it for the wake. `audit` kept unchanged for heat.
- **D6b WAREHOUSE MAINTENANCE → ANTECHAMBER PENDING-CHECK** (line 77–79): same `check`-as-pending-lister defect in the same file — re-pointed to `list-pending --state pending-senate`, with the `check`=divergence-only clarifier. (Same defect class as F5/#1; fixed for in-file consistency rather than leaving a self-contradiction.)
- The SEMANTIC AUDIT block was already gate-safe (superseding proposal via the antechamber, no by-hand write) — left as-is, per F4's verified note.

### Reconciliation 2 — contradiction-flag safety (F5/#2) + `check`→`list-pending`
`docs/skills/warehouse-usage.md`:
- **§2 step 3**: REMOVED the "by-hand audit-plane write, owner-executed" instruction. Replaced with a NEVER-by-hand rule grounded in AUDIT_PROTOCOL (audit-plane nodes are minted ONLY through the robot's single ID-allocation primitive — a hand-written flag = hand-minting an id = violating the ID-monopoly). The semantic-`contradiction` flag-emission verb is NAMED as a follow-up (a later SAW), not a by-hand workaround. Until it lands, a finding is routed two gate-safe ways: (a) needs a knowledge change → **superseding proposal** via `warehouse-ingest.md` (append-only, gate-safe); (b) worth tracking but not yet actionable → surfaced to the owner as a **note** outside the graph.
- **§3 Session-start (Senate) bullet**: reconciled the `check`-as-pending-lister phrasing — now `list-pending` (antechamber proposals awaiting judgment) + `check` (index/mirror divergence only) + `audit` (structural heat), with the `check`≠pending-lister clarifier. The §1 matrix row for `check` was already correct (divergence/rebuild) — untouched.

### Reconciliation 3 — retro lesson-source under warehouse-primary (#5a)
Re-based the retro suite off the stale LESSONS.md-as-live-sink framing. Principle applied uniformly: PRIMARY lesson signal = Censura verdict blocks in the per-ticket handovers (always present, warehouse or not); new lessons = warehouse lesson-nodes (read post-migration where populated); LESSONS.md = historical / pre-cutover, read-only, no longer growing. The retro-due counter re-based from "LESSONS.md 10-entry" → Censura-verdict-block count since the last marker — still a SIGNAL, owner still starts the session.
- `docs/retro/retrospector.md`: TRIGGERS #2 (counter re-based to Censura-verdict-block count); READS (Censura verdict blocks promoted to PRIMARY, LESSONS.md → historical read-only, new lessons → warehouse lesson-nodes); ALLOWED TOOLS Read line (LESSONS.md tagged historical/read-only, Censura block = primary). AUDIT-FLAG HARVEST + the no-standing-store / SAW-27 derived-at-harvest guards left UNCHANGED.
- `docs/retro/input.md`: LOAD ORDER #2 (LESSONS.md → historical read-only, points the live signal to item 4 + warehouse lesson-nodes); LOAD ORDER #4 (Censura verdict block marked PRIMARY); SCOPE BOUNDARY metrics line (Censura findings = primary, LESSONS.md = historical read-only). The standing-telemetry-store NEVER guard left unchanged.
- `docs/retro/session-starter.md`: TRIGGER NOTE counter re-based (LESSONS.md 10-entry → Censura-verdict-block counter).
- `docs/retro/output.md` (light): RULE-ROT PASS evidence source → "Censura verdict blocks / historical LESSONS.md".
- `docs/retro/discussion.md` (light): phase-1 findings list → "Censura findings, historical LESSONS.md patterns".

### Scope fence — honoured
- LESSONS.md NOT deleted (verified present at `docs/LESSONS.md`) — retirement remains a separate owner SAW.
- No `warehouse_robot` code, no agent query-policy blocks, no decided right/archetype touched.
- No standing telemetry store built (SAW-27 guard intact in retrospector.md + input.md).
- No "owner-operated" phrasing chased (closed by the glossary).

### Verification
- Dependency gate: `list-pending` present in `cli.py` (parser + handler).
- Post-edit grep: no remaining `check`-as-pending-lister claim (all `check` mentions now explicitly scoped to divergence); the only "by-hand" mentions are in the prohibition itself; `list-pending` now backs both the wake and the D6b pending-check.
- Not committed (owner commits).
