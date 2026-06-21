---
name: warehouse-usage
description: Owner-facing usage + doc-regime guide for the knowledge warehouse — the who-runs-which-CLI matrix (D2), how to run an owner semantic-audit pass, the maintenance-session cadence, and the warehouse-primary doc-regime switch-over (E1). Reference, not enforcement.
---

PURPOSE
The owner-facing companion to the warehouse. The robot specs
(`warehouse_robot/docs/{QUERY,WRITE,AUDIT,NODE_FORMAT}_PROTOCOL.md`) are the
enforcement authority; the per-agent query/ingest skills are the producer
contracts. This file is the OWNER's map: who is allowed to run which verb, how
to run the touches that are yours alone, when to run them, and what
"warehouse-primary" means for the flat docs. It states no new policy — it
collects the SAW-31 decisions (D2/D3/D6/E1) in one owner-readable place.

`[WAREHOUSE_ROOT]` is the warehouse root path; `[ANTECHAMBER_ROOT]` defaults to
an `antechamber` sibling (A3). (Catalogue note: `[WAREHOUSE_ROOT]` rides the
pending CONFIGURE.md token-catalogue reconciliation — Group-9 discovery F1 — to be
added before first propagation; it is not re-discovered here.)

## 1. Who-runs-which-CLI matrix (D2)

The model (D2, owner-confirmed): **agents READ and PROPOSE freely; the privileged
verbs are agent-EXECUTED only on explicit owner HITL.** The gate + the Senate's
per-proposal judgment is the control — not a propose-whitelist. The owner HITL is
CONSENT, not keystrokes: the owner approves, the agent executes (refined 2026-06-21).

> **Glossary — "owner-operated" / "owner-driven" = owner-AUTHORIZED** (the G7/G4
> consent-gate): the agent executes the CLI on that authorization — it does NOT mean
> the owner types the command. This is the canonical definition; the term may stand
> as-is elsewhere.

| Verb(s) | Plane / effect | Who runs it | Authorization |
|---|---|---|---|
| `open-scope` · `find` · `fetch` · `traverse` · `verdict` | read (+ trace round) | each agent, per its `--archetype` | none beyond the budget dial — read is free within the window |
| `grant` | refresh the budget window (consent-gate) | agent-executed | explicit owner HITL — one-shot, consumed on the next round |
| `propose` · `revise` | write to the **antechamber** queue (not the warehouse) | authoring agents (Praetor, Quaestor, Censura, Probator-narrow) | free — the hard-gate + Senate judgment is the control |
| `resolve … ingested/rejected/revise` | apply a Senate verdict; ingest burns the id + writes the markdown truth | agent-executed (Senate judges) | explicit owner HITL — **per-proposal** (`--proposal-key K`), never bulk all-or-nothing |
| `audit` | emit structural flags onto the audit plane | agent-executed at session start | explicit owner HITL — D6 hook 1; emits flags = a write |
| flag `resolves` (clear a handled flag) | write a `resolves` edge onto the audit plane | agent-executed sweep | explicit owner HITL — D3; the retro SURFACES, it does not write |
| `reconcile` · `check` · `reconcile-antechamber` | rebuild / divergence-check the derived index | owner / maintenance | owner-run; no semantic judgment |

Notes:
- **Read ⊥ write.** The `scrutinize` archetype (Tribunus, Probator, Curator) governs READ blindness (the SCRUTINIZE DENY hides `supersedes`/`derived-from`/`about` + `include_inactive`) — it does NOT bar a narrow propose right. Probator keeps one narrow authoring act (the CORRECTIO close lesson, D2c); Tribunus and Curator read but do not author.
- **The Senate's "Never run shell" is amended** to permit the warehouse CLI (read + propose freely; `resolve`/`grant` only on explicit owner HITL). "Never write code/source" and "never modify SPQR process files" still stand.
- **Three distinct acts, never conflated** (PoC clarification): `audit` (robot detects → emits flags) · retro harvest (reads open flags + heat → trend) · flag-sweep (`resolves` closes a handled flag). The owner-driven sweep is NOT the audit.

## 2. How to run an owner semantic-audit pass

The structural `audit` is graph-shaped only (orphan / relates-to-overuse /
missing-recommended-edge — AUDIT_PROTOCOL). The **semantic / contradiction** audit
is **owner-driven** and its automation is **deferred** (no CLI verb mints it; the
mechanism is per Session 6). Run it by hand when a trigger fires (section 3):

