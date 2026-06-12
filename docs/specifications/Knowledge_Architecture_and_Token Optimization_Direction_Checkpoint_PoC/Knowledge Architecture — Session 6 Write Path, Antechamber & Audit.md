---

---
## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Knowledge warehouse — write path, antechamber governance, audit layer & promotion gate

**Document status:** Complete — parent fold-back applied

**Phase:** PoC — Session 6 (depends on the fixed S3 ontology; closes S1-B, S1-F, S1-G)

**Date:** 2026-06-10

**Usage:** claude-opus-4-8:  12.0k input, 61.9k output, 2.0m cache read, 115.5k cache write ($3.35)

**Session scope:** The write path (proposal → ingest), antechamber governance, the audit layer, and the promotion gate. Nothing about storage substrate (S7), migration/chunking (S8), or SPQR-side implementation.

**Purpose:** Close write-path & audit governance (S1-B, S1-F, S1-G) on the fixed Session 3 ontology.

**Status legend:** decided · leaning · mixed · open

---

# Overview

Session 6 governs how knowledge **enters** the warehouse and how it is **watched** once in. It fixes a two-stage write path (deterministic robot gate → Senate semantic judgment), an archetype-conditional antechamber, a two-tier audit layer that only ever flags, and a per-risk-tier promotion gate that lets proven proposal-classes skip the Senate over time. The central reframe: the write path, the audit layer, and the promotion gate are one system — the gate is the dial that moves the determinism line rightward as the audit layer proves a class safe. Everything reuses the S3 append-only + derived-status machinery; no new mechanism is introduced.

# Findings

