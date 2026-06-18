---
type: poc
title: "SAW-33 — Align generic SPQR with the DOC-21 / FDP ticketing rework"
decides: "How the generic SPQR agent/skill/retro definitions are re-pointed from Notion-comment work-trace to the DOC-21 local-file (hub + output + handover) model so they run correctly in Foodoire"
status: done         # draft | done
date: 2026-06-18
tags: [poc]
---

# SAW-33 — FDP Ticketing Alignment — PoC

## Metadata
**Ticket:** SAW-33 — https://app.notion.com/p/37f68d5de1e881639232db37400532a6
**Authoritative source:** DOC-21 / FDP-49 — https://app.notion.com/p/37f68d5de1e8800b8159fd99dcdf2dbf
**Run:** to be indexed under v1.5 (decisions live here in the PoC; the run index links, does not inline)
**Date:** 2026-06-18
**Session ID:** b25bcd40-e010-4b44-9acf-f02bd53932e7
**Status:** ADOPTED — executed via SAW-33 (run v1.5, group [[03-fdp-ticketing-alignment]]) on 2026-06-18. 40 files edited (1 agent, 4 passes); master validation applied 4 fixes (canonical tags `content/spike` + `content/doc-change`; retro template → local `templates/retro_template.md`). All 5 execution flags adjudicated; 3 process-debt items + POC/BUG roles deferred to owner SAW tickets.

## Context / question
DOC-21 / FDP-49 locked a new Obsidian doc-model for Foodoire on 2026-06-15: per-ticket work-trace lives in **local markdown files** (`hub + output + handover`), not in Notion comments / child pages. The Foodoire vault + templates already exist. SAW-33 must re-point the **generic SPQR** agent + skill + retro **definitions** (in this repo: `docs/agents/`, `docs/skills/`, `docs/retro/`) so agent-driven ticket work writes to the new structure. SAW-33 is definition-only — it states *what changed*; the scope boundary and work split are decided here.

This PoC records the questions, the owner discussion, and the decisions. It is the single source the execution brief is derived from.

## Scope boundary
- **In scope (this repo only):** `docs/agents/` (7), `docs/skills/` (31), `docs/retro/` (5). Full review; edit the affected files.
- **Out of scope:** editing Foodoire files / propagation (separate downstream step); creating or shipping template files (already present in Foodoire); the `Marks-agentic-workflow-SPQR` template repo.

## Decisions (Q → A)

