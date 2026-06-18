---
up: "[[v1.5]]"
group: "CORRECTIO bug pipeline (SAW-29)"
order: 4/4
tags: [group]
---

# Group 4 — CORRECTIO bug pipeline (SAW-29)

## Brief

GROUP: CORRECTIO bug pipeline — generic-side definition of the lean bug-type flow (flow-doc + session-starter + agent mandates)
ORDER: 4/4
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/04-bug-pipeline.md
RATIONALE: one cohesive generic-side definition of the CORRECTIO bug flow across the CORE surface; single mental model, no cross-file conflicts — 9 files, single agent (7-FILES cap owner-overridden, SAW-33 precedent: one coherent surface kept under one agent that holds the whole CORRECTIO model — this is exactly the inconsistency-class the planning audit caught)
FILL_CHANGES_MADE: yes

SOURCE_OF_TRUTH:
  docs/spqr_self/poc/SAW-29 Bug Pipeline — PoC.md   ← AUTHORITATIVE for CONTENT (decisions D1–D25). If this brief and the PoC ever disagree, the PoC wins. Do not re-decide; apply.

PRE_FLIGHT (load before editing):
  - docs/spqr_self/poc/SAW-29 Bug Pipeline — PoC.md   (the decisions D1–D25 — read in full first)
  - docs/upgrade/execution.md   (execution protocol)
  - docs/skills/consilium-input.md + consilium-discussion.md   (FORM exemplar — skill phase-boundary convention: LOAD ORDER → phases → gates → NEVER; D25)
  - docs/skills/probator-input.md + docs/skills/curator-input.md   (FORM exemplar — lean input→output skill shape with explicit "do not load output before X" gate)
  - docs/agents/{praetor,probator,senate,tribunus,curator}.md + docs/skills/debugging-tribunus-input.md + docs/skills/git-workflow.md + docs/agents/session-starters.md   (the files being edited — read current form first)
  - docs/skills/{collegium-veto,praetor-revision}.md   (the veto/revision mechanic the bug flow REUSES — D26; read, do not edit)
  - /Users/kovacsmark/Documents/RecipeAPP/Foodoire/docs/work_documents/templates/{bug_output_template,ticket_hub_template,handover_template}.md   (FORM reference ONLY — the consuming-project artifacts the runtime instructions describe; DO NOT edit these — Foodoire is project-owned/out of scope)

CONVENTIONS (mandatory — match existing form, invent no new shape):
  - `bug-pipeline.md` is a NEW skill — it MUST follow the existing skill convention extracted from docs/skills/: frontmatter (`name`/`description`); numbered LOAD ORDER (AGENT_LAWS → CLAUDE → ticket + local `<TICKET-ID>_handover.md`/`_output.md` → next-phase ref); explicit phase boundaries mirroring OPUS/EXPLORACIO (input → work/HITL → output, each a cold-start session, Law 3); a closing NEVER/CONSTRAINTS block citing Laws (D25).
  - Agents keep their IDENTITY / PIPELINE / STAGE SKILLS / LAWS / ALLOWED TOOLS / NEVER structure. Add a BUG-mode section/pointer; edit in place, do not restructure.
  - Severity vocabulary is `HIGH / MED / LOW` (existing hub field) — never sev1/2/3 (D9).
  - The bug flow reuses the SAW-33 local work-trace model (hub + `<TICKET-ID>_output.md` + `<TICKET-ID>_handover.md`); the bug output uses the existing `bug_output_template.md` shape (SUMMARY · SYMPTOM/REPRO · ROOT CAUSE · FIX · VERIFICATION · REGRESSION RISK); reviewer notes live in the handover only.
  - The PoC is authoritative for CONTENT; the existing skill/agent forms are authoritative for FORM.

