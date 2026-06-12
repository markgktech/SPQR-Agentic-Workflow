---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — query protocol between the LLM and the deterministic robot

**Document status:** Complete — folded back

**Phase:** PoC — Session 4 (depends only on Session 3; runnable in parallel with Session 5)

**Date:** 2026-06-10

**Usage: **claude-opus-4-8:  14.3k input, 54.1k output, 2.0m cache read, 96.6k cache write ($3.04)

**Session scope:** The query contract — how an agent asks the robot, what it gets back, how rounds advance, and how much it may spend. Nothing about the retrieval engine (BM25/dense/hybrid) or storage substrate — those are Session 7.

**Purpose:** Close K6–K9 and the query-protocol open items so the write path (S6), substrate (S7), and migration (S8) build on a fixed contract.

**Status legend:** decided · leaning · mixed · open

---

# Overview

Session 4 fixes the contract by which a judgment agent queries the deterministic warehouse robot. The keystone reframe: with a typed graph now fixed (Session 3), retrieval is **not** an "expanding search window" — it is **entry-point selection followed by deterministic edge traversal**. The contract is therefore two-phase: a cheap disambiguation phase that returns a skeleton candidate list (no bodies), then an actual-retrieval phase that pulls bodies and edges only for explicitly selected nodes. A per-round verdict vocabulary is the control surface; intent-before / verdict-after brackets every round and doubles as the interaction trace. Budget and access permissions collapse into a single per-archetype query policy. Everything here is a **fixed input** for Sessions 6–8.

# Findings

- **The Session 2 "expanding-window" framing predates the fixed graph and must be re-read.** With Session 3's typed edges, "broadening" is graph-neighborhood expansion along edges, not re-searching with a wider net. The contract is traversal-centric, not search-centric.
- **Reducing disambiguity is a distinct, cheap first phase — not a failed first retrieval.** Round one returns only a skeleton candidate list (id + title + kind + scope, no body); the agent selects by ID. This converts a fuzzy paraphrase into a deterministic pick and sidesteps the paraphrase-drift problem structurally.
- **A full manifest does not scale and would reintroduce the monolith load the project exists to kill.** A ~10k-node table of contents is itself too large to load. The manifest must be scope-bounded — open a *section*, never the whole catalog.
- **"More results" is not one state but several distinct verdicts with different outcomes.** Wrong entry, right-area-but-not-yet-reached, genuinely absent, and present-but-unlinked each route differently. The most important is that the agent can cheaply and legitimately conclude ABSENT rather than loop forever.
- **N-bounded (top-k ranking) reintroduces the paraphrase-miss risk** wherever determinism is available: if the target ranks below the cutoff, the agent never sees it. Bound by structure (scope slice, edge set), not by ranking — rank-bound only the inherently fuzzy finder.
- **There is only one true DENY, and it is independence-driven.** Only the SCRUTINIZE tier must be blind to the reasoning it is meant to re-derive. Every other archetype's "restriction" is economy-driven scope-shaping already handled by budget and scope filters — do not over-build a DENY matrix.
- **The intent/verdict bracket is the interaction log for free.** No separate logging subsystem is needed; the contract emits a structured per-round trace by construction. WRONG-ENTRY + ABSENT verdicts with their intent text are exactly the "incorrect searches" a retro wants to review.

# Breakdown — the query contract

## Cluster 1 — Contract skeleton (closes K8)

- **Two phases:** (1) disambiguation — cheap skeleton candidate list (id + title + kind + scope, no body); (2) retrieval — body + edges only for the IDs the agent selects.
- **K8 resolved:** scope-bounded manifest, *not* a full-index load and *not* finder-only navigation. "Scoped TOC first."
- **Two feeds, one response shape:** a deterministic `kind`+`scope` filter (preferred, zero fuzzy) and the finder (K1, dense/BM25 entry, fallback when the scope is unknown). Both return the same candidate shape, so selection is uniform by ID. The finder stays a side-door, never primary retrieval (preserves C / K1).

## Cluster 2 — Round trigger & verdict vocabulary (closes K6)

- **Trigger split:** the robot triggers only the trivial **zero-result auto-broaden** (no judgment); everything else is an LLM verdict.
- **Per-round verdict (the control surface):** `FOUND-ENOUGH` (terminate, use) · `WRONG-ENTRY` (reformulate intent, re-enter — bounded retry) · `INSUFFICIENT-TRAVERSE` (follow an edge deeper — bounded depth) · `ABSENT` (terminate "not in warehouse" — a legitimate cheap terminal, not a failure) · `FOUND-UNLINKED` (terminate + emit missing-edge signal).
- **Hooks to Session 6:** `ABSENT` may emit a gap-candidate signal (antechamber); `FOUND-UNLINKED` emits a missing-edge audit signal. Session 4 lays only the emission hook; downstream handling is Session 6.

## Cluster 3 — Results per round (closes K7)

- **Scope-filter feed → scope-bounded:** the agent sees the *complete* slice (no ranking cutoff that could bury the target). Overflow is handled by **faceting** (return sub-scope breakdown + counts, force a narrower scope), never by truncation.
- **Finder feed → N-bounded (top-N):** the finder is inherently ranked and only needs to get a foot in the door; completeness is not promised.
- **Traversal round → scope-bounded to the node's edge set:** body for explicitly fetched nodes; all direct edges as TOC rows (the graph already did the filtering — a node has few edges by construction).
- **Unifying principle:** scope-bound where structure gives a natural boundary; rank-bound only where ranking is inherent.

