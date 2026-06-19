---
type: poc
title: "Future Observe Layer & Orchestration Horizon — Research Note"
decides: "Nothing now — captures the SAW-24 2.0/3.0 horizon (telemetry SOTA + future Observe + orchestration layer) as a reference for future upgrades."
status: draft
date: 2026-06-19
tags: [poc, research, horizon]
---

# Future Observe Layer & Orchestration Horizon — Research Note

> **Provenance:** surfaced 2026-06-19 as an owner research detour during the **SAW-27** (telemetry sensor) Phase-1 context-loading discussion. This is exploratory, NOT SAW-27 scope. SAW-27 is the thin now-wedge; this note is the horizon it sits under (the [[SAW-24]] epic: Observability / detection-health → 2.0 registry/online-eval, 3.0 self-building governance).

## Context / question
If we assume the 2026 state-of-the-art, what does a "full" telemetry/Observe layer look like for SPQR, and how would it work once a standing **orchestrator agent** exists that maintains the team? Reference only — so future upgrades don't re-derive it.

## Findings

### 1. The 2026 SOTA shape — three layers + a flywheel (OODA operationalized)
- **Trace** — capture every step deterministically. Standard = OpenTelemetry GenAI semantic conventions (`invoke_agent` → `chat` → `execute_tool`; attrs `gen_ai.agent.name`, `gen_ai.usage.input/output_tokens`, `gen_ai.response.finish_reasons`, `error.type`).
- **Score** — online eval on a sample; alert on *quality* drift (not infra). Trajectory metrics (step efficiency, tool/argument correctness, plan adherence) + LLM-as-judge (CoT / G-Eval).
- **Feedback (flywheel)** — failed traces → eval cases → same scorers gate CI. Day-1 trace → Month-1 online scoring → Quarter-1 regression-gating.
- Maps to OODA: **Observe** = Trace · **Orient** = the left-shift lens · **Decide** = the measurement gate that licenses further additions (anti over-engineering) · **Act** = regression registry → self-building governance.

### 2. The layer map (this resolved the owner's main confusion)
Different problems live on **different layers** — do not collapse them into "a memory the LLM reads":

| Layer | Answers | Where the LLM sits | Context-window bound? |
|---|---|---|---|
| **Execution / durability** (e.g. Temporal) | "keep running after a crash, exactly-once" | a *called worker* (code invokes it) | no — the engine replays code, not prompts |
| **Knowledge** (Graph RAG / warehouse) | "what conventions / decisions exist" | *this* is what the LLM reads, selectively | **yes — lives here** |
| **Interop** (A2A protocol) | "how agents message each other" | — | — |
| **Quality / governance** (gates, Laws, eval, telemetry/left-shift) | "is the work good" | — | — |
| **Audit / record** (append-only handover, hub) | "what happened, re-readable" | the LLM re-reads it | yes (when loaded) |

- SPQR's current cross-session mechanism = **re-read** (next session reads the doc vault; Law 3), which is the **knowledge/audit** layers — and is exactly what the context window bounds. **Graph RAG** is the answer to that pressure (pull only relevant knowledge), NOT durable-execution.
- **Temporal** = the execution/durability layer: an engine workflows *run on*, with an event-history the **engine** replays to resume — not a knowledge store, never poured into the LLM context. **Overkill for SPQR's HITL cadence**; relevant only if the orchestrator ran many *unattended* jobs with *irreversible* side-effects.
- **re-read = re-reason** (lossy, fine when human-gated + cheap to redo). **Temporal replay = reuse recorded results** (exact, exactly-once; the LLM is quarantined as an Activity and never re-run).

### 3. The orchestrator — a standing role (the SAW-24 3.0 horizon)
A non-per-ticket agent: the autonomous successor to today's owner-driven Upgrade-Master + Retro loop.
- **Reads:** telemetry trend (doc vault) + conventions (Graph RAG).
- **Does:** health-monitor → diagnose/localize a leaking agent/skill (TRAIL-style) → draft a fix (skill/checklist change or eval case) → **route it through the existing pipeline** → measure if the leak closed → promote recurring Censura findings into permanent agent checklists (one-off catch → permanent left-shift).

**Governance — the critical axis (Spock):** SPQR's safety model rests on separation (Upgrade-Master never edits product files directly; CLAUDE.md owner-applied; owner-only commit). An orchestrator that "maintains the team" is exactly that primitive. Two models:
- **(1) Proposer-only** — automates Observe/Orient/Decide-proposal; team-affecting Act stays human-gated. Current model intact.
- **(2) Closed-loop through its own gates** — applies changes, but every self-edit goes through the same pipeline it governs (SAW ticket → Censura → receipt → measured by telemetry). Self-modification allowed only *through* the gates, never via a privileged side-channel.

**Recommendation: (2)** — the orchestrator's power must be *initiate & route*, not *bypass*; it should be the most Law-bound agent, and earn autonomy by track record (trend-gated, reversible self-edits, HITL until proven).

### 4. Honest caveats
- **Low volume:** 2026 guidance = ≥500 cases before trusting aggregate metrics; SPQR runs few tickets → telemetry must be **trend + narrative**, not threshold dashboards (for a long time). This *validates* the now-wedge logic (accrue history) and *warns* against over-reading early numbers.
- **Goodhart:** optimizing "left-shift" is gameable (catch trivially early / under-report) → need a **balance metric** (escape-to-owner / post-close defects).
- **Who watches the watcher:** the orchestrator's own trajectory must be recorded + a human circuit-breaker.
- **Don't import the SaaS stack:** mirror the OTel *schema* (field names, span/trajectory model) in the doc-native record — don't bolt on an OTel SDK.

## Recommendation / decision
No action now. Keep as the horizon reference for the [[SAW-24]] 2.0/3.0 arc. When the orchestrator becomes a real ticket, start from §3 (governance model 2) and §4 (caveats). SAW-27 delivers only the thin sensor that begins accruing the data this horizon will later consume.
