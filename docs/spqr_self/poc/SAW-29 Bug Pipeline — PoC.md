---
type: poc
title: "SAW-29 — Bug-pipeline: define the bug-type ticket flow"
decides: "The lean, distinct bug-type pipeline (stages, agent mapping, routing, docs) reusing existing SPQR primitives — resolving the SAW-33/D15 + handover_template 'BUG: TBD' deferral"
status: done         # draft | done
date: 2026-06-18
tags: [poc]
---

# SAW-29 — Bug Pipeline — PoC

## Metadata
**Ticket:** SAW-29 — https://app.notion.com/p/Bug-pipeline-define-the-bug-type-ticket-flow-37668d5de1e8815090cae981644ce9c7
**Parent theme:** Operations / process-debt (Relation ticket = epic; excluded from scope)
**Run:** to be indexed under v1.5 as a new group (decisions live here; the run index links, does not inline)
**Date:** 2026-06-18
**Session ID:** 10b672b5-893b-40c3-8870-db8f53c527d8
**Status:** ADOPTED — executed via SAW-29 (run v1.5, group [[04-bug-pipeline]]) on 2026-06-18. 9 files, single-agent run (7-FILES cap owner-overridden): NEW `docs/skills/bug-pipeline.md` + `git-workflow.md` + 5 agent mandates (`praetor`/`probator`/`senate`/`tribunus`/`curator`) + `debugging-tribunus-input.md` + `session-starters.md`. Master verification clean; Flag #1 (Probator append-only sink-write) confirmed + recorded in D8. D10 descoped; `quaestor.md` unchanged (D12); Foodoire-owned template edits flagged downstream. Owner commits/pushes.

## Context / question
The pipeline was designed for DEV/SPIKE tickets; the bug-type flow was intentionally deferred until real bugs existed. Five FDP bug tickets now exist, so a **lean** bug flow is needed — **distinct from DEV (OPUS) and SPIKE (EXPLORACIO)**, right-sized (not full feature ceremony), reusing existing primitives (Senate/Praetor/Probator) at right-sized effort, with model/effort noted.

SAW-29 directly resolves a prior deferral: SAW-33 / D15 left **"BUG handover-chain roles owner-deferred"**, and `handover_template.md` literally carries **"BUG: TBD (owner regulates)"**. This PoC fills that in.

The Foodoire repo already pre-scaffolds bugs: `bug_output_template.md` exists; `ticket_hub_template.md` carries a BUG identity block (`severity` / `entry: wild|dev-linked` / `spawned_by` / `affects`); each flow has its own `dev_logs/<flow>_*` output folder. The design rides this existing scaffold.

## Scope boundary
- **In scope:** generic SPQR (CORE surface — propagates) — a new bug-flow **process-doc** (`docs/skills/bug-pipeline.md`) + **session-starter** entries; `git-workflow.md` (bug branch); the **BUG handover-chain** authored generic-side in `bug-pipeline.md`; agent-mandate touch-points where the bug flow changes behaviour OR where the Active-in/PIPELINE enumeration must acknowledge CORRECTIO: `praetor.md`, `probator.md`, `senate.md`, `tribunus.md`, `curator.md`, `debugging-tribunus-input.md` (`quaestor.md` unchanged — D12). **9-file single-agent run** (7-FILES cap owner-overridden, SAW-33 precedent). Target field: "process-doc + session-starters".
- **Out of scope:** Foodoire propagation (downstream, SAW-38 mechanism); the **Foodoire-owned template edits** (`handover_template.md` "BUG: TBD" → CORRECTIO chain, `bug_output_template.md` alignment, `correctio_outputs/` folder) — **project-owned** (not in the propagated CORE surface), flagged as a downstream owner-run action against Foodoire; SAW-21 (effort/model routing as a ticket — referenced only); SAW-2/SAW-8 (ticket-creation — already done); the Relation-ticket epic; concrete model-tier pinning (D10, descoped — owner runtime decision).

## Routing model — two axes (both already in the hub data model)
- **Axis 1 — origin:** `entry: wild | dev-linked`. `dev-linked` (cause near a known recent change, `spawned_by` set) → light triage folded into Praetor. `wild` (unknown origin) → may need a dedicated investigation stage.
- **Axis 2 — severity:** `severity: HIGH / MED / LOW` (existing hub vocabulary). Drives model/effort + conditional re-entry.

