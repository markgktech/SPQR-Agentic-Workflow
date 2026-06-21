---
type: poc
title: "SAW-31 Warehouse Cutover — PoC"
decides: "How SPQR agents/skills are re-wired to consume the warehouse (warehouse-primary): archetype mapping, who-runs-which-CLI, audit wiring, handoff & query-policy contracts"
status: done         # draft | done
date: 2026-06-21
tags: [poc, decision, warehouse, saw-31]
---

# SAW-31 Warehouse Cutover — PoC

## Context / question
SAW-31 is the generic-side cutover that makes the SPQR agents/skills **warehouse-primary**: every agent queries the warehouse for knowledge (instead of loading flat-doc monoliths), hot-path agents propose new knowledge through the write gate, the Senate session-starter surfaces pending antechamber items + audit heat, and the handoff carries warehouse state. The warehouse build (B1–B5) is GREEN; this PoC settles the cutover decisions. Scope confirmed at the SCOPE GATE (see SAW-31 ticket comment 2026-06-21). Warehouse = **PRIMARY authority immediately**, no flat-doc fallback instructions; flat-doc physical deletion is a separate later SAW (owner-gated). Runs **before** propagation+migration (A18 order) so warehouse-aware agents propagate once.

Sources: `warehouse_robot/docs/{QUERY,WRITE,AUDIT,NODE_FORMAT}_PROTOCOL.md`; Session 6 (write path/audit), Session 4 (query), 07-Planning Decisions (G7/G4/G5/G8 + A1–A18). Related: [[SAW-27 Detection-Health Sensors — PoC]] (retro-as-reader pattern this reuses), [[SAW-29 Bug Pipeline — PoC]].

## Decision items (Phase 3 — PoC-first; PROPOSED = my position, not yet owner-confirmed)

### D1 — Archetype ↔ agent mapping
**PROPOSED:** deliberate=Senate · execute=Praetor · synthesize=Quaestor · scrutinize=Tribunus/Probator/Curator (given by QUERY_PROTOCOL §4) · **consult = no current agent** (parked strategic lane — Execution Plan parked: "strategic lane J, CONSULT, I, Curator").
**Sub-question D1b:** does Senate's **Censura** (post-execution review) query as `deliberate` (sees lineage) or `scrutinize` (blind to the reasoning chain)? PROPOSED: **deliberate** — QUERY_PROTOCOL §4 names the blind-scrutinize set as exactly Tribunus/Probator/Curator and excludes Senate; Senate is the authority that issues verdicts/ingests, not a blind re-deriver.
**Why:** the five archetypes map cleanly to the six agents with consult left parked; matches the spec's explicit scrutinize set.
**Affected:** all 6 `docs/agents/*.md` (the `--archetype` self-declaration), the query-policy block.
**Status:** OPEN

### D2 — Who-runs-which-CLI matrix + NEVER reconcile (the cutover spine)
**PROPOSED matrix:**
| Operation | Runner | Note |
|---|---|---|
| query verbs (read) + `verdict` | each agent, per archetype | needs read-CLI right; **amend Senate "Never run shell"** narrowly |
| `propose` / `revise` (antechamber) | hot-path producers (Praetor, Quaestor; reviewers per D-tbd) | needs propose right + ingest skill |
| `resolve` (apply Senate verdict) | **OWNER** (Senate judges + surfaces; owner executes at session start) | G7/G4 + B4 "resolve owner-operated" |
| `grant` (consent) | **OWNER only** | consent act |
| `audit` (structural) | **OWNER** at session start | session-starter hook |
| flag `resolves` (clear flag) | **OWNER** sweep (retro surfaces, does not write) | D3 |
| `reconcile` / `check` | OWNER / maintenance | |
**NEVER reconcile (PROPOSED):** amend Senate `senate.md` "Never run shell commands" → "…except the read-only warehouse query CLI"; reviewers' "never write code" is untouched (a proposal is not source code, but if reviewers propose knowledge they get a narrow `propose` right — confirm which reviewers author knowledge). Retro stays read-only (does not run `resolves`; owner does).
**Why:** the no-shell intent was "reviewers/Senate don't run builds/tests/git" — a read-only knowledge query is not that; privileged writes stay owner-operated to preserve the daemon-free G7/G4 model and Senate's write-restraint.
**Affected:** ALLOWED TOOLS + NEVER in all agent files; `session-starters.md`.
**Status:** OPEN

### D3 — Flag-resolution (`resolves`) runner
**PROPOSED:** OWNER-operated sweep; the retro SURFACES open flags/heat but never writes (preserves retrospector read-only/vault-only NEVER). Automatable later.
**Affected:** `retro/retrospector.md`, `session-starters.md`.
**Status:** OPEN