GUARDRAIL — DO NOT CONFUSE TWO LEVELS:
  - YOUR job now IS to edit docs/agents/ and docs/skills/ in THIS (SPQR) repo. You are authorised to do so.
  - The runtime NEVER rules you WRITE INTO the bug-flow agent definitions (never modify SPQR process files/CLAUDE.md, never delete, append-only, reviewers never write code) are constraints on the CONSUMING-PROJECT agents — NOT on you, the execution agent, right now.
  - Never touch a consuming project (Foodoire); never edit its templates or create its folders; never commit or push; never modify the MAIN folder-note (v1.5.md) or sibling sub-docs.

EXECUTION ORDER (resumable passes — report per pass, then continue):
  PASS 1 — Foundations: the new flow-doc + branch convention (everything else points at these)
  PASS 2 — Agent mandates + launch + escalation wiring
  If context runs low: finish the current file, write Changes Made for completed passes, report which pass to resume from.

FILES:

  # PASS 1 — Foundations
  docs/skills/bug-pipeline.md (NEW): the CORRECTIO flow-doc (D2,D3,D4,D6,D6b,D7,D7b,D8,D9,D11,D12,D16,D22,D25). Define: the two routing axes (`entry: wild|dev-linked` + `severity: HIGH/MED/LOW`, both on the hub); the DEFAULT 2-session flow (Praetor investigate-first → HITL cause-note gate → fix; Probator verify+close); the investigate-first cause-note gate as the canonical phase boundary (Praetor STOPs for owner sign-off before any code — modelled on Consilium's owner-closes-discussion gate); Probator close = repro pre/post evidence + tests + conditional regression test (required unless owner tags `no-repro-harness`/untestable — D6b) + writes the routine knowledge entry to the project-knowledge sink (LESSONS.md today → Warehouse soon, D8); the `decision: yes` flag (raisable by Praetor@HITL or Probator@close, owner confirms) → conditional Censura (knowledge-base expansion, NOT a quality gate); escalation triggers (entry=wild & unlocalizable → investigator before Praetor; severity=HIGH/critical-surface → +Tribunus-review, +Curator iff deploy/config/runtime; too-big → re-file as feature); investigator selection (Tribunus standalone-debug default; if not localizable to a file/subsystem → owner files a normal EXPLORACIO **spike ticket**, no in-CORRECTIO quaestor mode — D12); the **veto/revision path** when Probator verification fails (Probator intercessio → praetor-revision → re-verify, REUSING `collegium-veto.md` + `praetor-revision.md`, no new mechanic — D26); edge/terminal states (not-a-bug → re-route/invalid; can't-reproduce → owner-close+reopen; reopened → NEW linked ticket); doc layout `dev_logs/correctio_outputs/<FDP-N>_<Title>/`. Follow the skill convention (frontmatter, LOAD ORDER, phase gates, NEVER) — D25. Model/effort is owner-set at runtime (note the dimension; pin no tiers — D10 descoped).
  docs/skills/git-workflow.md: D13 — add the bug branch convention `fix/<TICKET-ID>-slug` (sibling of `feature/<TICKET-ID>-slug`); one bug = one branch, no batching (batching only via explicit owner tag). Mechanics only; keep policy references intact.

  # PASS 2 — Agent mandates + launch + escalation
  docs/agents/praetor.md: D3,D4,D13,D18 — add a BUG (CORRECTIO) mode: Praetor is the bug executor; investigate-FIRST (draft bug_output SYMPTOM/REPRO + ROOT CAUSE + set hub identity severity/entry/affects + proposed FIX direction) → HITL cause-note gate (report to owner, STOP, owner signs off) → only then fix on `fix/<TICKET-ID>-slug`; creates the BUG hub (uncomment the BUG identity block) + bug_output (from bug_output_template) + handover; may raise `decision: yes` at the HITL gate; pointer to load docs/skills/bug-pipeline.md for bug tickets. Reuse existing Write/vault scope; do not duplicate the DEV flow. **Update the IDENTITY "Active in: OPUS pipeline (feature) only" + "Never active in" + PIPELINE POSITION enumeration to include CORRECTIO (D27).**
  docs/agents/probator.md: D6,D6b,D7b,D8 — add a BUG (CORRECTIO) close mode: verify repro pre-fix (must reproduce) + post-fix (must not), evidenced in the handover; tests; conditional regression test (D6b trigger); write the close + the routine knowledge entry to the project-knowledge sink (D8); may raise `decision: yes` at close. Keep read-only build/test Bash + handover-only Write. Keep the **intercessio veto → praetor-revision → re-verify** loop available in the bug flow (D26). **Update the IDENTITY "Active in: OPUS pipeline only" + "Never active in" + PIPELINE POSITION enumeration to include CORRECTIO (D27).**
  docs/agents/senate.md: D7,D7b — Censura BUG mode is CONDITIONAL, decision-triggered (runs only on a confirmed `decision: yes` to expand the repo project-knowledge sink — NOT a quality gate for bugs). State the decision definition ("a choice a future ticket's agent would behave differently knowing"). Do not add a standing bug review gate. **Update the PIPELINE enumeration to include CORRECTIO (Censura conditional) (D27).**
  docs/skills/debugging-tribunus-input.md: D11,D12 — resolve the SAW-33/D15 "BUG handover-chain roles owner-deferred": Tribunus standalone-debug is now the CORRECTIO escalation investigator (entry=wild & cause not localizable), producing a structured fix-spec (repro · root-cause file:symbol · proposed change · blast radius); if the cause is not localizable to a file/subsystem → the owner files a normal EXPLORACIO **spike ticket** (no in-CORRECTIO quaestor mode — D12). Update the "roles deferred" note to point at bug-pipeline.md.
  docs/agents/session-starters.md: D22,D25 — add a CORRECTIO launch entry (paste prompt: load docs/skills/bug-pipeline.md, Praetor as bug executor, ticket URL, project path) + tab-name convention; note the owner moves the Notion ticket through stages and launches each hop (owner-launched, handover-driven). Keep existing entries intact.
  docs/agents/tribunus.md: D11,D12,D27 — the IDENTITY "Active in: OPUS pipeline only" / "Never active in: EXPLORACIO…" contradicts both the existing standalone-debug mode AND the new CORRECTIO role. Acknowledge: Tribunus is the CORRECTIO escalation **investigator** (standalone-debug, via debugging-tribunus-input.md) and the **HIGH/critical-surface code-review re-entry** (D11). Update Active-in / PIPELINE POSITION accordingly; keep the intercessio veto semantics.
  docs/agents/curator.md: D11,D27 — the IDENTITY "Active in: OPUS pipeline only" contradicts the CORRECTIO conditional re-entry. Acknowledge: Curator enters CORRECTIO **only** on `severity: HIGH` or when the fix touches deploy/config/runtime (D11). Update Active-in / PIPELINE POSITION; keep verdict-only (no veto).