## Cluster 4 — Query modes / resolution (closes the deep-dig vs high-altitude item)

- **One contract, two resolutions:** high-altitude = **skeleton** (TOC + edge skeleton, no bodies — breadth, navigation/mapping); deep-dig = **body-fetch + edge traversal** (depth, reading).
- **The agent picks resolution per need;** the verdict vocabulary drives it (`INSUFFICIENT-TRAVERSE` = go deeper, `WRONG-ENTRY` = go to another section).
- **Guardrail:** high-altitude has a maximum breadth ceiling — you open a scoped *section*, never the whole warehouse graph at once.

## Cluster 5 — Intent declaration & trace (confirms K9)

- **K9 confirmed:** every round is bracketed — **intent before** (what + which feed + which resolution) and **verdict after**.
- **The bracket is the trace record:** intent → returned-set summary → verdict. The contract emits this per round by construction.
- **Consumption is downstream:** retro review ("how does it perform vs plan", incorrect searches), golden-set measurement (S7, Ragas/TruLens), audit (S6). Session 4 owns only the emission.

## Cluster 6 — Per-archetype query policy (merges budget + DENY)

- **Budget = the "how much" dial:** altitude ceiling (max breadth of one scope-open) · round count (parameterizable; separate caps for WRONG-ENTRY retry vs INSUFFICIENT-TRAVERSE depth) · body-fetch ceiling (the expensive axis) · terminal backstop (on exhaustion, force a terminal verdict).
- **Failure handling:** budget exhaustion is an **owner escalation (halt)**, never a silent fail. The escalation packet = the trace + the terminal verdict + what was gathered, so the owner can judge whether something was lost. A fresh budget requires an **owner-issued continuation grant**; the robot enforces this as a deterministic **consent-gate** (no grant → no fresh round). Not a cooldown (delay ≠ consent), and the robot's capability is not capped — only gated. The general owner-halt mechanism is an existing SPQR pattern; the grant-issuance detail is S6/SPQR-level.
- **DENY = the "what not" dial, structural on edges + kinds (robot-enforceable; does not reopen Session 3's prose-body boundary):**
    - **SCRUTINIZE (Tribunus, Probator, Curator) — the only true DENY:** ALLOW decision nodes (whole), constraints (the checklist), diff/mandate; DENY `derived-from` / `supersedes` lineage traversal (the reasoning chain) and `about`-linked lessons (journey memory). "Not too deep" = no lineage traversal, not section-hiding. Accepted tradeoff: the immediate decision node's rationale prose stays visible (a minor leak vs. reopening S3); may be tightened later if sycophancy proves high.
    - **DELIBERATE (Senate:Consilium):** broadest — all kinds, bodies, all edges, high-altitude; works at altitude, not at low-level constraint detail. (Scope-shaping, not DENY.)
    - **EXECUTE (Praetor, Quaestor):** scoped to the ticket blast radius — scope decisions, domain patterns, constraints, bodies in-scope. (Scope-shaping.)
    - **SYNTHESIZE (Senate:Censura, Retrospector):** deliberately sees the journey — lessons, full history, churn, all bodies. (No DENY.)
    - **CONSULT:** broad high-altitude skeleton, shallow body (light per call). (Scope-shaping.)
    - **ROBOT:** N/A — it is the server; it holds nothing.

# Recommendations

- **Fixed inputs for Sessions 6–8:** the two-phase contract; the verdict vocabulary; scope-bound-vs-rank-bound result rule; the two-resolution model; intent/verdict bracket as trace; the per-archetype query policy (budget dials + the single SCRUTINIZE DENY).
- **Lane handoffs:** ABSENT / FOUND-UNLINKED downstream handling → S6; trace consumption (retro + measurement) → S6 / S7; finder engine choice (BM25 / dense / hybrid / RRF) → S7; continuation-grant issuance mechanism → S6 / SPQR-level.
- **Build order unchanged:** S4 and S5 both depend only on S3; S6 consumes the hooks laid here.
- **Revisit trigger:** if retro shows a high WRONG-ENTRY rate or reviewer sycophancy, tighten the SCRUTINIZE DENY (possibly by making ADR sections individually addressable — a Session 3 extension, flagged as a deviation if taken).

# Descoped

- Retrieval engine (BM25 / dense / hybrid / RRF) and recursive traversal implementation — Session 7.
- Flag / signal lifecycle and the antechamber that consumes ABSENT / FOUND-UNLINKED — Session 6.
- Continuation-grant issuance mechanism (how the owner grants) — S6 / SPQR-level.
- Golden query set and Ragas / TruLens measurement — Session 7.
- Storage substrate and the markdown-vs-DB reconciliation — Session 7.

# References

- Session 1 checkpoint: Knowledge Architecture & Token Optimization — Direction Checkpoint PoC (parent)
- Session 2: Node Structure, Query Interface & Knowledge Base Restructuring (K6–K9 origin)
- Session 3: Node Schema & Graph Ontology (fixed input — universal node + 3 kinds, edge ontology, append-only)
- Session Roadmap: Open-Question Map & Critical Decisions (sibling)
- SPQR AGENT_LAWS — Law 3 (external record is truth) underpins the trace + fold-back rule; Law 4 (independent view) underpins the SCRUTINIZE DENY