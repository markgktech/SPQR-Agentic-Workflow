## Metadata
**Ticket (SAW):** https://app.notion.com/p/38068d5de1e881dc87bbf685e3d02a4b
**Ticket (DOC schema):** https://app.notion.com/p/38068d5de1e881249d90ca1ea5afb1a3
**Epic:**
**Component:** SPQR / Canary
**Document status:** BRIEF — not started (proposal to validate)
**Date:** 2026-06-15
**Session ID:** — (pending PoC execution)
**Usage:** — (pending PoC execution)
**Session scope:** The deterministic, non-LLM validator that runs over a written SPQR handoff artifact (`_handover.md` + hub) and flags self-contradiction / dropped items / chain breaks at the commit gate.
**Purpose:** Propose Canary A as a PoC brief — well-prepared proposals ("how the meal *could* be cooked"), **not** fixed decisions. The PoC session refines, decides, and validates; nothing here is canon.

---

# Overview
This PoC explores a **deterministic handoff-validator** for the SPQR pipeline: a small script that reads the md handoff an agent already wrote, **recomputes** what the agent *should* have concluded, and compares. It is **not** an LLM probe and never runs inside an agent session — so it adds **zero agent context cost**. **In scope:** the check classes, where/what runs it, where the result is written, and the dependency on the schema (DOC) + skill emission (SAW). **Out of scope:** the deeper *semantic* derailment check (that is Canary B's job), and building the mechanics now.

This is the pipeline-side, automatic, documented canary — the counterpart to **Canary B** (the personal, on-demand session-sharpness probe). The two are **complementary layers that meet at the handoff**: A is the cheap always-on net (mechanical infidelity); B is the expensive deep check (semantic derailment).

# Motivation
SPQR agents are stateless: each starts cold, works, writes a structured handoff, and routes on. Errors therefore **do not accumulate across agents** — they crystallize **within a session and freeze into the handoff**, which the next stateless agent then loads as truth. A corrupted handoff silently poisons the whole downstream chain.

The skill files are already full of invariants phrased as **NEVER / MAX / ONE** ("never omit `session_id`", "MAX 2 BLOCKERS", "one veto per run", "no silent clean pass", "verdict only, no veto"). Today these are *hoped-for* — honored only if the agent does not derail. Canary A **compiles the existing prose rules into an executable check** at the commit gate, so they are enforced regardless of agent state. It invents no new rule.

# Findings
- **The verdict is a pure function of the decision tags.** Per `consilium-output.md`: `BLOCKED ⟺ any unresolved BLOCK`; `APPROVED_WITH_RISK ⟺ RISK present, no BLOCK`; `APPROVED ⟺ all DECIDED`. So the validator can **recompute the verdict from the tags and compare to the stated verdict** — a mismatch is a derailment signal. This is the showcase check, fully deterministic, no LLM.
- **A self-produced artifact can only be checked for *internal* consistency.** A derailed session can write a wrong ledger *and* a matching wrong output (garbage-in-garbage-in-**match**). So A's ceiling is internal consistency + serialization fidelity; catching "consistently confident but wrong" needs an external grader against the raw transcript — that is **Canary B**, not A. Do not over-engineer A into a fuzzy thing.
- **The result has a deterministic home.** Post-DOC-21, `_handover.md` is a local append-only file and the hub frontmatter is the queryable node. The validator writes a `canary:` line in the handover and `canary_status` in the hub; Dataview displays it. A property does **not** self-signal — the script writes it; the blocked commit / red Dataview cell shows it.
- **The repo already has the runtime.** `.pre-commit-config.yaml` + `.gitleaks.toml` exist; a pre-commit hook is the natural home, firing exactly at the branch-end HITL the owner already does (jegy=branch, owner commits at the end).

# Breakdown

## Check classes (all parse + compare, no LLM)
| Class | Example check |
|---|---|
| **1. Structural completeness** | `session_id` / `expected_outputs` / `routing` never omitted; Praetor `impl_doc` URL present before routing; `routing` names a legal next agent |
| **2. Internal consistency** | **verdict ⟺ tags** recomputed; `≤2 BLOCK`; `dissent` / `unresolved_conflict` non-empty if a disagreement was raised; no silently dropped `OPEN` |
| **3. Cross-chain continuity** | `addressed[N+1]` ⟺ `expected_outputs[N]`; chain order Praetor→Tribunus→Probator→Curator; veto budget ≤1 Tribunus + ≤1 Probator / run; all `session_id` present; Curator issues **no** veto (role boundary) |

## Worked example (the planted-error case)
A Consilium handover states `verdict: APPROVED` but its `decisions:` list contains a `[BLOCK]` tag. Validator: parse tags `{DECIDED, BLOCK}` → recompute → `BLOCKED` required → `APPROVED` stated → **FAIL: verdict_tag_mismatch** → write `canary: FAIL [verdict_tag_mismatch]` + `canary_status: FAIL` → exit non-zero → commit blocked at the HITL gate.

## Where / what runs it (proposal)
- **What:** ~100-line script (Python fine; Node fine) — parse frontmatter + decisions block, recompute, compare, write result, exit code. Lives in a PoC because a script is a runnable mini-project.
- **Where (primary):** pre-commit hook via the existing `.pre-commit-config.yaml` → blocks the branch commit on FAIL.
- **Where (secondary):** on-demand (`canary.py FDP-N`); and a Dataview dashboard note in Obsidian for passive cross-ticket visibility (display only — Obsidian cannot do the reconciliation logic; DataviewJS is fragile for cross-file checks).

## The fork to validate — End-sweep tag-ledger
A's reconciliation today is limited to *internal* consistency because the discussion's decisions only become structured **at output**. To also catch **discussion→output serialization drops**, the Consilium **End-sweep** (which already reviews all decisions) could **emit a structured tag list** as an in-session ground truth. **Validate** whether the small added context is worth the stronger check. The ceiling is still serialization fidelity — pre-end-sweep derailment remains B's job.

# Recommendations
- **Do (in the PoC):** build the deterministic validator for Class 1–3; recompute verdict⟺tags as the core; write `canary:` + `canary_status`; wire a pre-commit hook; prototype on **mock fixtures** first, finalize after DOC + SAW land.
- **Validate, do not assume:** the End-sweep tag-ledger addition; the exact parse-stable field formats (must track the post-DOC-21 handover schema); pre-commit vs. on-demand as the primary trigger.
- **Defer / out of scope:** semantic derailment detection (Canary B); editing hub/handover templates (the DOC ticket reserves the field; population follows once the shape is locked here).

# Descoped
- **Semantic / LLM-judge checking** — explicitly Canary B's layer; not built here.
- **Template edits + legacy backfill** — owned by the DOC ticket; never stamp closed hubs.
- **Alerting infrastructure** — none; the blocked commit + Dataview cell are the signal.

# References
- SAW ticket — Align SPQR skills with Canary A: https://app.notion.com/p/38068d5de1e881dc87bbf685e3d02a4b
- DOC ticket — Canary doc-model (schema): https://app.notion.com/p/38068d5de1e881249d90ca1ea5afb1a3
- DOC-21 / FDP-49 — Obsidian + ticketing rework (hub + local append-only handover): https://app.notion.com/p/37f68d5de1e8800b8159fd99dcdf2dbf
- `docs/skills/consilium-output.md` — verdict rules (pure function of tags); `consilium-discussion.md` — decision tags + End-sweep; `ticket-comment.md` — NEVER-omit fields.
- `.pre-commit-config.yaml`, `.gitleaks.toml` — existing pre-commit runtime.
- Companion: `Canary B — Session Sharpness Probe — PoC.md`.
