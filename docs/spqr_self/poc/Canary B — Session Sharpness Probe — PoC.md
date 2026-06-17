## Metadata
**Ticket:** — (personal global tool; standalone PoC, ~no DOC/SAW footprint by owner choice)
**Epic:**
**Component:** SPQR / Canary (global tool)
**Document status:** BRIEF — not started (proposal to validate)
**Date:** 2026-06-15
**Session ID:** — (pending PoC execution)
**Usage:** — (pending PoC execution)
**Session scope:** A personal, owner-triggered, single-command tool — droppable into **any** chat — that gives an **objective** read on whether the live session's context is still intact, especially when the owner *feels* drift (and around compaction).
**Purpose:** Propose Canary B as a PoC brief — well-prepared proposals, **not** fixed decisions. The PoC session refines, decides, and validates.

---

# Overview
This PoC explores a **session-sharpness / capacity gauge**: a one-command tool the owner fires when they suspect a session is drifting, that returns an **objective** "intact / degraded" verdict instead of a gut feeling. It lives in the **global `~/.claude/`** (like the four laws) so it works in **any** chat, with the generic SPQR getting a copy. **In scope:** the grader architecture, the probe types, the decision rule, the trigger. **Out of scope:** the not-yet-canonized Fable / "bika"-agent → execution-agent run flow used to build it (owner-regulated; deliberately not opened here).

This is the personal, undocumented canary — the counterpart to **Canary A** (the pipeline deterministic validator). The two are **complementary layers that meet at the handoff.**

> **Engine note (don't forget):** B's engine is an **LLM grader (a fresh subagent), skill-based — NO standalone script required.** Unlike Canary A (whose engine is deterministic code), B is essentially a skill (md): it uses the agent's existing Bash/Read tools to locate + read this session's transcript jsonl (a couple of commands, not a program), and the grading is the subagent's LLM judgment. At most a tiny Bash glue snippet for locating the jsonl; do **not** start writing a real script/program for B.

# Motivation
On long sessions (even on a strong model) derailment often arrives **earlier than it feels**, and the owner cannot verify from inside whether the model is "actually dumb." The pain is sharpest around **compaction**: research shows context loss is severe (only ~40% of facts retrievable after compaction; recall drops to 0–7% in compacted zones; "artifact trail" is the weakest dimension). The deeper goal is **not** to survive compaction but to **never reach it** — to know *when to round off a topic or hand off* before rot sets in.

The worst case is not a degraded session — it is a **degraded session that authors the next session's context**, silently propagating the derailment as "truth." So the gauge's highest-leverage moment is **before trusting a session to write a handoff.** This makes Canary B the empirical instrument behind AGENT_LAWS **Law 3** ("the external record is truth; do not rely on session memory") — it measures *how much* session memory can still be trusted.

# Findings
- **A degraded session cannot grade itself.** If it has drifted, its self-assessment has drifted too. Objectivity **requires an external grader with ground truth.**
- **The ground truth survives compaction.** Claude Code stores the full, pre-compaction transcript on disk (session jsonl). Compaction truncates the *working window*, not the on-disk log — so a fresh grader can compare the live session's answers against what was *actually* said.
- **Quality rot precedes window-full.** The token bar measures *proximity* to the cliff; the canary measures *quality* — which (per context-rot research) degrades well before the window is full. Both are needed for "never reach compaction"; the canary is the one no token bar shows.
- **Probe taxonomy is established practice.** Factory.ai's probe-based eval uses **recall / artifact / continuation / decision** probes, generated from the pre-compression context and graded **blind** by a separate judge against ground truth. The technique is proven in production; the *one-command personal* packaging is the gap this fills.

# Breakdown

## Architecture (proposal)
`/canary` →
1. spawn a **fresh, clean-context subagent** (does not inherit the possibly-degraded window),
2. it reads **this session's raw transcript** from disk (ground truth),
3. it extracts N **session-specific facts** (not generic puzzles),
4. those become probes the **live session must answer from memory — without re-reading the source**,
5. the subagent grades the answers **blind** against the transcript,
6. it returns an objective verdict: `INTACT` / `DEGRADED — lost 3/5: …`.

Two design subtleties to preserve: **answer from memory** (re-reading the file makes it pass trivially and measures nothing) and **session-specific facts** (a generic IQ probe passes even on a context-lost model).

## Probe types (the "any check" menu)
| Probe | Asks | Catches |
|---|---|---|
| **Recall** | "what was the original error message?" | lost facts |
| **Artifact** | "which files did we modify?" | lost work trail (weakest dimension → weight it) |
| **Continuation** | "where were we, what's next?" | lost task-state |
| **Decision** | "why did we choose X?" | lost rationale |

## Decision rule — criticality-gated traffic light
Not count-based. **Any miss on a load-bearing fact = RED**, regardless of how many trivia pass (a session that aces trivia but lost *the core constraint* is the dangerous one).
| Light | Condition | Action |
|---|---|---|
| 🟢 GREEN | all **critical** probes pass | sharp — safe to take another topic; safe to trust it to author the handoff |
| 🟡 AMBER | criticals pass, peripheral misses / borderline | **round off now**; don't load a heavy topic; review any handoff it writes before trusting it |
| 🔴 RED | **any critical** probe fails | don't trust it to author the next context — wrap, write context yourself / from the record, start fresh |

**Honest limit:** the canary reads **now** (current sharpness). "Can it take another topic?" is forward-looking, and the heavy topic itself can tip it — so green = *safe to extend*, not a guarantee. Re-check **after** a heavy load, not only before.

# Recommendations
- **Do (in the PoC):** build the `/canary` tool as a global `~/.claude` slash-command/skill; fresh-subagent grader reading the session jsonl; active probes answered from memory; weight **recall + artifact**; criticality-gated 🟢/🟡/🔴 output; copy into generic SPQR.
- **Validate, do not assume:** active-answer vs. passive-compare grading; subagent-in-session vs. fully separate Claude Code call on the jsonl; whether the critical-fact anchor is owner-supplied or grader-inferred; probe count (proposal 4–6).
- **Defer / out of scope:** the Fable / bika→execution build-flow (owner-regulated); auto-fire after compaction (proposed optional hook — owner asked for manual first); any DOC/SAW footprint (personal, undocumented by choice).

# Descoped
- **Prevention** (re-pinning critical facts, system-prompt re-injection) — this tool is *detection*, not prevention.
- **Pipeline integration / documentation** — Canary B is a personal tool; the pipeline canary is Canary A.

# References
- AGENT_LAWS — Law 3 ("the external record is truth"): `/Users/kovacsmark/.claude/rules/AGENT_LAWS.md` + `.claude/rules/AGENT_LAWS.md`.
- Factory.ai — probe-based evaluation of context compression (recall/artifact/continuation/decision; blind LLM judge): https://factory.ai/news/evaluating-compression
- Companion: `Canary A — Deterministic Handoff Validator — PoC.md`.