### D4 — Handover field contract (trace + antechamber state)
**PROPOSED:** add 2 brevity-capped optional fields to `skills/ticket-comment.md`: `warehouse_trace:` (session-id / last-round ref or n/a) and `antechamber:` (pending proposal keys+state or none). SAW-26 `receipt:` discipline EXTENDED to cover warehouse write claims (propose/ingest CLI output line) — that IS "verification-on-handoff."
**Affected:** `skills/ticket-comment.md` (field contract + brevity floor), producers/enforcer.
**Status:** OPEN

### D5 — Query-policy block mandatory elements
**PROPOSED:** a shared block + per-archetype dial values, referencing QUERY_PROTOCOL as the enforcement authority (no prose duplication). Mandatory elements: `--archetype`/`--session` self-declare · intent/verdict bracket discipline (one open round; close with verdict) · budget dials (usage reference) · SCRUTINIZE DENY (scrutinize agents only) · ABSENT handling (empty slice = legitimate ABSENT, escalate/flag, never auto-broaden) · BudgetExhausted → escalation packet → owner `grant` loop.
**Affected:** all 6 agent files; new `skills/warehouse-ingest.md` cross-ref.
**Status:** OPEN

### D6 — Audit cadence hooks
**PROPOSED:** exactly two hooks, no third standing mechanism — (1) session-start: owner runs `audit`, heat surfaced (mirrors antechamber pending-check); (2) retro: harvest flags+heat → trend (mirror SAW-27) + the semantic-audit "review this" prompt + owner flag-resolution sweep. Cadence parameter PARKED (no minted numbers).
**Affected:** `session-starters.md`, `retro/retrospector.md`, `retro/input.md`.
**Status:** OPEN

## Findings from execution (Group 9, 2026-06-21)
- **F1 — `[WAREHOUSE_ROOT]` placeholder not catalogued in CONFIGURE.md** (out-of-scope discovery). Rides the existing deferred "CONFIGURE.md token-catalogue reconciliation" item (stale catalogue; propagation derives `spqr.config` from it). Propagation-prep, downstream — not this run. Owner adds it to the Variable Catalogue + `spqr.config` before first propagation.
- **F2 — Probator D8 close-write vs scrutinize (D2c gap).** Probator writes routine knowledge to the sink at bug close (SAW-29) but D2c only converted Censura's LESSONS write → proposal, and the brief scoped probator.md to query-block-only. Agent correctly flagged, did not act (Law 1). **Resolution principle (proposed):** the scrutinize archetype governs READ blindness (the DENY), NOT write — read-archetype ⊥ propose-right. So Probator = scrutinize-on-read **+** propose-right for its close-write (lesson-node proposal), mirroring Censura D2c. Also check Curator for the same pattern. **D2c is EXTENDED** to cover every agent that authored knowledge to a flat sink, not just Censura. Fix = a small Group-9 follow-up pass on `probator.md` — same file-ownership surface. **Owner chose FIX-NOW (2026-06-21)** → Group 9b brief + starter created. **Curator verified NOT affected** (it writes verdict blocks to the local vault, not knowledge nodes to the warehouse) → probator.md ONLY. `resolve`/`grant` stay Senate+owner-HITL; Probator gains only `propose`/`revise` for the close lesson.

- **F3 — D2c consistency leftovers (independent Codex review, 2026-06-21).** Two gaps the master A10 missed, caught by Codex — the 9b probator.md change was not propagated to two related files:
  - `warehouse-ingest.md:16-18` — proposer list omits Probator + the "scrutinize agents do not author" blanket contradicts 9b. → add Probator (CORRECTIO close lesson only); correct the blanket (Tribunus/Curator still non-authoring).
  - `bug-pipeline.md:46` — sink still "today LESSONS.md; soon the Warehouse" → reconcile to warehouse-primary (close entry = lesson-node proposal via the ingest skill).
  Lesson: the F2/9b scope fence ("probator.md ONLY") was too narrow — a propose-right change must sweep every file that asserts the proposer set or the sink. → **Group 9c** (2-file closure). Tribunus/Curator verified correctly non-authoring (no change). All other Codex checks (1–4, 6, CLI-reality, query-block byte-identity, SCRUTINIZE DENY distribution, fence) GREEN.