OUT OF SCOPE (do not do):
  - Edit `docs/agents/quaestor.md` — UNCHANGED per D12 (the escalation is a normal EXPLORACIO spike ticket, not a quaestor mode).
  - Touch Foodoire or any consuming project; edit its templates (`handover_template.md` "BUG: TBD", `bug_output_template.md`); create `correctio_outputs/`. These are project-owned, flagged downstream (PoC "Open / descoped").
  - Pin model/effort tiers (D10 descoped — note the dimension only).
  - Create or renumber Notion tickets; change ticket properties.
  - Commit or push.
  - Modify the MAIN folder-note (v1.5.md) or sibling sub-docs — master-only.

REPORTING:
  - Report at the end of each PASS (files touched, anything ambiguous).
  - Fill ONLY this sub-md's "## Changes Made" section. Flag any out-of-scope discovery for the master; do not act on it.

## Changes Made

Executed in 2 passes, 9 files (8 edited + 1 new). PoC SAW-29 D1–D27 applied; existing skill/agent forms preserved.

### PASS 1 — Foundations

**docs/skills/bug-pipeline.md** (NEW — the CORRECTIO flow-doc)
Created following the existing skill convention: frontmatter (`name`/`description`) → numbered LOAD ORDER (AGENT_LAWS → CLAUDE → ticket + local handover/output → this file → active stage skill → veto/revision skills in that path only) → explicit phase boundaries → NEVER/CONSTRAINTS citing Laws. Content: the two routing axes (`entry: wild|dev-linked` + `severity: HIGH/MED/LOW`, both hub-resident, D9); the DEFAULT 2-session flow (D2); investigate-first → HITL cause-note gate (canonical phase boundary, modelled on Consilium's owner-closes-discussion gate) → fix (D3, D4); Probator close = repro pre/post evidence + tests + conditional regression test (required unless owner tags `no-repro-harness`, D6b) + routine knowledge entry to the abstract project-knowledge sink (D8); `decision: yes` → conditional decision-triggered Censura, not a quality gate (D7, D7b); escalation triggers (D11); investigator selection (Tribunus standalone-debug default; non-localizable → owner files EXPLORACIO spike, no in-CORRECTIO quaestor mode, D12); the REUSED veto/revision path (collegium-veto + praetor-revision, D26); edge/terminal states (D16, D15); doc layout `dev_logs/correctio_outputs/<FDP-N>_<Title>/` (D18, D19); model/effort noted as owner-set runtime dimension, no tiers pinned (D10). Notion read-only for agents, owner-launched hops (D20, D23).

**docs/skills/git-workflow.md** (D13)
BRANCH NAMING: added `fix/<TICKET-ID>-slug` as the CORRECTIO sibling of `feature/<TICKET-ID>-slug`, same deterministic derivation; added "one bug = one branch, no batching (batching only via explicit owner tag)". OPEN + ATTACH and EXISTING-BRANCH DETECTION: added the `fix/` prefix variant (open after the HITL gate; detect with `git branch --list 'fix/<TICKET-ID>-*'`). Mechanics only — all policy references (owner-only commit, merge gate) left intact.

### PASS 2 — Agent mandates + launch + escalation

**docs/agents/praetor.md** (D3, D4, D13, D18, D27)
IDENTITY: role now "execution agent (OPUS) and bug executor (CORRECTIO)"; Active-in updated to OPUS + CORRECTIO. PIPELINE POSITION: added the CORRECTIO chain line + CORRECTIO revision re-entry (Probator intercessio). BRANCH: noted `fix/` branch opens only AFTER the HITL cause-note gate. New BUG (CORRECTIO) MODE section: investigate-first (create BUG hub w/ uncommented BUG identity block + bug_output from template + handover) → HITL cause-note gate (STOP, owner sign-off, may raise `decision: yes`) → fix on `fix/<TICKET-ID>-slug`; reuse existing Write/vault scope; never fix pre-existing bug inline (D15). STAGE SKILLS: added bug-pipeline.md pointer + Probator-intercessio note on praetor-revision.

**docs/agents/probator.md** (D6, D6b, D7b, D8, D27)
IDENTITY + PIPELINE POSITION updated to include CORRECTIO (verify + close). INTERCESSIO: noted the same veto mechanic applies in CORRECTIO (D26). New BUG (CORRECTIO) CLOSE MODE section: repro pre/post evidence, tests cited per path, conditional regression test (owner-set trigger, D6b), routine knowledge-sink entry (D8), `decision: yes` raise (D7b). ALLOWED TOOLS + NEVER: extended Write minimally to allow the append-only routine knowledge entry to the project-knowledge sink at CORRECTIO close (mirrors Senate's LESSONS.md write) — see reconciliation note below.

**docs/agents/senate.md** (D7, D7b, D27)
IDENTITY: noted Censura in CORRECTIO is conditional/decision-triggered. CENSURA mode: added a "CENSURA in CORRECTIO" block — runs ONLY on confirmed `decision: yes`, knowledge-base expansion only, not a quality gate; decision definition stated; routine lessons explicitly excluded (Probator writes those). PIPELINE: added the CORRECTIO line (Censura conditional, no Consilium in default bug flow). No standing bug review gate added.

**docs/skills/debugging-tribunus-input.md** (D11, D12)
Replaced the "BUG handover-chain roles owner-deferred (D15)" note with a CORRECTIO ESCALATION INVESTIGATOR block: this standalone-debug mode IS the investigator (before Praetor when entry=wild & cause not localizable), producing a structured fix-spec (repro · root-cause file:symbol · proposed change · blast radius); non-localizable → owner files EXPLORACIO spike; no in-CORRECTIO quaestor mode. OUTPUT: in CORRECTIO investigator mode the fix-spec is recorded in the handover for the owner-launched Praetor session. Points at bug-pipeline.md.

**docs/agents/session-starters.md** (D22, D25)
Added a CORRECTIO — BUG FLOW section (owner-launched, handover-driven): two paste prompts (Praetor bug executor / Probator verify+close, both loading bug-pipeline.md), escalation-hop pointers, Warp tab-name convention `<TICKET-ID> — [Agent] (CORRECTIO)`, and a Praetor pre-step noting the `fix/` branch opens only after the HITL gate. Existing entries (SPQR v1.1 starter, Debugging Tribunus standalone, Personas) left intact.

**docs/agents/tribunus.md** (D11, D12, D27)
IDENTITY: role adds "standalone-debug investigator"; Active-in now OPUS + CORRECTIO (two conditional roles) + standalone debugging — resolves the prior "OPUS only" contradiction. New CORRECTIO ROLES block: (1) escalation investigator via debugging-tribunus-input.md, (2) HIGH/critical-surface code-review re-entry, same intercessio veto semantics. PIPELINE POSITION: added the CORRECTIO chain. STAGE SKILLS: added the CORRECTIO investigator preload line.

**docs/agents/curator.md** (D11, D27)
IDENTITY: Active-in now "OPUS + CORRECTIO only conditionally". New CORRECTIO RE-ENTRY block: enters ONLY on severity=HIGH OR fix touches deploy/config/runtime; cut from the default; verdict-only (no veto), unchanged. PIPELINE POSITION: added the CORRECTIO chain with the conditional Curator insert.

### Verification — OUT OF SCOPE respected

- `docs/agents/quaestor.md` — UNCHANGED (verified via `git diff --quiet`). No in-CORRECTIO quaestor mode introduced; escalation routes out to a normal EXPLORACIO spike ticket (D12).
- Foodoire / consuming-project files — NOT touched. The three templates (`bug_output_template.md`, `ticket_hub_template.md`, `handover_template.md`) were Read as FORM reference only; no writes. `handover_template.md` "BUG: TBD" string + `bug_output_template.md` alignment + `correctio_outputs/` folder remain the flagged downstream Foodoire-owned action.
- Severity vocabulary `HIGH/MED/LOW` only — grep for `sev[123]` returns only the explicit prohibition line in bug-pipeline.md.
- Model/effort tiers NOT pinned — D10 noted as an owner runtime dimension only.
- Veto/revision: REUSED `collegium-veto.md` + `praetor-revision.md` (read, not edited); no new mechanic.
- MAIN folder-note `v1.5.md` and sibling sub-docs — NOT edited by this agent (any uncommitted change there predates this session — master-owned run-container setup).
- No git commit / push run. No Notion tickets created or modified.

### Flags for the master (out-of-scope / reconciliation — not acted on)

1. **Probator Write-scope reconciliation (brief vs PoC).** The brief says "keep handover-only Write" yet also tasks Probator with "write the routine knowledge entry to the project-knowledge sink" (D8). These conflict. Per "PoC wins on conflict," I extended Probator's Write minimally to an **append-only** entry to the project-knowledge sink (LESSONS.md → Warehouse) at CORRECTIO close only — mirroring Senate's existing LESSONS.md write. No code/source/output-doc write added. Flagging for the master to confirm this is the intended resolution (vs. having Probator only record the lesson in its handover for a later writer).
2. **D24 validation pending** — dry-run-mapping the 5 existing FDP bugs onto CORRECTIO is an acceptance test for after G4 lands (per PoC "Open/descoped"); not part of this generic-side execution.
3. **Foodoire downstream action still open** — the project-owned template/folder edits remain a candidate owner-run SAW against Foodoire (PoC "Open/descoped").
