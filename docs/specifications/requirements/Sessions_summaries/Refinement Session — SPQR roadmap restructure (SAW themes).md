---

---
## Metadata

**Type:** Refinement session (not a retro)

**Date:** 2026-06-05

**Session ID:** eba0971b-dbe4-44ab-9b66-96aaea8997c3

Total usage cost: 8.5k input, 241.4k output, 10.4m cache read, 977.9k cache write ($17.39)

**Scope:** SPQR agentic workflow — grooming/refining the open SAW tickets into a roadmap; NOT Foodoire code.

**Inputs:** Retro #2 cluster directions (problem-clusters C1–C6) + the 16 open SAW tickets.

**Roundtable:** Gyuri (dev-process architect) + Laci (2026 agentic trends), web-validated.

**Outcome:** SAW DB restructured into 10 theme containers + 4 now-wedge children, executed in Notion.

---

## Goal

Order the open SAW tickets into a consistent theme structure with clear horizons (now / after first dev+bug / 2.0 / 3.0), and decide what enters scope now. The retro states PROBLEMS; this session designs and commits.

---

## Method decisions (the durable "how")

- **Carve-from-clean-theme:** big themes are structured containers; small/now tickets are carved out and parented for traceability. Cross-cutting wedges get one primary parent + a contributes-to link.
- **Decide ≠ Execute:** high-confidence target architectures are decided now; the big cross-cutting execution is batched into 2.0's large-context window (token-efficient bulk). Never build throwaway overhead.
- **Wedge-placement rule:** build a wedge where the process is untested (learn) or damage accrues now and is cheaply stoppable; solve a 2.0 element now if its solution is already correct and applicable.
- **Hybrid migration:** new tickets only where the structure genuinely changes; reshape-in-place for clean containers; close superseded tickets with a pointer (not delete), only on verified placement.
- **Output discipline:** all Notion tickets in English; container tickets use an extended format (a second "container"-type template is parked for the output phase).

---

## Key analytical decisions (the durable "what")

- The retro recognized PROBLEMS, not solutions — C1–C6 distilled to problem + root cause on a 5-axis frame.
- **C4 (Verification) and C5 (Observability) were homeless** — created as new big-theme containers; they are the two highest-leverage clusters.
- **Thicken-now (3 real wedges):** receipt rule (C4+C6), telemetry sensor (C5, absorbs SAW-9), live-decision manifest + supersession + back-write (C1+C2 glue).
- **C5 elevated to NOW** as the measurement gate that licenses any further structural/agent additions (anti over-engineering).
- **10th container created — Operations / process-debt** — operational items (ticket-procedure, bug-pipeline, usage labor, model-routing) that don't fit the cognitive themes.
- **Decouple decide from execute** surfaced and adopted as the resolution of "don't build throwaway" vs "don't wait artificially."

---

## 2026 validation (web)

- 5/6 clusters map 1:1 to 2026 best practice; governance articulation slightly ahead of the average.
- **Caution adopted:** multi-agent over-engineering (15× token overhead; "start single-agent, add only for the measured failure mode") → measurement-first (C5).
- **Governance ≠ orchestration** layer separation validated → Picard/constitution to Governance, routing to Orchestration; orchestration enforces policy it does not author.
- **Same-model committee representational collapse** (chain-of-thought cosine ~0.888; "Consensus is Not Verification") validates SAW-20's false-consensus finding; true multi-core independence flagged as an OPEN 2026 frontier (ensembling does not restore it).

---

## Structure outcome — 10 theme containers

1. Communication / glue (reshaped SAW-10)
2. Source-of-truth & decision integrity (new)
3. Knowledge representation (reshaped SAW-13)
4. Verification & evidence / Specification (new)
5. Observability / detection-health (new)
6. Hygiene / rule-rot (reshaped SAW-11)
7. Gate-primitive (reshaped SAW-14, + salience/trigger from SAW-12)
8. Orchestration 3.0 (reshaped SAW-12, slimmed)
9. Governance / constitution — north star (reshaped SAW-15, + ownership rule + frontier flag)
10. Operations / process-debt (new)

**Now-wedge children (Up Next):** Receipt rule → 4 · Telemetry sensor → 5 · Live-decision manifest → 2 · Lean bug-pipeline → 10.

---

## What changed in Notion

- **Created:** 4 new containers + 4 now-wedge children.
- **Reshaped:** SAW-10 split (→ Communication; machine-readable-docs → Knowledge; ADR-WHY → Decision-integrity); SAW-11/12/14/15 reshaped (EN). SAW-12 slimmed, its principles redistributed by reference (Picard + multi-core-independence → Governance; salience/trigger → Gate-primitive; intake → Operations).
- **Re-parented:** SAW-1 → Decision-integrity · SAW-16 → Hygiene · SAW-17 → Verification · SAW-20 → Governance (near-now, before any persona-split).
- **Closed with supersession-pointer (Stage = Done, content preserved):** SAW-2, SAW-8, SAW-9, SAW-19, SAW-21.
- **Untouched:** SAW-18 (Done).

---

## Horizon map

- **Now:** Receipt · Telemetry sensor · Live-decision manifest (+ SAW-1/16/17 near-exec, SAW-20 pre-split).
- **After first dev + bug tickets:** Hygiene audit · typed-handoff rollout · telemetry thickening · bug-pipeline + SAW-8 fix (gated before the bug batch).
- **2.0 (Observation unfolded, not full-auto):** deep Observability · machine-checked acceptance criteria · decision-store migration · knowledge representation · gate-telemetry.
- **3.0 (autonomy):** Orchestration (A2A) · Governance L3–L4.

---

## Remaining (future sessions — NOT this one)

- Execute the now-wedge tickets (write the rules into skill files).
- Record the decide-now decisions (C1 target architecture: decision-store + docs-as-projection; C2 typed-handoff schema lock).
- SAW-8 Urgent fix before the next FDP/bug ticket batch.
- Output-phase: create the second "container"-type SAW template.

---

*2026 validation sources: "Consensus is Not Verification" (arXiv 2603.06612); "Representational Collapse in Multi-Agent LLM Committees" (arXiv 2604.03809); AI agent governance two-layer framework (*[*atlan.com*](http://atlan.com/)*); agent observability & over-engineering anti-patterns (*[*digitalapplied.com*](http://digitalapplied.com/)*, Wasowski 2026).*