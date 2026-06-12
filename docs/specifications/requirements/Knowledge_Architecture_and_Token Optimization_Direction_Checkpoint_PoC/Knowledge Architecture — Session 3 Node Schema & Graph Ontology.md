---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — node schema, edge ontology, identity & provenance

**Document status:** Complete — folded back

**Phase:** PoC — Session 3 (foundation; consumed by every downstream session)

**Date:** 2026-06-10

**Usage:** claude-opus-4-8:  7.9k input, 71.1k output, 2.1m cache read, 118.3k cache write ($3.59)

**Session scope:** The shape of a node and an edge — nothing about storage technology or retrieval runtime

**Purpose:** Close the node-schema foundation (S1-D, K10) so Sessions 4–8 build on a fixed ontology

**Status legend:** decided · leaning · mixed · open

---

# Overview

Session 3 closed the highest-leverage foundation: what a node and an edge are. The keystone resolved to a **single universal node with a discriminating **`**kind**`** field** (Option B) — not separate node types. Three kinds (decision / constraint / lesson) share a common spine and differ only in their body fields and which edges they use, so the "typed-nodes-in-a-trench-coat" risk stays closed. Specs are ruled **out** of the warehouse as source-of-intent. ID and provenance schemas are fixed. Everything here is now a **fixed input** for Sessions 4–8.

# Findings

- **The keystone was pre-decided by K10.** "A single universal node type whose type-metadata drives validation" already implies Option B; Session 3 only made it explicit. The universal node wins because the kinds share a 5-element spine (id, kind, status, provenance, edges) and differ only in body — they never rewrite the spine.
- **"Everything is a decision" is softened to "everything is a node; decision is the dominant kind."** Inherited knowledge (Swift naming, Apple HIG) becomes `kind: constraint`, not a decision it never was. Provenance carries the distinction via `origin`.
- **The warehouse is the system-of-record, not the source-of-intent.** Committed/applied knowledge lives in; aspirational specs stay out. A spec is *input* to a decision, never warehouse content — so the warehouse never has to ingest after every spec edit. The "why" still enters, but as a decision's rationale plus an external `motivated-by` pin.
- `**CONVENTIONS.md**`** is not a kind.** It splits along the provenance axis into `decision` (we chose it) and `constraint` (inherited from the platform).
- **Drift forensics needs more than a live link.** A bare link to a mutable external spec erases the very drift it should expose; it needs a version-pin (`spec-ID@version`) plus a frozen input snapshot in the decision rationale.
- **Append-only is structural, not cosmetic.** "Superseded" is **derived from an incoming **`**supersedes**`** edge, never a written field**; a node is never mutated after birth. New nodes attach; meaning lives in the incoming edge. This is what kills drift by construction.

# Breakdown — the four clusters

## Cluster 1 — Ontology keystone

- **Option B:** one universal node + `kind` field. Shared spine (id, kind, status, provenance, edges) + kind-specific body.
- **Three kinds:** decision · constraint · lesson.
- **Spec excluded:** stays outside as source-of-intent; linked via external `motivated-by` ref, never ingested.
- **Layering:** one logical source-of-truth store; the `kind` discriminates; physical views are derived robot projections, not separate stores (a later DB index would be a derived projection — Session 7).

## Cluster 2 — Field schema per kind

- **Field-vs-prose boundary set by the consumer:** robot filters/traverses on it → frontmatter; LLM interprets it → prose body. ADR sections (Context/Decision/Rationale/Consequences) stay prose; only filterable metadata is frontmatter.
- **Shared spine (frontmatter):** id · kind · status · provenance · title · edges · body.
- **Per kind (conditionally required, K10):** decision → `scope` required, supersedes/motivated-by optional; constraint → `source` required, no supersedes, no agent; lesson → `agent` + `ticket` required, `about` edge strongly recommended.
- **Status:** base enum `active` / `retired` for all + per-kind extension; `superseded` is derived, not stored.
- **Hard vs soft rules:** hard schema (id, kind, origin missing) blocks at ingest; soft policy (kind-foreign status, missing recommended edge) does not block — it **flags**, append-only. Flag *lifecycle* is Session 6; Session 3 only lays the hard/soft hook.
- **Atomicity criterion:** a node = one independently supersedable/referenceable assertion. The *splitting procedure* (ingest chunking) is Session 8.

## Cluster 3 — Edge ontology

- **Typed set:** `supersedes` (decision→decision) · `derived-from` (decision→decision/constraint) · `constrains` (constraint→decision) · `about` (lesson→decision) · `relates-to` (any→any, second-class fallback).
- `**motivated-by**`** is an external reference, not an internal edge** — points at a versioned spec outside the graph; internal traversal never steps on it.
- **Trench-coat closed:** no kind owns a private edge type; kinds use subsets of the shared ontology.
- `**relates-to**`** overuse** is a small risk (the Jira relate-vs-child-of pattern); no metric now, a later audit (S6) may look.
- **Edges are directed; no inverse edges** — the robot reads a directed edge both ways.
- **Append-only invariant:** an existing node is never mutated when a new edge arrives; the meaning lives in the incoming edge.

## Cluster 4 — Identity & provenance

- **ID:** opaque, stable, assigned by the ingest-robot at commit (single serializing gate → no collision even with sequential numbers). Form `food-n23` = project-prefix + node-marker `n` + sequential number. **No kind encoded in the ID** (would drift against the kind field); `n` marks the universal node type, not the kind. Human readability comes from `title`, not the ID.
- **Provenance (PROV-O inspired, origin-conditional):** `origin` (decided/inherited/observed, always) · `timestamp` (ingest time, always) · `ticket` (decided/observed — the external work-item handle; **supersedes the earlier separate **`**run**`** field**, per the S5 fold-back 2026-06-10) · `agent` (decided/observed) · `source` (inherited). Append-only; never rewritten. **Traceability:** `ticket` + `agent` reconstruct the SPQR session (tab-name = `TICKET-XXX — Agent`); the full ticket→session-id map lives externally (Obsidian), not in the warehouse — only the join key is stored. Single ingest timestamp, no separate event-time field.

# Recommendations

- **Fixed inputs for Sessions 4–8:** universal node + 3 kinds; the edge ontology; the ID and provenance schemas; the append-only "superseded = derived" invariant. Do not re-litigate.
- **Lane boundaries handed off:** flag lifecycle → Session 6; atomic-splitting / chunking procedure → Session 8; storage substrate & markdown-vs-DB → Session 7; query protocol → Session 4.
- **Next:** Session 4 (query contract) and Session 5 (restructuring) may both run now — each depends only on Session 3.

# Descoped

- Flag lifecycle and audit policy — Session 6.
- Ingest chunking / atomic-splitting procedure — Session 8.
- Storage substrate, DB index, retrieval runtime — Session 7.
- Query protocol (trigger, result count, INDEX-first) — Session 4.

# References

- Session 1 checkpoint: Knowledge Architecture & Token Optimization — Direction Checkpoint PoC (parent)
- Session 2: Node Structure, Query Interface & Knowledge Base Restructuring (sibling)
- Session Roadmap: Open-Question Map & Critical Decisions (sibling)
- Foodoire decisions directory: Docs/decisions/a01–a22 (the warehouse prototype; ID scheme migrates a→n)
- W3C PROV-O — entity / agent / activity, borrowed for the provenance field set
- SPQR AGENT_LAWS — Law 3 (external record is truth) underpins the fold-back-per-session rule