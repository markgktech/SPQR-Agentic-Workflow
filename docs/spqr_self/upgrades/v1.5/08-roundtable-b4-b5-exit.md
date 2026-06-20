---
up: "[[v1.5]]"
group: "Warehouse Initiation — build (B1–B5)"
order: 8/8
saw: [SAW-30]
type: roundtable
phase: 2
tags: [group, warehouse, roundtable]
---

# Roundtable — Warehouse Phase 1 close (B4 + B5 + Exit Check)

## Context
Phase 2 roundtable for the SAW-30 build-closure run: **B4** (write gate), **B5** (audit tripwires), **Phase 1 Exit Check** (independent Probator verification). Two from-scratch personas reviewed the plan against the actual files (Planning Decisions G1–G8/A1–A8, B3 delivery note open questions, Sessions 2/6/7, `warehouse_robot/` code). Primary lens: **agent-actionability** (can a stateless execution agent apply the rule without extra context). Personas ran independently (no cross-contamination). Findings, not approvals — the master synthesises and the owner closes Phase 2.

**Protocol note:** single round. The two independent reviews converged on the blockers and raised **no mutually-contradictory positions**; per the roundtable EXECUTION PROTOCOL a second round runs only on contested/modified content, of which there is none. Justified single-round close (not a silent skip).

---

## Persona 1 — Gyuri (Dev Process Architect) — findings

