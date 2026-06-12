---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — knowledge base restructuring (target structure per existing file + migration-readiness)

**Document status:** Complete — parent fold-back pending

**Phase:** PoC — Session 5 (depends only on Session 3; ran after Session 4, not in parallel)

**Date:** 2026-06-10

**Usage:** claude-opus-4-8:  19.8k input, 94.5k output, 4.5m cache read, 174.9k cache write ($5.82)

**Session scope:** How the existing knowledge-base files become warehouse nodes — the conventions restructuring axis, the lessons linkage model, the architecture-invariant trace, and the a01–a22 gap-fill. Nothing about storage substrate (S7), write-path governance (S6), or chunking (S8).

**Purpose:** Produce a target structure per existing file and a migration-readiness list, on the fixed Session 3 ontology and Session 4 query contract.

**Status legend:** decided · leaning · mixed · open

---

# Overview

Session 5 maps every existing knowledge-base file (ARCHITECTURE, CONVENTIONS, LESSONS, DATA_MODEL, decisions/a01–a22, INDEX) onto the fixed Session 3 node ontology, producing a per-file target structure and a migration-readiness list. The work was calibrated against the real Foodoire `Docs/` tree, not a second-hand summary. The central reframe: with the typed graph fixed (S3) and the query contract fixed (S4), the old "pick one restructuring axis" question dissolves — the candidate axes are not competitors but orthogonal mechanisms that each map to a different part of the schema. The session also surfaced two pieces of never-explicitly-decided knowledge and one warehouse-boundary line, and produced one fold-back into the Session 3 provenance schema.

# Findings

