---

---
# SPQR — Structured Pipeline for AI-Assisted iOS Development

Governed, sequential multi-agent development pipeline for Foodoire. Solo developer. Team-level engineering rigor.

## What it delivers today

**Planning**

- Senate debates every ticket as 3 independent roles before implementation starts
- Agents form their own approach before reading the plan — anchoring bias eliminated
- Structured handoff with acceptance criteria before a single line of code is written

**Execution**

- Praetor implements in worktree isolation
- Tribunus reviews with fresh eyes — no inherited Senate judgment on code quality
- Probator verifies against acceptance criteria
- Curator checks operational readiness
- Each agent has veto authority in its domain — only the broken delta returns, no scope creep

**Memory**

- Every decision in Notion ticket comments — external source of truth
- [LESSONS.md](http://lessons.md/) accumulates per-ticket learnings, Senate reads on startup
- Architecture Decision Records track every significant architectural choice

**Spikes**

- Quaestor runs structured research on unknowns before production code is written
- Decision record handed off — no guesswork mid-implementation

## Where it's going — 6 Development Directions

The pipeline evolves along six independent but connected directions. Each has a holy grail — the end state that defines done for that direction. Versions are milestones along the way, not the goal itself.

| Direction | The question | Holy grail |
| --- | --- | --- |
| Orchestration | Who runs the pipeline? | Master agent coordinates; Mark sees exceptions only |
| Observability | Can we see what's happening and why? | Pipeline self-improves; patterns predict failures before they occur |
| Communication | How do agents hand off information? | Typed, filtered payloads between agents; Notion is visualization only — not source of truth |
| Specification | How precise and verifiable is the spec? | Machine-checked acceptance criteria; automatic pass/fail between Senate and Praetor |
| Memory & Learning | Does the system learn across tickets? | Cross-ticket intelligence; recurring failure points surfaced proactively |
| Resilience | What happens when something breaks? | Self-healing pipeline; no manual recovery needed |

## The end state

Mark focuses on product decisions. The pipeline handles the rest — every ticket, autonomously.

---

[[DONE SPQR v1.1 — Roadmap Decisions]]

[[SPQR v2.0 - Semi-Automated Pipeline]]

[[SPQR v3.0 - Autonomous Pipeline (A2A Vision)]]