- **Evaluation is two-stage, not monolithic.** The "Senate evaluates and ingests" direction is refined: a deterministic ingest-robot runs the cheap hard-schema gate and the S4 pre-ingest query check; the Senate (Opus) is woken only for semantic judgment, on a pre-assembled packet. Malformed proposals never cost an Opus call.
- **The robot is the write-path front door, event-triggered — not Senate-initiated.** The Senate *consumes* the robot's connection report; it does not *initiate* the routine pre-check. Exception: during judgment the Senate may initiate a deeper S4 deep-dig (robot-executed).
- **The promotion gate is the system's through-line.** It governs not just check-promotion but **which proposal classes skip the Senate entirely** (auto-ingest). "Determinism line moves right" = fewer escalations; long-run the robot runs itself and the Senate is the exception path. Promotion is reversible (a post-promotion flag demotes — not a ratchet).
- **A flag is an audit-node on a separate plane, self-similar to the knowledge graph.** It is not a 4th knowledge kind (S3's three kinds stay untouched; S3 explicitly deferred flag-lifecycle to S6). The flag points at its target via a `flags` edge and never mutates the target; its open/resolved status is *derived* from an incoming `resolves` edge — the exact mirror of S3's "superseded is derived."
- **Concurrency dissolves under append-only.** The serialized ID gate (S3) removes ID collisions; contradictory parallel proposals both ingest (no lost write) and surface as an audit flag, not a merge conflict. No locks.
- **Dup/orphan defense is three-layered:** agent reads before proposing (agent-discipline rule) → robot pre-check connection report → auditor orphan/contradiction watch.
- **"Run ID / Session ID binding" is obsolete.** S3/S5 dropped the `run` field; binding is `ticket` + `agent`, and the session-id map lives outside the warehouse (Obsidian). S6 only governs how the in-flight proposal binds to `ticket`+`agent` before the node-ID exists.

# Breakdown — the three clusters

## Cluster A — Write path & antechamber

- **Two-stage evaluation:** robot hard-gate (id/kind/origin well-formed) + S4 skeleton pre-check → escalate to Senate only for semantic judgment. The robot does the actual append (food-nNN at the serializing gate + edges).
- **Proposal lifecycle state machine:** `proposed` → [robot hard-gate] → `rejected-malformed` OR `validated` → [robot pre-check + escalation decision] → `auto-ingested` (promoted class — present now, initially empty, activated by Cluster C) OR `pending-senate` → [Senate verdict] → `ingested` / `rejected` / `revise`.
- **revise:** no separate state — wakes the proposing agent via the `ticket`+`agent` binding, re-enters at `proposed`. Bounded loop (N rounds → owner/CONSULT escalation).
- **Antechamber visibility is archetype-conditional** (the write-side mirror of the S4 read policy): SCRUTINIZE shielded (DENY/independence), EXECUTE sibling-read (anti-duplication), SYNTHESIZE delta/aggregate view. Agents must *read* the antechamber before proposing — a governed discipline, not just a data structure.
- **Concurrency:** append-only + serialized ID gate + audit-flag for semantic conflict; no locks.
- **Scope-discipline cost (S1-B):** accepted trade — monotonic growth, retired nodes hidden by the S4 active-filter, node/scope count = the S5 bleed monitor.

## Cluster B — Audit layer

- **Two-tier auditor, neither mutates (flag-only):** continuous deterministic robot tripwires (orphan-watch, missing-recommended-edge, `relates-to` overuse) + a periodic **semantic** audit (contradiction detection). The semantic audit is **owner-driven for now**.
- **Severity (S1-F): hybrid.** Emergent `frequency × damage` (one metric feeding model-tiering and the promotion gate) with a small **fixed floor** for categorically-critical cases (e.g. contradiction on a foundational node).
- **Flag lifecycle:** flag = append-only audit-node on a **separate audit-plane**, reusing the universal-node machinery (one ingest-robot, plane discriminator e.g. ID `f` vs `n`). Status derived (no `resolves` edge = open, has one = resolved). Multiple flags per node = multiple independent flag-nodes; node "heat" = aggregate of open flags. Resolution is a write-path action or a retro-sweep; no hot-path human clearing.

## Cluster C — Promotion gate

- **Promotes two things through one gate:** deterministic *checks* (LLM → robot, the determinism line) and proposal *classes* (skip Senate → auto-ingest).
- **Per-risk-tier, not global, not literal per-check (S1-G):** thresholds set by risk class (e.g. `reversible-cheap` vs `silent-corruption-risk`), so the damage profile is respected without an unmanageable number of knobs.
- **Calibrated by the Cluster B audit metric;** reversible — a post-promotion flag demotes. **Owner-driven trigger for now;** mechanism now, automation (SYNTHESIZE/Senate) later.
- **Initial state:** everything un-promoted; the auto-ingest class starts empty; promotion is earned per-class via a clean audit history.

# Recommendations

- **Closes S1-B, S1-F, S1-G.** Folded into the parent direction table: row **B** (mutation-cost resolved — accepted trade), row **F** (severity → hybrid emergent + fixed floor), row **G** (promotion gate → per-risk-tier).
- **Small S4 fold-back:** add a "knowledge-plane only" default to the S4 active-filter, so knowledge queries don't see the audit plane.
- **Owner-driven for now, by design:** the semantic audit and the promotion trigger are judgment acts the owner performs; the session fixes the *mechanism*, automation is deferred.
- **SPQR not-now tasks (carry into the SPQR update):** the auto-ingest proposal class; the periodic semantic-audit "review this" schedule entry.

# Descoped

- Storage substrate and the physical realization of the audit plane / serializing gate — Session 7.
- Ingest chunking / atomic-splitting — Session 8.
- Model-tiering measurement tuning and the semantic-audit cadence parameter — parked measurement lane.
- SPQR-side implementation of the write path and the schedule task — separate SPQR update.

# References

- Session 3: Node Schema & Graph Ontology (fixed ontology; laid the hard/soft flag hook, deferred lifecycle here)
- Session 4: Query Interface Contract (pre-ingest query check; archetype policy; active-filter the plane-default extends)
- Session 5: Knowledge Base Restructuring (ungoverned lesson-mixing this write path fixes; run→ticket fold-back)
- Session Roadmap: Open-Question Map & Critical Decisions (S1-B/F/G origin; fold-back-per-session rule)
- SPQR AGENT_LAWS — Law 3 (external record is truth)