| # | Area | Finding | Agent-actionable? | Position |
|---|------|---------|---|---|
| G1 | **Two-model collision (blocker)** | Owner's "B4/B5 each a separate execution agent" names the upgrade-agent **brief model**; every on-disk artifact is the warehouse **Starter A** model (agent self-plans, surfaces contradictions, waits for approval, writes a delivery note). Opposite contracts; no doc says which governs. | N | Pick ONE before any session. Lean **Starter A governs** (B1–B3 ran under it; B4 genuinely needs the plan-and-surface phase — see G11–G14). If brief model: master must pre-bake B4's open Qs or it violates Law 2/4. |
| G2 | Hand-off undefined | Who fills the starter `{params}`, where the filled starter + dependency-gate evidence are recorded — unspecified. | N | State hand-off owner + artifact location. |
| G3 | Dependency gate trusts the GREEN token | Gate checks "delivery note exists + says GREEN", not re-derivation; B2 shipped a ~10%-flaky GREEN. | Y(check)/N(sufficiency) | Master **re-runs the prior suite at gate time** — the owner's "master critically re-tests" ask, currently nowhere in the docs. |
| G4 | Verification-loop gap/redundancy | 3 layers (agent tests / master re-test / Probator exit). (b) master re-test has **no artifact, scope, DoD**; overlaps (c). | N | Split: master re-test = bounded smoke re-run of the just-built suite **+ cross-B integration seam**, right after each build session; Probator = whole vertical slice, fresh session, end of B5. |
| G5 | Exit-check independence not enforceable | "Fresh session that didn't build B1–B5" is honour-only (B3 already resumed a warm session across the Fable→Opus break). | N | Make it visible: exit report records its session id, asserts it differs from every delivery-note session id. |
| G6 | A4 isolation — one hole | Helpers use system tmp; instance `.gitignore` covers only `index.sqlite*`, not stray node/antechamber markdown — which B4 writes. Negative check names only `warehouse/`, not antechamber. | Y | Mandate system-tmp; negative check must include the **antechamber** dir. |
| G7 | A4 vs B4 antechamber isolation | "Disposable instance" language never says the antechamber sibling is part of the disposable unit; agent could pollute canonical `project_memory/antechamber/`. | N | One line: disposable unit = warehouse root **+ its antechamber sibling**, same tmp parent, deleted together. |
| G8 | **Receipt rule not bound (blocker-ish)** | SAW-26 receipt rule is authored for the product pipeline only; Starter A never references it. B3 §4 **paraphrases** ("171 tests") which the receipt rule explicitly forbids. | N | Add verbatim `receipt:` field to delivery-note DoD §4 (decisive `Ran N tests … OK` line). |
| G9 | Anti-flake repeat-run is non-actionable | B2/B3 ran suites 5×–10× as de-facto convention; nowhere in the DoD. Count-based with no count. | N | Promote to DoD: byte/ordering loops ≥5; full suite ≥5× consecutive at close; receipt cites the clean count. |
| G10 | DoD has no teeth on checkpoint comments | B3 skipped mid-checkpoint comments yet exited GREEN; it's the only resume anchor if a session dies. | Y | Enforce (no GREEN without the trail) or honestly downgrade — don't keep a per-session-violated rule. |
| G11 | B4 open-Q: ID allocation vs `id_counter` | `upsert_node` advances counter on every fold incl. reconcile; B4 must allocate from counter not markdown-max; fold re-touch interaction unspecified. | N | Allocate via `UPDATE id_counter … RETURNING` inside the gate txn, write markdown, then fold (max() guard makes re-touch idempotent). State it. |
| G12 | B4 open-Q: trace + antechamber visibility | B3 note recommends (no write-path trace; queries don't see antechamber) but nothing requires a B4 agent to read those recs — they vanish under the brief model. | N | Reinforces G1 → Starter A ("read all prior delivery notes"). |
| G13 | B4 open-Q: `status: retired` write path | `v_effective_status` lets stored `retired` win; but append-only store refuses overwrite → no retire-as-transition mechanism specified. | N | Likely retire = a new superseding node; B4 must surface, not assume. |
| G14 | B5 vs B3 DENY: antechamber-read has no surface | Session 6 wants archetype-conditional antechamber **reads** before proposing; B3 shipped canonical-plane-only queries; no read verb exists. | N | Owner call: antechamber-read = B4 sub-surface or deferred to v1.5 cutover (Phase 3 ingest). B4 scope fence must say which. |
| G15 | **B5 tripwires non-actionable (blocker)** | `relates-to overuse` (count?) and `missing-recommended-edge` (which edges per kind?) have no threshold/table anywhere. | N | B5 must surface as placeholder dials (B3 budget-dial precedent: "pre-calibration, retro sets real values"). |
| G16 | Exit-check A8 environment-binding | Byte compare requires "same Python/SQLite build"; a fresh session on another interpreter fails for an environmental reason, undetectably. Notes record Python but **not SQLite version**. | Y/N | Exit-check asserts `python3 --version` + `sqlite3.sqlite_version` match the recorded receipt; add SQLite version to the receipt. |

**Gyuri clean passes:** dependency DAG correctness (B4→B1,B2; B5→B1–B4 matches real code coupling); A5 git mode internally consistent + G3 enforced in code (no git call anywhere); A8 two-part criterion well-formed and matches `fold.logical_digest`; fixture discipline concrete + versioned (14 nodes + 26 queries on disk).

**Gyuri's block:** G1 gates G2/G4/G12/G13. Resolve to Starter A (or pre-bake the answers) before any session opens.

---

## Persona 2 — Laci (Agentic Trends Expert) — findings

| # | Area | Finding | Agent-actionable? | Position |
|---|------|---------|---|---|
| L1 | **B5 tripwires undefined (blocker)** | Orphan / relates-to-overuse / missing-recommended-edge named in 5 docs, defined in none. A from-scratch B5 agent must invent thresholds — "a flag store with arbitrary thresholds is noise" (the B5-analogue of SAW-40's "stale store worse than none"). | N | Owner fixes 3 measurable predicates before B5 (orphan = 0 in+out edges AND not foundational; overuse = >K relates-to, K stated; missing-recommended = per-kind required-soft-edge table). |
| L2 | **`kind` frozen-enum vs governed-extensible** | `schema.py:50` `CHECK (kind IN (...))` + `store.py` `KNOWLEDGE_KINDS` bake kind into DDL+codec; yet Session 2 K10 chose schema-driven type enforcement, and `scope` (G5) IS governed-extensible. A future kind (SAW-40 convention) = schema migration, not a content add. | N (for the future add) | Don't change now, but B4 must **document the freeze as deliberate** with its cost (seed-level schema bump / A2 re-fold), not deepen it. Flag: is `constraint` already the home for conventions? then no new kind needed. |
| L3 | Write-path has no telemetry | Trace is read-path only (QUERY_PROTOCOL §8 + B4 open-Q#1). No record of proposals-rejected / revise-depth / time-in-pending / auto-ingest-vs-escalation — exactly the promotion-gate + SAW-40 freshness signals. `antechamber.updated_at` is overwritten (no transition history). | Y (minimal hook) | B4 keeps an append-only proposal-event log OR names the blind spot explicitly as the SAW-31/SAW-40 hook. Silent blind spot = the risk. |
| L4 | **Antechamber mirror unverified (blocker)** | Mirror carried over verbatim on rebuild (`fold.py:252`) but **excluded from the A8 digest** (`_DIGEST_QUERIES` L63–71); and not markdown-derivable (proposals live outside warehouse, G6/A3) → divergence check can't see it either. A corrupt mirror — B4's own write-state — is invisible to both exit-check and divergence. | Y | B4 adds antechamber↔mirror reconcile + divergence (mirroring B2) OR defers with reason; exit-check must walk a proposal through the full state machine AND assert mirror == antechamber dir. |
| L5 | New honour seam: proposal `ticket`+`agent` | Session 6 binds in-flight proposals + `revise` wake to self-declared `ticket`+`agent` — the write-path analogue of G8. Spoofable, and a bad write persists as un-ingested content; no provenance trace beyond the overwritten row. | Partial N | Treat as self-declared-logged (G8 posture) AND append-only-visible (ties L3). Confirm B4 builds the archetype-conditional antechamber visibility policy or defers it. |
| L6 | `auto-ingested` scope boundary | DDL already admits `auto-ingested` state (`schema.py:98`); B4 scope says only "antechamber handling". Build-empty-path vs defer the promotion gate is unstated → latent dead-path. | Y | B4 explicitly decides; exit-check catches a DDL-admitted state the code never reaches. |
| L7 | **B5 scope-creep guard (freshness)** | Divergence tracks markdown↔index only, never node↔external-reality. SAW-40's code-vs-convention staleness is owner-driven semantic audit (Session 6 Cluster B), NOT a B5 tripwire. A from-scratch B5 agent reading SAW-40 context could over-build. | Y | B5 ticket carries an explicit fence: "code/convention freshness is NOT a B5 tripwire." B5 stays purely graph-structural. |
| L8 | ID monopoly vs counter | Two ID sources (counter for live allocation, markdown-max for rebuild) are correct but a trap; a fresh B4 agent could read markdown-max and collide. | Y | One-line rule in B4 note; exit-check asserts a crash-skip-gap scenario (S7: unique not gapless). |

**Laci clean passes:** read-path consent-gate / budget / SCRUTINIZE-DENY (deterministic, Law-4-honest); antechamber physical separation G6/A3 (correct — which is *why* L4 matters); append-only + serialized-ID concurrency model (correct-by-construction at v1 volume); G8 read-path honour system genuinely trace-visible; markdown↔index divergence boundary correctly scoped (basis for L7).

**Laci top-3:** L1 (B5 undefined — blocking), L4 (mirror hole exit-check can't see), L2 (kind freeze — at least document the cost). L3/L5 acceptable as *named* deferrals, not silent.

---

## Master synthesis — flat item list for Phase 3

Convergence (both personas, independent) = high confidence. Dispositions are the master's; decisions are made in Phase 3 and recorded as Planning-Decisions amendments (A9+).

| # | Item | Source | Class | Master disposition (position for Phase 3) |
|---|------|--------|-------|-------------------------------------------|
| R1 | **Which execution model governs B4/B5** | G1,G12 | BLOCKER | **Starter A governs the build**, master owns the hand-off + critical re-test. Reconciles "continue existing logic" + "separate execution agent per ticket". Decide first. |
| R2 | **B5 tripwire rules undefined** | G15,L1 | BLOCKER | Define orphan / overuse / missing-recommended as **measurable predicates**, numeric parts as **placeholder dials** (B3 precedent). No B5 session until fixed. |
| R3 | **Antechamber mirror write-state hole** | L4,G14 | BLOCKER | B4 adds antechamber↔mirror reconcile + divergence OR defers-with-reason; exit-check asserts mirror == antechamber dir after a full state-machine walk. |
| R4 | **Master critical re-test layer undefined** | G3,G4 | IMPORTANT | Specify: bounded smoke re-run of the just-built suite **+ cross-B integration seam**, immediately post-build, distinct from Probator's whole-slice exit. This *is* the owner's strengthening ask — wire it into the DoD. |
| R5 | **Receipt rule not bound to the suite** | G8,L3 | IMPORTANT | Verbatim `receipt:` field in delivery-note DoD §4 (decisive `Ran N … OK` line; cite ≥5× clean count). Ends B3-style paraphrase. |
| R6 | B4 open Qs under-specified | G11,G13,L8,L5 | IMPORTANT | Master pre-resolves into the brief / Starter A plan phase surfaces: ID allocation via counter-txn; retire = superseding node; proposal ticket+agent self-declared-logged. |
| R7 | `kind` frozen vs governed-extensible | L2 | NOTE | Don't change now; B4 documents the freeze as deliberate + names the cost (SAW-40 forward). Check if `constraint` already homes conventions. |
| R8 | Write-path telemetry blind spot | L3,L5 | NOTE | Acceptable as a **named** deferral (B4 note names the SAW-31/SAW-40 hook); unacceptable silent. |
| R9 | `auto-ingested` promotion-gate boundary | L6 | NOTE | B4 explicitly builds empty-reachable path vs defers; exit-check catches the dead path. |
| R10 | Anti-flake repeat-run not in DoD | G9 | IMPORTANT | Promote to DoD (≥5× consecutive; receipt cites count). |
| R11 | Exit-check independence + env-binding | G5,G16 | IMPORTANT | Honour-based but visible: assert session-id differs from all delivery notes; assert Python + **SQLite** version match recorded receipt (add SQLite version to receipt). |
| R12 | A4 antechamber isolation under-specified | G6,G7 | MINOR | Disposable unit = warehouse + antechamber sibling under one tmp parent; negative check includes antechamber dir; system-tmp mandated. |

## Open items flagged for new tickets (owner creates — no ID minted here)
- **Antechamber↔mirror reconcile** — if R3 is deferred rather than built in B4, it is its own ticket (a B2-analogue divergence check for the antechamber plane).
- **Write-path telemetry / proposal-event log** (R8) — rides the SAW-31 cutover or SAW-40; candidate ticket if wanted standalone.
- **`kind` extensibility governance** (R7) — rides SAW-40 (is convention a new kind or `constraint`); flag only.

## Points to update (which file, when)
- **Phase 3 → Planning Decisions amendments (A9+):** R1, R2, R6, R7, R9 (decisions).
- **Phase 4 → B4 / B5 execution briefs + delivery-note DoD:** R3, R4, R5, R10, R11, R12 (the strengthened test + verification contract).
- **Exit-check (Starter B) addenda:** R3 (mirror assert), R11 (session-id + version match), R12 (antechamber negative check).