| # | Question | Decision |
|---|----------|----------|
| D1 | Which surface, which repo? | Generic SPQR only (this repo's agents/skills/retro). Foodoire propagation is downstream, not now. No template creation/shipping. |
| D2 | Where does inter-agent handover go? | **Notion ticket comments → local append-only `<TICKET-ID>_handover.md`.** Blocks separated by `---`; the `ticket-comment.md` field contract (still_solving / mode / addressed / expected_outputs / routing / session_id …) is **preserved** — only the transport changes. |
| D3 | Where does the implementation doc go? | Notion "Implementation Notes" child page → local **`<TICKET-ID>_output.md`** with minimal frontmatter (`up: "[[<TICKET-ID>]]"` + one content tag). Reviewer NOTES sections **removed** (→ handover). |
| D4 | Does a local handover break fresh-reviewer sessions / Law-3 (raised as a blocker)? | **No — withdrawn.** The pipeline runs sequentially in **one working directory**; "fresh session" = a fresh Claude conversation (no chat memory), **not** a git clean-checkout. The md files persist on disk in that working dir, so the next agent reads them regardless of commit state. No commit needed between stages. Demonstrated by the real FDP-32/33/36 runs. Only a manual `git stash` / branch-switch / clean checkout mid-pipeline could hide them — not part of the flow. The SAW-32 "uncommitted working tree, no intermediate commits" rule targets **code**, not the work-trace, and does not conflict. |
| D5 | Where does the routing/handoff signal live once comments are gone? | It stays a **field in the handover block** (`routing: → next agent`). The owner now reads the handoff from the files, not Notion comments. |
| D6 | Hub session/cost table — who supplies the numbers? | The agent writes its **`session_id` row** (`echo $CLAUDE_CODE_SESSION_ID`; `—` sentinel if unknown). `cost_total` stays `null` and is **owner-filled** post-session via `/usage`. The job is to provide the slot, not to self-measure tokens (agents cannot, and it would conflict with the retro "do not instrument" rule). |
| D7 | Who creates the hub, and when? | The **executor agent creates the hub** from template: **Praetor** for DEV (OPUS), **Quaestor** for SPIKE (EXPLORACIO) and DOC. Consilium (skippable in OPUS) only appends its handover block; the executor seeds the hub session table from the existing handover blocks. **Backfill invariant:** any agent that finds the hub missing creates it. (Generalizes the owner's "Praetor creates / backfills" to the pipelines where Praetor never runs.) |
| D8 | Identity / numbering token in generic files? | Use a project-neutral placeholder **`<TICKET-ID>`** that resolves to the **consuming project's** per-ticket scheme (Foodoire → `FDP-N`), with `FDP-N` shown as the example. `DEV-XXX` demoted to legacy alias only. **Unify** the two current tokens (`DEV-XXX` + `[TICKET-ID]`) into the one placeholder. **Note:** `SAW` tickets (SPQR self-development, incl. SAW-33) live in a **separate Notion-based upgrade/documentation flow** (PoC + run container under `docs/spqr_self/`); they do **not** use this per-ticket hub+output+handover vault model, so `<TICKET-ID>` is never resolved to `SAW` by these agent/skill files. |
| D9 | What stays in Notion? | **Only the ticket definition + creation** (central `FDP-N` numbering, Notion-assigned; `Ticket type` field; new Notion templates). `ticket-slicing.md` + `censura-ticketing-*` keep Notion ticket creation — do **not** rip Notion out of them. Everywhere else: work-trace → local files; **no more inter-agent Notion comments** for the work-trace (Censura too: verdict → handover + `LESSONS.md`). |
| D10 | Tool permissions — agents currently cannot write files | **Big gap.** Every agent except Praetor has file-write prohibitions and no `Write/Edit` (old model wrote only to Notion). Add **scoped `Write/Edit` to the `work_documents/` vault** to Senate, Tribunus, Probator, Curator, Quaestor, Retrospector. Guardrails: **NEVER modify the SPQR process files** (`docs/agents/`, `docs/skills/`) **or `CLAUDE.md`**; **NEVER delete a file** under any circumstance; writes are **append / add-new**, not overwrite. Reviewers still **never write code/source**. |
| D11 | Veto / revision transport | Vetoing agent appends a **veto block** to `<TICKET-ID>_handover.md` (`veto_from` / `issue` / `fix_contract` / `resubmit_to` / `routing`). Praetor reads it, fixes, writes **`<TICKET-ID>_output_revN.md`** (delta: CHANGED / NOT TOUCHED / SCOPE NOTE) + appends a "Revision #N" block. Matches the real FDP-36 (2 veto rounds). |
| D12 | Per-type output specifics | DOC output = **change-manifest** (files/sections touched, DONE/FLAGGED, ⚠️ flags, `modifies:` property). BUG = **fix-doc**. SPIKE output = existing structure **minus** the top metadata block (hub owns identity). POC currently informal / not-ticketed (owner-driven, outside SPQR). **POC & BUG handover-chain roles owner-deferred (TBD).** |
| D13 | Retro alignment depth | **Full** alignment (owner rejects the DOC-21 "retro process owned by DOC-018" carve-out). Local file; frontmatter `content: retro`, `retro_n` (start at 1, increment — creator reads prior retro for the next number), `phase` (= project phase), `verdict` (the retro template's **own** vocabulary, not Censura GREEN/RED), `tickets_reviewed: [[<TICKET-ID>]]` hub wikilinks; `Retroactio.md` as the retro MOC. **Input re-pointed:** the retro reads the Censura **verdict from the local `<TICKET-ID>_handover.md`**, not Notion comments (LESSONS.md unchanged). |
| D14 | Reviewer NOTES sections | **Removed** — duplicate of the handover. Reviewers append their block to `_handover.md` only; the output carries no `--- X NOTES ---` sections. All skill lines referencing "NOTES sections" are rewritten accordingly. |
| D15 | Which ticket types / pipelines adopt the local-file model? | **All consuming-project types**, each in its own pipeline — not just DEV. **DEV** (OPUS: Praetor executes). **SPIKE** (EXPLORACIO: Consilium → Quaestor → Censura). **DOC** (EXPLORACIO-family: Quaestor doc-execute → Censura) — the documentation process now also produces a local hub+output(change-manifest)+handover, same as the others. **BUG** + **POC**: the hub+output+handover structure stands, but **handover-chain roles are owner-deferred**; POC is currently informal / not-ticketed. Affected skills by type — **SPIKE:** `quaestor.md`, `quaestor-relatio.md`, `quaestor-relatio-output.md`, `spike-document.md`; **DOC:** `quaestor-doc-execute.md`, `doc-maintenance.md`; **BUG (standalone):** `debugging-tribunus-input.md` (roles otherwise deferred). |

## Findings (roundtable, 2026-06-18)
Two from-scratch personas (Dev Process Architect + Agentic Trends Expert) pressure-tested the master's initial reading. Net:
- **Reframe (both):** SAW-33 is not only "align text" — the file-based transport (`_handover.md`, hub, session table) does not yet exist in `docs/` and is **authored by porting** the existing Notion field-contracts. Captured in D2/D6/D7/D10.
- **Durability blocker (Dev Process Architect):** raised, then **resolved** — see D4 (rested on a clean-checkout assumption that the flow does not perform).
- **Genericity (Agentic Trends Expert):** placeholder token over hardcoded `FDP-N` — adopted as D8.
- **Actionability gaps:** append contract (who-creates / `---` delimiter / locate-last / session_id capture) must be stated, not just pointed at a template — folded into the execution brief via D2/D7. `session_id` capture (`echo $CLAUDE_CODE_SESSION_ID` + sentinel) reused verbatim.
- **Not flagged by either, found by master sweep:** the **tool-permission contradiction** (D10) — the single most output-improving find.

## Recommendation / decision
Adopt D1–D14. The **execution brief** (separate file, derived from this PoC) maps each decision to file-level edits (which file, what change, how) for a stateless execution agent, grouped for sequential delivery. The v1.5 run index links this PoC and the brief; it does not inline the decisions.

## Deferred / flagged (owner-owned)
- **Process gap:** the upgrade-agent pipeline does not prescribe "decisions → PoC (template) first, then execution brief"; it says "record decisions in the run container." → flag a **SAW candidate** at session end (this run found it).
- **POC & BUG handover-chain roles** — owner-regulated, TBD (D12).
- **Hub `cost_total` source** — owner-filled via `/usage` (D6); no agent instrumentation.

## References
- DOC-21 / FDP-49 — the authoritative target conventions.
- Foodoire real artifacts — `…/Foodoire/docs/work_documents/dev_logs/opus_outputs/FDP-32|33|36/` (hub + output + handover + rev) — the ground-truth pattern this PoC aligns to.
- `docs/skills/ticket-comment.md` — the field contract preserved under D2.
- `docs/spqr_self/poc/Git Branching Strategy — PoC.md` — sibling process-rework PoC; house style + the SAW-32 "uncommitted working tree" rule referenced in D4.
- `docs/upgrade/upgrade-agent.md` — the pipeline whose missing PoC-first step is flagged above.