- **F4 — Group-10 validation gate (independent Codex, 2026-06-21; verified against code/files).** Six-point holistic pass; #2 GREEN. Real findings:
  - **#1** `ticket-comment.md` receipt example used the transient `validated`; `propose` returns `pending-senate` (write_gate.py:448-451). → fix example.
  - **#3** `warehouse-usage.md` session-start line "owner runs audit" contradicts its own matrix + final D2. → agent-runs-on-owner-HITL.
  - **#4** stale "OWNER executes the ingest" survived the D2 refinement in `praetor.md`, `quaestor.md`, `warehouse-ingest.md` (11/99), `censura-output.md` (56). → "the Senate runs `resolve` on owner HITL." (`senate.md:62` already correct.)
  - **#6** `warehouse-usage.md` semantic-audit how-to violates the intent/verdict bracket + uses non-real `--edge-type a|b|c` pipe syntax. → bracket per verb + one `traverse --edge-type` per call.
  → folded into ONE consolidated amendment ([[10-amend-saw31-final-consistency]]) per the validate-before-confirm rule. **Exhaustive close:** the 10-amend pass-1 still left D2-stale "owner-run" instances (the refinement landed mid-run; per-finding patches kept missing some). A master corpus-wide grep (agents+skills+retro) found exactly four more — session-starters.md:23, warehouse-usage.md:86, retrospector.md:39, input.md:11 — fixed in [[10-amend-b-d2-phrasing-exhaustive]]. **Lesson:** when a decision is refined mid-run, immediately grep the WHOLE corpus for the superseded phrasing — do not patch per-finding. The semantic-audit by-hand lines + the later-owner-run migration step are CORRECT (verified, left as-is).
  - **#5a (DEFERRED → residue sweep):** the retro still treats `LESSONS.md` + its 10-entry counter as the primary signal, but Censura now proposes lesson-nodes to the warehouse. Live contradiction; coupled to the broader LESSONS.md retirement → handled in the post-Group-10 flat-doc residue sweep (the retro's Censura *verdict-block* signal in handovers is intact; only the *lesson sink* moved).
  - **#5b (→ housekeeping ticket):** `ticket-comment.md` `mode:` enum omits CONSILIUM/QUAESTOR/CENSURA (SAW-33-era gap, not warehouse-coupled) → candidate owner SAW, out of SAW-31 scope.