1. **Query wide — one verb per round, each closed with a `verdict` before the next**
   (the intent/verdict bracket; QUERY_PROTOCOL §2). Read the slice under review,
   deliberately including the lineage the structural audit and the scrutinize agents
   cannot see. Open a round with `open-scope`, then close it before the next verb:
   `open-scope --warehouse-root [WAREHOUSE_ROOT] --archetype deliberate --session <id> --intent "semantic-audit <scope>" --scope <scope> --include-inactive`
   → `verdict --warehouse-root [WAREHOUSE_ROOT] --session <id> --verdict INSUFFICIENT-TRAVERSE`.
   **Verdict choice matters** (QUERY_PROTOCOL §2): a **terminal** verdict
   (`FOUND-ENOUGH` / `ABSENT` / `FOUND-UNLINKED`) CLOSES the session — to keep the one
   session open across the verbs below, close each intermediate round with a
   **non-terminal** verdict (`WRONG-ENTRY` / `INSUFFICIENT-TRAVERSE`) and reserve a
   terminal verdict for the final round; alternatively, run each verb under its own
   `--session` (each closed with a terminal verdict). Then walk the reasoning chain
   with `traverse` — **one `--edge-type` per call** (no pipe syntax), a separate round
   each, closing each with a `verdict` before the next. Each `traverse` carries the
   full required flag set, varying only the edge type:
   `traverse --warehouse-root [WAREHOUSE_ROOT] --archetype deliberate --session <id> --intent "semantic-audit <scope>" --id <node-id> --edge-type supersedes`,
   then the same with `--edge-type derived-from`, then `--edge-type about`.
   Including the lineage via `--include-inactive` on the `open-scope` round above
   surfaces superseded nodes — a contradiction often hides in a chain that was never
   properly superseded.
2. **Reason about contradictions.** Read the bodies (`fetch`) and judge: do two
   active nodes assert opposing decisions/constraints? Is a node stale relative to
   a later one it should have superseded? Is a lesson contradicted by practice?
   Close the round with a `verdict` (FOUND-ENOUGH / ABSENT / WRONG-ENTRY as fits).
3. **Resolve the finding the gate-safe way — NEVER a by-hand flag write.** A
   `contradiction` flag is an audit-plane node, and audit-plane nodes are minted
   **only** through the robot's single ID-allocation primitive (AUDIT_PROTOCOL:
   `id_counter` burn → markdown → fold). Writing a flag file by hand = hand-minting
   an id, which violates the ID-monopoly the gate exists to enforce — **do not do
   it.** No CLI verb emits a semantic `contradiction` flag yet (the structural
   `audit` is graph-shaped only); that **flag-emission verb is a named follow-up**
   (a later SAW), not a by-hand workaround. Until it lands, route the finding one
   of two gate-safe ways:
   - **needs a knowledge change** → a **superseding proposal** (a new node that
     `supersedes` the stale one) via `warehouse-ingest.md` — gate-safe, append-only,
     never an in-place edit;
   - **worth tracking but not yet actionable** → surface it to the owner as a
     **note** (outside the graph) until the flag-emission verb exists.

## 3. Maintenance-session cadence

Daemon-free (G7/G4): every maintenance touch runs only when the owner opens a
session and authorizes it. The session-starters live in `agents/session-starters.md`
(D6b owner-driven starters: `audit` run · antechamber pending-check · flag-resolution
sweep · semantic-audit "review this"). Recommended triggers — **the cadence
PARAMETER is parked; no number is minted here:**

- **Session start (Senate):** the Senate (agent) runs `list-pending` (antechamber
  proposals awaiting judgment) + `check` (index/mirror divergence only) and `audit`
  (structural heat) on the owner's session-open authorization (agent-executed on owner
  HITL), surfacing the result into the Senate session (D6 hook 1). `check` is a
  divergence check, **not** a pending lister — `list-pending` is the queue read.
- **At retro:** the retro harvests open flags + heat as a TREND and surfaces them
  (D6 hook 2 / D3) — read-only; the resulting flag-resolution sweep is agent-executed on owner HITL (D3).
- **Semantic-audit pass (section 2):** recommended after a large ingestion,
  before a milestone, or on degrading heat / WRONG-ENTRY signals. The retro
  RECOMMENDS it; the owner runs it.

## 4. Doc-regime switch-over (E1)

The warehouse is the **PRIMARY knowledge authority.** Agents query it for
knowledge — there are **no flat-doc fallback instructions** in the warehouse-aware
agent files; an empty slice is legitimate **ABSENT** evidence (escalate/flag,
never silently fall back to a flat monolith).

- The switch takes effect **post-migration in the consuming project** — once a
  project's knowledge has been migrated into its warehouse instance, its agents
  are warehouse-primary. (This generic-side run is additive capability +
  warehouse-primary instructions; the first project migration is a separate,
  later, owner-run step.)
- **Flat docs are NOT deleted this run.** Physical retirement of the flat-doc
  monoliths (e.g. `LESSONS.md`) is a **separate owner-gated SAW** — the cutover is
  authority-first, deletion-later. Until then the flat docs may physically remain;
  they are simply no longer the authority the agents read from.
