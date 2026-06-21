---
up: "[[v1.5]]"
group: "Warehouse Cutover — observers + usage/doc-regime (SAW-31)"
order: 10/10
saw: [SAW-31]
ticket: SAW-31
status: pending
type: brief
tags: [group, warehouse, cutover, brief]
---

# Group 10 — Warehouse Cutover: state observers + owner usage/doc-regime

## Brief
GROUP:          Warehouse Cutover — observers + usage/doc-regime (SAW-31)
ORDER:          10/10 (SAW-31 execution session 2 of 2 — Agent B)
REPO:           SPQR (generic; A18 generic-first)
RUN_CONTAINER:  /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:        /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/10-warehouse-cutover-observers-docs.md
RATIONALE:      The warehouse-state observers (handoff traceability + retro audit-reader) + the owner-facing usage/doc-regime layer; depends on Group 9 (the propose action + ingest skill it traces/documents).
SOURCE_OF_TRUTH: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md  (D3, D4, D6 + clarifications; DERIVE, do not re-decide)
FILL_CHANGES_MADE: yes

PRE_FLIGHT (load in order):
  - docs/upgrade/execution.md
  - .claude/rules/AGENT_LAWS.md
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md
  - warehouse_robot/docs/QUERY_PROTOCOL.md            (trace §8 → the warehouse_trace pointer; SCRUTINIZE rule context)
  - warehouse_robot/docs/AUDIT_PROTOCOL.md            (the flag plane + heat + open/resolved-derived the retro reads; the `resolves` write the owner sweep applies)
  - docs/spqr_self/upgrades/v1.5/09-warehouse-cutover-agent-layer.md   (dependency: the ingest skill + propose action this group traces/documents)
  - docs/spqr_self/upgrades/v1.5/06-detection-health-sensors.md        (the SAW-27 retro-reader pattern this mirrors — derived-at-harvest, no standing store)

DEPENDENCY GATE: Group 9 GREEN (the ingest skill + the propose action exist; the `audit`/`check` verbs exist in `warehouse_robot/`). STOP if Group 9 is not complete or any referenced verb is absent.

## Scope — build exactly this (PoC D3, D4, D6 + clarifications)

## FILES (4)
  docs/skills/ticket-comment.md: **D4 LEAN.** Add an immutable `warehouse_trace:` field to the handover field contract (session-id / last-round ref, or `n/a`) — keep the brevity floor (one line; do not bloat the block). Extend the **SAW-26 `receipt:` discipline** to cover warehouse-write claims: a `propose`/`resolve` claim carries its verbatim CLI verdict line (= "verification-on-handoff"). **Do NOT add a mutable `antechamber:` status field** — roundtable D4: it is stale-by-construction in an append-only file; current pending state lives authoritatively in the antechamber queue (`check` / the session-starter pending-check).
  docs/retro/retrospector.md: add **audit-flag harvest** — at retro time, read the open flags + per-node heat (from `audit` / the derived `v_flag_status`) and interpret as TREND across markers (mirror the SAW-27 derived-counter pattern: derived-at-harvest, **NO standing store**); add the **semantic-audit "review this" prompt** (owner-driven, recommended triggers: post-large-ingestion / pre-milestone / on degrading heat or WRONG-ENTRY signals; cadence parameter parked); **surface** open flags for the owner-HITL flag-resolution sweep (D3 — the retro surfaces, it does NOT write `resolves`).
  docs/retro/input.md: load order gains the audit flag/heat read (`audit` JSON / `check`); preserve the no-standing-store guard and the existing git boundary.
  docs/skills/warehouse-usage.md: **NEW** — owner-facing usage doc: (1) the **who-runs-which-CLI matrix** (read/propose = agents; `resolve`/`grant`/`audit`/flag-`resolves` = agent-executed on explicit owner HITL — D2); (2) **how to run an owner semantic-audit pass** (query the warehouse incl. `include_inactive` + `traverse` → reason about contradictions → emit a `contradiction` flag; mechanism per S6, automation deferred); (3) the **maintenance-session cadence** (recommended triggers; parameter parked); (4) the **doc-regime switch-over (E1)**: the warehouse is the PRIMARY knowledge authority — agents query it, NO flat-doc fallback instructions; the switch takes effect post-migration in the consuming project; flat docs are NOT deleted this run (retirement = a separate owner SAW).