- **F5 — whole-warehouse holistic review (calibrated high-bar Codex, 2026-06-21; all verified against code).** Three GENUINE findings (no nitpicks — the calibration worked):
  - **#1 — the Senate wake pending-check is broken.** `session-starters.md:24` claims `check` "lists proposals waiting on Senate judgment", but `check_antechamber` (write_gate.py:679) is a divergence check (dir vs mirror) — when consistent it reports "clean" and lists NOTHING; and `cli.py` has NO pending-list verb. The wake (a core SAW-31 deliverable, G7/G4) silently misses the ingest queue. **Owner call: BUILD a `list-pending` verb now** (warehouse_robot code) + re-point the session-starter doc to it. Code task [[11-list-pending-verb-build]]; doc fix in the final doc pass.
  - **#2 — the manual contradiction-flag instruction is unsafe.** `warehouse-usage.md` §2 says "by-hand audit-plane write" — but no CLI emits a semantic flag, so by-hand = hand-minting a node file + ID = violating the ID-monopoly the gate exists to enforce. → doc fix: route a contradiction finding through the gate (a superseding proposal) or an owner note; name the flag-emission verb as a follow-up; NEVER a by-hand flag write.
  - **#3 — proposal-key allocation race (data loss).** `_allocate_key` (write_gate.py:309) is max+1 from the dir with NO lock, then `write_text` overwrites (:382) — two concurrent `propose` can collide and one clobbers the other. The id_counter monopoly is transaction-safe; the antechamber key is not. → **warehouse_robot CORRECTIO bug ticket (owner-created)**, out of SAW-31 doc scope (could ride the verb build since same file — owner's call).
  Doc fixes (#1-doc + #2 + the #5a retro lesson-source) consolidated into one final SAW-31 doc pass after the verb lands.

## Recommendation / decision
Filled item-by-item as the owner confirms each D1–D6.

### #decision DECIDED (owner-confirmed 2026-06-21)
- **D2 — DECIDED: "agents read + propose; privileged = agent-executes-on-owner-HITL."** All agents may **read** the warehouse (per-archetype budget). All knowledge-authoring agents may **propose** to the antechamber via the ingest skill (the gate + Senate judgment is the control, not a propose-whitelist). The privileged ops (`resolve` verdict / `grant` / `audit` / flag `resolves`) are **executed by the agent but ONLY on explicit owner authorization (HITL gate)** — *refined 2026-06-21 from "owner mechanically runs it": the G7/G4 gate is owner CONSENT, not owner keystrokes; the owner approves, the agent executes.* `resolve` is **per-proposal** (`--proposal-key K --verdict …`), never bulk all-or-nothing; the CLI is trivially cheap (id burn + markdown + fold, sub-second) — the cost is the Senate's per-proposal semantic judgment, which happens in-session regardless. **NEVER reconcile:** `senate.md` "Never run shell commands" is **amended** to permit the warehouse CLI (read + propose freely; `resolve`/`grant` only on explicit owner HITL) — owner rationale: the no-shell rule existed only to prevent unjustified code modification, now outdated for the warehouse path; misuse stays catchable in owner review. Reviewers' "never write code" untouched (a proposal is not source).
- **D1b — DECIDED: Censura queries as `deliberate`** (sees lineage) — per QUERY_PROTOCOL §4 the blind-scrutinize set is exactly Tribunus/Probator/Curator; Senate is the authority that judges/ingests.

### Write-flow clarification (owner-confirmed mental model + one refinement)
propose (any authoring agent) → robot **hard-gate** (deterministic, cheap; malformed bounces) → **validated, waits in the antechamber QUEUE (decoupled, non-blocking)** → at the **next Senate session start** the session-starter surfaces pending items to the **owner**; the **Senate makes the semantic judgment** (ingest/reject/revise) → the **OWNER runs the actual `resolve` (ingest) CLI** (privileged write: id burn → markdown truth → fold). Refinement vs the owner's phrasing: the Senate **judges/validates**, the **owner executes the ingest**; timing is "next Senate touch via the queue," not strictly "this ticket's end."
- **Concrete consequence (new D-item D2c):** Censura today writes `LESSONS.md` (`senate.md:33`); warehouse-primary makes that a **lesson-node proposal to the antechamber** (via the ingest skill), not a flat-file write. Affected: `senate.md` Censura step, `skills/censura-output.md`.

### Clarifications recorded (owner Q&A 2026-06-21)
- **`consult` archetype = parked, no current agent.** It is a low body-fetch-ceiling query-budget profile reserved for a future strategic/advisor agent (Execution Plan parked "strategic lane J, CONSULT, I, Curator"). Not assigned this run.
- **`scrutinize` ≠ a fix loop.** It is the review-agents' query archetype: they query **blind to the reasoning chain** (the SCRUTINIZE DENY hides supersedes/derived-from/about) so they **independently re-derive** the judgment. The "bad proposal → author fixes & resubmits" loop is the separate write-gate **`revise`** verdict — do not conflate.
- **audit / harvest / sweep are three distinct acts:** `audit` (robot detects → emits flags) · retro harvest (reads open flags + heat → trend) · flag-sweep (`resolves` closes a handled flag). The owner-driven sweep is NOT the audit.
- **Owner-driven warehouse-maintenance session-starters are a concrete SAW-31 output** (new D-item D6b): paste-prompt starter(s) for the owner-run touches — `audit` run, antechamber pending-check, flag-sweep, semantic-audit "review this" — daemon-free, run when the owner authorizes. Affected: `agents/session-starters.md`.

### Phase-3 CLOSED — all items DECIDED (owner-confirmed 2026-06-21)
- **D1 — DECIDED:** mapping deliberate=Senate · execute=Praetor · synthesize=Quaestor · scrutinize=Tribunus/Probator/Curator · consult=parked (no current agent).
- **D3 — DECIDED:** flag-resolve = agent-executes-on-owner-HITL sweep; retro surfaces open flags/heat, does not write.
- **D4 — DECIDED = LEAN-refined** (owner delegated to roundtable; both personas independently → LEAN). Drop the mutable `antechamber:` handover field (stale-by-construction in an append-only file; authoritative state lives in the antechamber queue / `check` / session-starter pending-check). Keep `warehouse_trace:` immutable pointer + the **SAW-26 `receipt:` extension** that explicitly logs the propose action + gate verdict (immutable fact = within-pipeline visibility). Roundtable: 08-roundtable note to be written in the run container.
- **D5 — DECIDED:** query-policy block mandatory elements (archetype/session self-declare · intent/verdict bracket · budget dials · SCRUTINIZE DENY · ABSENT handling · BudgetExhausted→grant loop) — built into the agent files, QUERY_PROTOCOL is the enforcement authority.
- **D6 — DECIDED:** two audit hooks (session-start `audit` + retro harvest/trend) + **D6b** owner-driven warehouse-maintenance session-starters; cadence parameter parked.