- [**CONVENTIONS.md**](http://conventions.md/)** is largely a derived projection of the ADRs already.** Roughly two-thirds of its sections trace to an explicit decision (MV/MVVM → A21, error patterns → A14/A13, UX → A3, strings → A6, position → A8, SwiftLint → A22, DI → A07). The operational rule is the ADR's consequence restated. Migration implication: **link (**`**derived-from**`**), do not duplicate.** The no-ADR remainder (JSON blobs, the OSLog rule, the self-chosen naming rules, commit-message format) is surfaced never-decided knowledge that becomes new nodes.
- **The "restructuring axis" question is pre-graph and dissolves.** A prose file needs one organizing axis; an atomic-node graph does not. The four candidate axes become orthogonal mechanisms: provenance → `kind` (S3, fixed); consumer → `scope` + the per-archetype query policy (S4, fixed — not a stored consumer field); derivability → edges (`derived-from` / `constrains`); change-rate → emergent from supersede history (not stored). The real S5 decision is which axis maps to which mechanism, plus the scope vocabulary.
- **A fourth content category exists: code-derivable registry.** Inventory content (the service list, actor-isolation annotations, OSLog categories, most of DATA_MODEL) is neither decision, constraint, nor lesson — it is derivable from the code itself. Keeping it as hand-maintained nodes reintroduces the W2 drift the project exists to kill. It stays out; the lookup falls back to reading code (already possible). This is a removal, not a build task.
- **"Local-first" is an orphan invariant.** Of the three ARCHITECTURE invariants, two trace cleanly to navigation ADRs; "local-first" traces to no dedicated ADR — it is assumed everywhere ([CLAUDE.md](http://claude.md/), ARCHITECTURE topology, DATA_MODEL) but never decided. It becomes a new foundational decision node at migration.
- **Lessons split by **`**about**`**-target along the warehouse boundary.** Project-decision lessons (SwiftLint/A22, RecipeService/A21) carry an `about` edge to an ADR and belong to the project warehouse. SPQR-process lessons (re-verification steps, pre-flight checks) point at no decision — they are generic pipeline knowledge and route out to the SPQR side. The mix exists because lesson ingestion was never governed; that governance is the S6 write-path.
- [**LESSONS.md**](http://lessons.md/)** is the strongest migration candidate** — append-only, one entry per run, already structured (date / ticket / verdict / sentence). Its only gap was linkage, now specified.

# Breakdown

## Topic 1 — Conventions restructuring & scope taxonomy

- **Axis resolution:** provenance → `kind`; consumer → `scope` + query policy; derivability → edges; change-rate → emergent. No axis is a file-partitioning choice anymore.
- **Scope = the thematic top-level cluster tag** and the deterministic `kind`+`scope` filter key of the S4 contract. It is orthogonal to `kind` (a scope holds both decisions and constraints) and coarser than edges.
- **Granularity policy (asymmetric):** merge thin scopes now (logging + code-style + git-workflow → `tooling`), keep the overloaded `data-layer` whole for now; the auto-generated index surfaces bleed (node count per scope) and the S4 faceting handles overflow at query time. Thin scopes are hard to name (determinism loss); overloaded scopes only grow a slice, which is observable.
- **Provisional scope set (illustrative, from a stale snapshot — re-derive at migration, do NOT force-fit):** `naming`, `project-structure`, `architecture`, `service-pattern`, `concurrency`, `dependency-injection`, `data-layer`, `localization`, `error-handling`, `ux-pattern`, `tooling`.
- **Scope is a controlled vocabulary:** new values are a governed act (S6), not free text, or the deterministic filter fragments. A node's scope is fixed at birth (append-only); re-scoping is a supersede. The vocabulary itself is living, not frozen at migration.
- **Registry gate (split, not delete):** the inventory drops to a code-derived view; embedded decisions inside it (RecipeService scope ceiling, MarkdownService revisit threshold) stay as nodes.

## Topic 3 — Architecture invariants & the node-vs-consequence test

- **Trace result:** "Views never navigate" + "AppCoordinator owns navigation" = one decision node (two faces of one invariant), `derived-from` → A07/A12/A13. "Local-first" = orphan → new foundational decision node, origin `decided`, marked retro-synthesized, no source edge.
- **Node-vs-consequence test (resolves the Topic 1 handoff, applied to every ADR-derived rule):** create a separate node when the rule is (1) independently consumed — especially checklist-loaded by SCRUTINIZE, which S4 denies the ADR lineage — OR (2) synthesized from multiple ADRs (no single home) OR (3) referenced by other nodes; otherwise it stays as the ADR's Consequences prose, no node.
- **Kind:** all three invariants are `kind: decision` (we chose them); `constraint` is reserved for platform-inherited rules (Apple HIG, Swift 6.2 isolation).

## Topic 2 — Lessons linkage model

- `**agent**`** = the subject (erring) agent**, single-valued; the catching agent stays in prose. The field serves the "show agent X's lessons" filter, for which the subject is what matters.
- `**ticket**`** is the traceability handle; the separate **`**run**`** field is dropped** (see fold-back). `ticket` + `agent` reconstruct the SPQR session via the tab-name convention `TICKET-XXX — Agent`; the full ticket→session-id map lives in Obsidian, not the warehouse.
- `**verdict**`** (GREEN/YELLOW/RED) is a structured field.**
- `**about**`**-target classification:** project-decision lessons → `about` edge to the ADR (project warehouse); SPQR-process lessons → tag `spqr-process`, route out of the project warehouse (preserved as retro fuel, not deleted). The exact SPQR-side destination is parked.
- **Unlinked process-lesson = gap-signal** (a lesson requesting a mandate change never captured as a decision) — handled as the S4 FOUND-UNLINKED / S6 antechamber pattern, not force-linked via `relates-to`.

## Per-file target structure

| Source file | Target state | How / nodes | Edges |
| --- | --- | --- | --- |
| [ARCHITECTURE.md](http://architecture.md/) | Dissolves | Topology = descriptive, no node. 3 invariants → 2 nodes: navigation invariant (1 node), local-first (new orphan node) | nav node `derived-from` → A07/A12/A13; local-first has no source edge |
| [CONVENTIONS.md](http://conventions.md/) | Atomic nodes | 16 sections → decision/constraint nodes by scope; ~2/3 trace to ADRs (link, don't duplicate); no-ADR sections = new never-decided nodes | ADR-derived rules `derived-from` / `constrains` → ADR; node-vs-consequence test per rule |
| CONVENTIONS — registry parts | Out / split | Service list, actor-table annotations, OSLog categories → code-derived view; embedded decisions stay nodes | — |
| DATA_[MODEL.md](http://model.md/) | Registry-dominant → mostly out | `@Model` code is code-derivable; embedded decisions already are ADRs (A04, A09, A16) | decisions already in decisions/ |
| [LESSONS.md](http://lessons.md/) | Lesson nodes + classification | `kind: lesson`; `agent`/`ticket`/`verdict` fields; one-time split project-lesson vs `spqr-process` (route out) | project-lesson `about` → ADR; process-lesson unlinked = gap-signal |
| decisions/a01–a22 | Gap-fill (prototype) | ID `a`→`n` remap (food-nNN); provenance backfill (origin=decided, timestamp=ADR date, run/agent=migration marker); rewrite inline refs | add `supersedes` (A06/A21/A22 candidates); receive `derived-from` from CONVENTIONS + invariants |
| decisions/[INDEX.md](http://index.md/) | Removed → auto-generated | Manual A1…A22 list → robot projection from frontmatter; doubles as bleed monitor (node count/scope) and feeds S4 K8 scoped-TOC | — |

## Migration-readiness list

- ID `a`→`n` remap + inline reference rewrite.
- Provenance backfill convention for historical ADRs (run/agent unknowable → migration marker).
- Add `supersedes` edges (read all 22 ADRs for supersede relations).
- Build the auto-generated index (replaces [INDEX.md](http://index.md/)); it is also the bleed-monitoring surface and an S4 input.
- Re-derive the scope vocabulary against real content (the provisional set is illustrative — do not force-fit).
- LESSONS classification: project vs `spqr-process` (~19 entries, roughly half each).
- Drift fixes found in the live docs: `DECISIONS.md` phantom reference in DATA_MODEL (should be `decisions/`); duplicate `App/` line in the CONVENTIONS folder tree; manual INDEX maintenance.

# Recommendations

- **Closes for Session 5:** the conventions restructuring axis (axes → mechanisms + scope), the lessons linkage model, the architecture-invariant trace, the a01–a22 gap-fill plan. Fold these into the parent direction table (D row, conventions/lessons sub-status).
- **Pending Session 3 fold-back (applied):** the provenance `run` field is dropped; `ticket` is the external run-handle. Confirmed at S5; the S3 doc is amended accordingly.
- **Provisional-scope guard (mandatory):** the scope list is an illustrative draft from a stale snapshot. Re-derive it against actual content at migration. Do not force-fit content into these scope names; if reality differs, the scope list changes, not the content.
- **Do now:** treat CONVENTIONS migration as a linking exercise against existing ADRs, not a re-authoring exercise.
- **Defer:** the SPQR-warehouse destination for process-lessons (parked); write-path governance that prevents future lesson-mixing (S6); the optional code-derived registry view (only if reading code proves too expensive).

# Descoped

- Storage substrate, the markdown-vs-DB reconciliation, and the auto-index engine — Session 7.
- Write-path / antechamber governance and flag lifecycle (the fix for ungoverned lesson ingestion) — Session 6.
- Ingest chunking / atomic-splitting procedure — Session 8.
- The project-warehouse vs SPQR-warehouse boundary (where process-lessons land) — parked strategic lane.

# References

- Session 3: Node Schema & Graph Ontology (fixed ontology — universal node + 3 kinds, edges, provenance; amended here for `run`→`ticket`)
- Session 4: Query Interface Contract (fixed — `kind`+`scope` deterministic filter, per-archetype policy, SCRUTINIZE DENY)
- Session 2: Node Structure, Query Interface & Knowledge Base Restructuring (K3/K4/K5 origin)
- Session Roadmap: Open-Question Map & Critical Decisions (sibling)
- Foodoire `Docs/`: [ARCHITECTURE.md](http://architecture.md/), [CONVENTIONS.md](http://conventions.md/), [LESSONS.md](http://lessons.md/), DATA_[MODEL.md](http://model.md/), decisions/a01–a22 + [INDEX.md](http://index.md/) (the real source, calibrated against)
- SPQR AGENT_LAWS — Law 3 (external record is truth) underpins the fold-back rule