## Scope fence — do NOT do (flag if found, per Law 1)
- Do NOT have the retro WRITE to the warehouse (no `resolves`; the retro is read-only/vault-only — D3). The flag-resolution sweep is owner-HITL, executed via the Group-9 session-starter maintenance starter / the Senate path.
- Do NOT add a standing telemetry store (SAW-27 guard holds — derived-at-harvest only).
- Do NOT edit the project-side `retro_template.md` (G2 — that trend/flag section is propagation-deferred to Foodoire, not a generic file here).
- Do NOT touch agent/ingest/session-starter files — those are Group 9 (no file-ownership split).
- Do NOT build the full semantic-audit automation or any Foodoire content.

## Changes Made

**Status:** COMPLETE — 4 files (3 edited + 1 NEW). No commit (owner commits). DEPENDENCY GATE verified GREEN before any edit.

### Dependency gate (verified, not assumed)
`python3 -m warehouse_robot --help` confirms every referenced verb exists: `init · check · reconcile · open-scope · find · fetch · traverse · verdict · grant · propose · revise · resolve · reconcile-antechamber · audit`. Pinned the verbs I reference to reality: `audit --warehouse-root P` (only flag; exit 0 clean / 1 findings / 2 error; JSON carries `open_flag_count` + `heat`); `check --warehouse-root P [--antechamber-root]` (divergence + antechamber); query verbs are hyphenated and take `--archetype/--session/--intent` (`--include-inactive` on open-scope/find/fetch). Group 9 (the ingest skill + propose action this group traces/documents) is COMPLETE/GREEN per its Changes Made — the trace + receipt-extension + flag-reader rest on real surfaces.

### Per-file

- **docs/skills/ticket-comment.md (D4 LEAN).** Added the immutable `warehouse_trace:` field to FORMAT (the query `--session` id / last-round ref, or `n/a`) + a FIELD RULES entry: a one-line pointer, not a transcript — round detail lives in the trace table, write proof in `receipt:`. **Extended the canonical `receipt:` discipline** to warehouse-write claims: a `propose`/`revise`/`resolve` claim carries its verbatim CLI verdict line (`<command> → <state + proposal key>`) — verification-on-handoff; warehouse-write producers = Praetor/Quaestor/Censura/Probator-narrow + Senate-on-owner-HITL `resolve`; noted Censura now carries a warehouse-write receipt for its lesson proposal though it produces no build/test receipt. Updated the FORMAT receipt hint + CONSTRAINTS ("…/warehouse-write claim"). **Did NOT add a mutable `antechamber:` status field** (roundtable D4: stale-by-construction in an append-only block; authoritative pending state lives in the antechamber queue / `check` / session-starter pending-check) — and added an explicit CONSTRAINT barring it. Brevity floor preserved (one line per added field).

- **docs/retro/retrospector.md.** READS now names the warehouse open-flag/heat read as a further derived-at-harvest input (read the flag plane; never run `audit`; never write `resolves`). New **AUDIT-FLAG HARVEST (SAW-31 / D3 / D6 hook 2)** section, modelled on the SAW-27 derived-counter pattern (derived-at-harvest, NO standing store): (1) read open flags + per-node heat from the derived `v_flag_status` / the owner's session-start `audit` JSON; (2) interpret as TREND across markers (orphan / relates-to-overuse / missing-recommended-edge counts + heat direction), narrative not a threshold, with the same Goodhart guard; (3) **SURFACE** open flags + heat as candidates for the owner-HITL sweep — the retro does NOT write `resolves`; (4) the owner-driven **semantic-audit "review this" prompt** (recommended triggers: post-large-ingestion / pre-milestone / degrading heat or WRONG-ENTRY; cadence parameter PARKED). ALLOWED TOOLS gains the read-only flag/heat read and a Bash bar on any flag-emitting/write verb; two NEVERs added (never run `audit`; never write `resolves`/any node/flag).

