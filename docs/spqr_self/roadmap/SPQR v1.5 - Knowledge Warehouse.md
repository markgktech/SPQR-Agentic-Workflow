---

---
## Metadata

| Field | Value |
| --- | --- |
| Created | 2026-06-12 |
| Created by | Mark + Claude |
| Version | v1.0 — Big picture |
| Status | Direction fixed — PoC arc (S1–S8) closed; pre-build |
| Position | Between v1.3 (baseline, committed) and v2.0 — Semi-Automated Pipeline (unchanged) |

---

## Executive Summary

v1.5 replaces the knowledge substrate under the still-manual pipeline. It is **not** an automation step — the owner remains the orchestrator, every stage stays owner-triggered. What changes is how the system stores, retrieves, and protects project knowledge: instead of agents loading monolithic prose documents "just in case," a git-native **knowledge warehouse** serves exactly the knowledge each agent needs, through a deterministic zero-token robot layer.

v2.0 (Semi-Automated Pipeline) keeps its place and its content. v1.5 exists *because* of it: automation routed over a drifting, expensive, vendor-welded knowledge layer would automate the wrong thing faster. v1.5 is the floor v2.0 stands on.

---

## Why — the three business pressures

- **Token cost scales with the wrong things.** Agents carry whole convention/architecture documents in context regardless of the task, and prose retrieval over MCP is expensive and non-deterministic. Knowledge becomes pay-per-need: scoped queries, skeleton-first, bodies only on explicit selection; everything judgment-free runs in a deterministic robot at zero token cost.
- **Decision drift erodes trust in the record.** Decisions made mid-pipeline don't reliably flow back to the source of truth, so the record goes stale and self-contradictory — and a record you can't trust costs review time on every ticket. The warehouse removes drift structurally: one gated write path, append-only decisions, state derived rather than edited.
- **Vendor lock-in deepens by default.** Machine-truth living in Notion and a Claude-runtime-shaped workflow tie the system to tools that should be replaceable. The warehouse is plain markdown + an embedded, disposable SQLite index — portable, diffable, no server, no platform ownership of the truth.

---

## What — in broad strokes

| # | Item | What it is |
| --- | --- | --- |
| 1 | The warehouse | Git-native document graph: universal nodes (decision / constraint / lesson), typed edges, append-only with derived status; markdown = source of truth, SQLite index = derived and disposable |
| 2 | The robot | Deterministic zero-token layer: scoped query interface (skeleton → selective fetch → bounded traversal), gated write path (proposal → validation → Senate judgment → ingest), audit tripwires that flag and never mutate |
| 3 | Migration | One-time load of the existing project knowledge (~830 lines) — faithful extraction plus owner-led backfill of decisions that were made but never written |
| 4 | SPQR cutover | Agents query instead of loading monoliths and propose instead of editing docs; per-archetype access policies, including a robot-enforced blind spot that protects reviewer independence |
| 5 | Safety regime | Test-run until an explicit owner cutover call: the old flat docs stay intact and authoritative as fallback; full warehouse reset remains possible and cheap |

The independent housekeeping items (SAW-1, 16, 17, 29, model-usage switch, git formalization, telemetry thin layer) ship separately as **v1.4**, in parallel with the build — the cutover update stays clean.

---

## As-Is → To-Be

| Dimension | As-Is (v1.3) | To-Be (v1.5) |
| --- | --- | --- |
| Knowledge load | Monolith files loaded whole, per session, just in case | Scoped queries; skeleton first, bodies on demand; per-archetype budgets |
| Knowledge writes | Hand-edited prose docs; updates skipped or duplicated → drift | Single gated write path; append-only; drift detectable, not silent |
| Review independence | Convention ("fresh eyes") with no enforcement | Robot-enforced DENY: reviewers cannot traverse the reasoning they must independently re-derive |
| Record location | Mixed: Notion + repo docs, both editable | Git markdown = truth; Notion = ticketing only; human views are projections |
| Cost profile | Tokens spent re-reading static knowledge every run | Zero-token robot serves the static part; LLM spends tokens on judgment only |

---

## What v1.5 hands to v2.0

- **The interaction trace** (intent/verdict per query round) → the v2.0 observability layer's data source.
- **Provenance on every node** (who, when, which ticket) → the reasoning-trace / decision-provenance requirement (v2.0 gap G1).
- **Hierarchical memory** (v2.0 item 2.1) → partially absorbed: the warehouse *is* the cross-ticket knowledge layer above LESSONS.
- **"Notion = view, not source of truth"** (v2.0 glue principle) → already realized in v1.5.
- **The deterministic robot** → the layer a thin orchestrator can route around without burning judgment tokens.

When v2.0 planning starts, its item list needs one revision pass against what v1.5 already delivers.

---

## Out of scope

- Any pipeline automation — DAG, conditional branching, checkpoint-resume stay in v2.0.
- Embedding / semantic search — deferred behind a measured trigger; keyword finder ships first.
- Pruning the old flat docs — only at the explicit cutover call, after the warehouse earns trust.
- Strategic lane (CONSULT role, independence-vs-continuity, portability/resell, Curator revision) — parked.

---

## References

- Knowledge Architecture & Token Optimization — Direction Checkpoint PoC + Sessions 2–8 (`docs/specifications/requirements/Knowledge_Architecture_and_Token Optimization_Direction_Checkpoint_PoC/`)
- Pre-Build Decision List (Planning Session Input) — the open decision backlog feeding the build planning
- Execution Schedule — Warehouse Build & SPQR Cutover — phases, exit checks, interim documentation regime
- SPQR v2.0 — Semi-Automated Pipeline — the unchanged next era this version feeds