## Decisions (Q → A)
Status legend: ✅ confirmed · ✂️ descoped (owner-reopenable).

| # | Question | Decision |
|---|----------|----------|
| D1 ✅ | Flow name (Roman sibling of OPUS/EXPLORACIO)? | **CORRECTIO** (owner pick). Drives the output-folder name (D19 → `correctio_outputs/`) and the session-starter label. |
| D2 ✅ | Default flow shape? | **Position B, 2 sessions.** `owner files bug → Praetor (investigate-first → HITL cause-note gate → fix) → Probator (verify + close)`. Leanest shape that still preserves one independent check (Probator). |
| D3 ✅ | Separate triage/Tribunus stage by default? | **No.** Triage folds into Praetor as a **structural investigate-first gate**: Praetor produces the cause-note and STOPs for owner sign-off **before writing any code**. The only thing a separate investigator objectively buys is anchoring-bias-free root-cause; for most bugs the HITL gate (owner = fresh eyes) covers it. |
| D4 ✅ | HITL cause-note gate contract? | Praetor drafts `bug_output` **SYMPTOM/REPRO + ROOT CAUSE** + sets hub identity (`severity`, `entry`, `affects`) + proposed **FIX direction**, **reports to owner, owner signs off → only then code.** The bug flow's single mandatory HITL. |
| D5 ✅ | What is cut from the default? | **Consilium** (bug's unknown is root-cause, not design — triage replaces it); **Tribunus code-review** (one reviewer suffices for a small fix; Probator is more essential); **Curator** (a behaviour-restoring fix doesn't change ops posture). |
| D6 ✅ | The one independent check? | **Probator.** Verifies **repro pre-fix (must reproduce) + post-fix (must not), evidenced in handover** + tests + regression test (conditional, D6b) + writes the close + the routine knowledge entry (D8). |
| D6b ✅ | Regression test — mandatory? | **Conditional with a stated trigger:** a regression test is required **unless** the owner tags the ticket `no-repro-harness` / "untestable because X" (recorded in the hub). Unconditional-mandatory = feature ceremony; condition-with-no-trigger = non-actionable — so it gets an explicit, owner-set trigger. |
| D7 ✅ | Censura — needed? | **Conditional, decision-triggered — not a quality gate.** Runs only when the fix produced a **durable decision** that must expand the repo project-knowledge base. Routine lessons do NOT need Censura. |
| D7b ✅ | Decision definition + flag mechanism? | **Decision = a choice a future ticket's agent would behave differently knowing.** Flag `decision: yes` raisable by **whoever first sees it** — Praetor at the HITL gate, or Probator at close — **owner confirms** → Censura runs (expands the knowledge base). |
| D8 ✅ | Knowledge sink? | **Abstract "project-knowledge sink" — not hardcoded.** Today = `LESSONS.md`; soon = the **Warehouse** (v1.5). Routine lesson always written at close; decision → Censura records. The Warehouse swap stays a one-line change. **Tool-permission (resolved at execution — Flag #1):** Probator gains scoped **append-only** write to the sink at CORRECTIO close (Probator is the closer; no later writer exists in the default 2-session flow), mirroring Senate's `LESSONS.md` write. This supersedes the brief's "handover-only Write" line (PoC-wins). Confirmed by master at verification. |
| D9 ✅ | Severity vocabulary? | **`HIGH / MED / LOW`** (existing hub field) — not sev1/2/3. Drives model routing (D10) + escalation (D11). |
| D10 ✂️ | Model/effort routing per stage? | **DESCOPED — owner runtime decision, no tiers pinned.** The flow doc *notes* that model/effort is owner-selected per bug (guided by `severity`/`entry`) — satisfies the AC "model/effort noted" without binding tiers. Non-binding suggestion may be included (e.g. diagnosis-heavier on `wild`/HIGH). Reopenable. |
| D11 ✅ | Escalation triggers (mechanical only)? | `entry: wild` **and** Praetor reports "cause not localizable" → **+ investigator before Praetor** (D12). `severity: HIGH` or fix touches a critical surface → **+ Tribunus code-review after Praetor**; **+ Curator only if** the fix touches deploy/config/runtime. **Censura: never via severity** — a bug too big for this flow is re-filed as a feature (earns ceremony as OPUS). |
| D12 ✅ | Investigator selection when escalated? | **Tribunus standalone-debug by default** (code-near, existing primitive). If Tribunus returns "root cause not localizable to a file/subsystem" → **the owner files a normal EXPLORACIO spike ticket** (genuine research); Quaestor runs the standard spike flow. **No in-CORRECTIO quaestor mode — `quaestor.md` unchanged** (respects "EXPLORACIO only"). One default + one mechanical escalation (out to a spike ticket). |
| D13 ✅ | Branch granularity? | **`fix/<TICKET-ID>-slug`, one bug = one branch, no batching.** Keeps ticket↔branch↔verify 1:1 for Probator's per-ticket receipt. Batching only via explicit owner tag. Mechanics in `git-workflow.md`. |
| D14 ✅ | Where does the cause-note live? | **Local** — `bug_output` ROOT CAUSE section + hub identity. **Not** a Notion comment. (Owner reads it in the repo + at the HITL gate.) |
| D15 ✅ | Bug found mid-feature work? | **Always a separate owner-initiated bug ticket**, `entry: dev-linked` + `spawned_by: [[FDP-parent]]` (parent gets `spawned: [[BUG-...]]`). Praetor **never** fixes a pre-existing bug inline (protects feature branch + Censura scope). Data model enforces this. |
| D16 ✅ | Edge/terminal states? | **Full proposal adopted.** (a) **"not a bug"** → triage re-routes to OPUS/EXPLORACIO or closes invalid; (b) **can't-reproduce** → owner-close terminal state + reopen affordance; (c) **reopened-after-close** → **spawn a NEW linked ticket** (`spawned_by` the original) for trace integrity — not a re-run of the closed ticket. |
| D17 ✅ | Sizing — who/when? | Praetor sets at the triage/HITL gate; informs the owner's model/effort call (D10). Notion `Size` + hub. |
| D18 ✅ | Documentation process? | Bug folder `dev_logs/correctio_outputs/<FDP-N>_<Title>/`. **Praetor** creates the **hub** (uncomment the BUG identity block) + **`bug_output`** (from `bug_output_template.md`) + **handover**; **Probator** appends its handover block; **Censura** (if triggered) appends + writes the knowledge entry. Reviewer notes live in `_handover.md` only. |
| D19 ✅ | Output folder name? | **`correctio_outputs/`** (from D1) — matching the per-flow convention (`opus_outputs`, `exploracio_spiking`, `poc`, `retroactio`). |
| D20 ✅ | Notion boundary? | **Read-only for agents.** The **owner** moves the bug ticket through stages; Praetor/Probator/etc. only **read** the ticket definition, never write Notion properties. Consistent with SAW-33/D9. |
| D21 ✅ | Ticket-creation tie-in? | **Confirm existing rule** — `ticket-slicing.md`: "Bug tickets owner-initiated only", `Ticket type = Bug`. No new creation logic needed. |
| D22 ✅ | Process-doc placement (surface)? | **`docs/skills/bug-pipeline.md`** (the flow doc) + entries in `docs/agents/session-starters.md`. |
| D23 ✅ | BUG handover-chain (resolves SAW-33/D15 "roles deferred")? | BUG chain = **Praetor → Probator → [Censura iff decision]**, with `[investigator →]` prefix and `[→ Tribunus-review]` / `[→ Curator]` conditional inserts. **Authored generic-side in `bug-pipeline.md`.** The literal `handover_template.md` "BUG: TBD" string edit is **Foodoire-owned (project-owned, not propagated)** → downstream owner action, not this run. **Hops are owner-launched** (owner moves the ticket + starts each session); context is handover-driven. |
| D24 ✅ | Validation? | Dry-run-map the **5 existing FDP bugs** onto the flow at execution/wrap-up (acceptance test, not a design constraint) — any ticket that can't route cleanly is a finding. |
| D25 ✅ | Skill + phase-boundary convention? | The CORRECTIO flow-doc + any stage skills **follow the existing skill convention** (no central template — extracted from `docs/skills/`): frontmatter (`name`/`description`); numbered **LOAD ORDER** (AGENT_LAWS → CLAUDE → ticket + `<TICKET-ID>_handover.md`/`_output.md` → next-phase file); **explicit phase boundaries mirroring OPUS/EXPLORACIO** — distinct input → work/HITL → output phases, each a **cold-start** session (Law 3), with hard gates ("never load output before the phase closes", "never close the HITL gate without owner signal" — Law 2); a closing **NEVER/CONSTRAINTS** block citing Laws. The **investigate-first cause-note gate (D4) is the canonical phase boundary** (modelled on Consilium's owner-closes-discussion gate). **Planning decided (D25):** a bug-mode branch in existing agent mandates + one `bug-pipeline.md` orchestration doc (no new per-stage skill triads). |
| D26 ✅ | Bug-flow veto/revision path? | When Probator's verification fails (repro persists post-fix / tests fail), Probator raises **intercessio** → **`praetor-revision`** (Praetor fixes only the vetoed issue, writes `_output_revN.md`) → re-verify. **Reuses the existing OPUS veto/revision mechanic** (`collegium-veto.md`, `praetor-revision.md`) — no new mechanic; `bug-pipeline.md` references it. |
| D27 ✅ | Which agent mandates acknowledge CORRECTIO? | Beyond behaviour edits, the **Active in / PIPELINE POSITION** enumerations must not contradict CORRECTIO: update `praetor.md` (executor), `probator.md` (verify+close), `senate.md` (conditional Censura), **`tribunus.md`** (standalone-debug investigator + HIGH code-review re-entry), **`curator.md`** (conditional HIGH/ops re-entry). `quaestor.md` unchanged (D12). Found by the **planning completeness audit** → 9-file set; **single-agent run, 7-FILES cap owner-overridden** (SAW-33 precedent). |

## Findings (roundtable + owner discussion, 2026-06-18)
- **Both personas:** skeleton sound and correctly lean, but "right-sized" / "lighter effort" / the triage→fix handoff are non-agent-actionable as phrased → pinned via fields (`severity`/`entry`) + the investigate-first gate. Neither wanted new agents.
- **Owner-driven reframe:** the real router is **two axes** (origin `entry` + `severity`), both already present in the hub. This collapses the default to a **2-session** flow (Position B) — triage folds into Praetor; Tribunus/Curator/Censura become conditional.
- **Censura reframed (owner):** from quality-gate (cut) to **decision-triggered knowledge-base expansion** (kept, conditional).
- **Scaffold already half-built:** `bug_output_template.md`, hub BUG identity block, per-flow output folders, and `handover_template` "BUG: TBD" — SAW-29 completes the design the templates anticipated.

## Recommendation / decision
Adopt D1–D9, D6b, D11–D27 (all ✅). D10 is ✂️ descoped (owner runtime decision; flow doc only *notes* the model/effort dimension to satisfy the AC). On owner Phase-3 close, derive the execution brief (planning.md) mapping each decision to file-level edits; the v1.5 run index links this PoC as a new group.

## Open / descoped (owner-owned)
- **D10 (descoped)** — concrete model tiers per stage; owner sets per bug at runtime. Reopenable as a later SAW candidate if a fixed routing is wanted.
- **Foodoire-owned follow-up (flagged, downstream)** — apply the CORRECTIO chain to Foodoire's `handover_template.md` ("BUG: TBD" → chain), align `bug_output_template.md`, create `dev_logs/correctio_outputs/`. Project-owned (not in the propagated CORE surface); owner-run against Foodoire, alongside/after the pending v1.3→v1.5 propagation. Candidate SAW ticket (owner creates).
- **D24 validation** — dry-run-map the 5 FDP bugs onto CORRECTIO once G4 lands (proves routability without touching Foodoire).

## References
- SAW-33 PoC — `docs/spqr_self/poc/SAW-33 FDP Ticketing Alignment — PoC.md` (D15 deferral this resolves; house style).
- Foodoire scaffold — `…/Foodoire/docs/work_documents/templates/bug_output_template.md`, `ticket_hub_template.md`, `handover_template.md`; `dev_logs/opus_outputs/FDP-32|33|36/` (ground-truth folder pattern).
- `docs/agents/{praetor,probator,senate,tribunus}.md`, `docs/skills/{debugging-tribunus-input,ticket-slicing,git-workflow}.md` — primitives reused.