- **docs/retro/input.md.** LOAD ORDER gains item 5 — the warehouse audit flag/heat read (owner session-start `audit` JSON / `v_flag_status`; read-only, derived-at-harvest, no standing store; read the flag plane only, never run `audit`; skip if the warehouse is not in use), renumbering discussion.md to 6. SCOPE BOUNDARY extended: the flag/heat read is the same derived-at-harvest shape as the SAW-27 counters (IN scope; reads + surfaces, never `audit`/`resolves`); the no-standing-store guard and the git boundary are preserved verbatim. New NEVER barring `audit`/`resolves` from the retro.

- **docs/skills/warehouse-usage.md — NEW.** Owner-facing usage + doc-regime guide, four sections: (1) the **who-runs-which-CLI matrix** (D2 — agents read + propose freely; `grant`/`resolve`/`audit`/flag-`resolves` agent-executed on explicit owner HITL; `resolve` per-proposal never bulk; the three distinct acts audit/harvest/sweep kept separate; read ⊥ write, Probator's one narrow authoring act, the Senate "Never run shell" amendment); (2) **how to run an owner semantic-audit pass** (query wide incl. `--include-inactive` + `traverse` over lineage → reason about contradictions → record a `contradiction` flag; mechanism per S6, **automation deferred** — by-hand audit-plane write until a verb exists; a real contradiction → superseding proposal via warehouse-ingest, never in-place edit); (3) the **maintenance-session cadence** (daemon-free; session-start / retro / semantic-audit triggers; cadence parameter PARKED, no number minted; cross-refs `session-starters.md` D6b); (4) the **doc-regime switch-over (E1)** — warehouse PRIMARY, no flat-doc fallback, empty slice = legitimate ABSENT; switch takes effect post-migration in the consuming project; flat docs NOT deleted this run (retirement = a separate owner SAW). Uses the `[WAREHOUSE_ROOT]`/`[ANTECHAMBER_ROOT]` token convention with a pointer to the pending CONFIGURE catalogue item (Group-9 F1; not re-discovered).

### Scope fence — honoured (verified)
- Retro does **not** write to the warehouse — no `resolves`, no node/flag emission; it reads + surfaces only (grep-confirmed the guards in READS, ALLOWED TOOLS, NEVER on both retro files).
- No standing telemetry store added — derived-at-harvest only; the SAW-27 guard wording preserved.
- **Did NOT edit the project-side `retro_template.md`** (G2 — propagation-deferred to Foodoire). Only `retro/input.md` + `retro/retrospector.md` touched.
- **Did NOT touch agent / ingest / session-starter files** (Group 9 ownership) — `git status` confirms exactly my 4 files changed.
- Did NOT build the full semantic-audit automation or any Foodoire content (the semantic-audit pass is documented as owner-driven, automation explicitly deferred).
- No mutable `antechamber:` field added (D4 LEAN) — grep-confirmed.
- No git commit/push.

### Design note for the master (Law 4)
The brief's phrasing "read … from `audit` / the derived `v_flag_status`" carries a latent tension: running `audit` **emits** flags (an id-burn write) and is the owner's session-start act (D6 hook 1) — it is not a read. To keep the retro strictly read-only/vault-only (its identity + the D3 fence), I implemented the harvest as a **read of the already-derived flag/heat state** (the owner's session-start `audit` JSON / `v_flag_status`), and added explicit guards that the retro never runs `audit`. This is consistent with the PoC's three-distinct-acts clarification (audit ≠ harvest ≠ sweep); flagging it so the wording is read the same way downstream (e.g. when this propagates to Foodoire's `retro_template.md` trend section).

### Out-of-scope discovery (report only — Law 1/Law 4)
- The semantic-audit pass needs to **record a `contradiction` flag**, but the structural `audit` verb emits only the three graph-shaped tripwire types — there is **no CLI verb to emit an owner/semantic flag**. The PoC says "mechanism per S6, automation deferred," so I documented it as a by-hand audit-plane write for now. When the owner wants this operational, a small `flag` (or `audit --semantic`) emission verb is the natural follow-up SAW — surfaced for the master, not acted on here.
