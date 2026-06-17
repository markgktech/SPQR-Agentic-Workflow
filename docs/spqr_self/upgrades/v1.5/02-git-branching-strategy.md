---
up: "[[v1.5]]"
group: "Git workflow single-source + session wiring"
order: 2/2
saw: [SAW-32]
poc: ["[[Git Branching Strategy — PoC]]"]
tags: [group]
---

# Group 2 — Git workflow single-source + session wiring

> Independent workstream folded into v1.5 (no dependency on Group 1 — propagation). Covers SAW-32: adopt the Git Branching Strategy PoC into the SPQR process and agent mandates.

## Decisions
<!-- #decision — Phase 3, SAW-32. Recorded in real time. -->

**Core problem (the spine).** Git guidance in SPQR is duplicated across agent/process files and has diverged into mutually contradictory versions (worktree in `praetor.md` + `session-starters.md`, GitHub Flow in the PoC). A stateless agent follows whichever stale file lands in its context. The fix is structural, not a model choice.

- **D1 · I8 (spine) — single source.** Git **mechanics** live in one new named file `docs/skills/git-workflow.md`; agents reference it by name, never embed commands. Divergence becomes structurally impossible (one copy). *Affected:* new `docs/skills/git-workflow.md`; `praetor.md`, `session-starters.md` (reference it).
- **D2 · I1 — branching model.** GitHub Flow: one `main` (always green) + short-lived `feature/DEV-XXX-slug` per ticket; dependent tickets as a sequential chain (next branches from `main` after the previous merges). Git Flow rejected (overkill at this scale). *Affected:* `git-workflow.md`.
- **D3 · I2 + I10 — Praetor auto-open + agnostic isolation.** Praetor auto-opens the branch before coding (cheap/reversible → no gate), name derived deterministically from the ticket ID. Praetor `Isolation` becomes **mechanism-agnostic** ("within the assigned branch / working directory") — worktree is an optional switch, not identity. *Affected:* `praetor.md`.
- **D4 · I3 — existing-branch stop rule.** If a branch already exists for the ticket → Praetor **STOP + ask owner** (never delete/resume on its own — deletion is destructive, HITL). Deterministic detection: `git branch --list 'feature/DEV-XXX-*'`. *Affected:* `git-workflow.md` (mechanic), `praetor.md` (the stop behaviour).
- **D5 · I4 — commit authority as config, not time.** Expressed as `commit_authority: owner` (a value an agent reads now), **not** "for ~6 months" (a time-based rule an agent cannot measure — L2). No intermediate OPUS commits; on failure → restart ticket, discard, no commit. The **no-commit guarantee already exists** (senate.md "never run shell commands" + `CLAUDE.md.template` "git commit/push: NEVER") — `git-workflow.md` references it, does **not** duplicate it. *Affected:* `git-workflow.md`.
- **D6 · I5 — Censura commit message.** Add a `commit_message` field to Censura's GREEN handoff block in `censura-output.md` (title + human-readable bullets, deliverable altitude, synthesized from ticket trail + diff). Handoff channel = Censura's existing Notion ticket comment; owner copies it into the commit. This is text output only — does not violate the no-shell-command rule (Censura never commits). *Affected:* `censura-output.md`.
- **D7 · I6 — merge gate.** Owner is the merge gate (irreversible → human gate). Documented in `git-workflow.md` as an owner action; agents do not merge. *Affected:* `git-workflow.md`.
- **D8 · I7 — release marker.** Release milestone = `git tag` (logical, searchable), not a branch. *Affected:* `git-workflow.md`.
- **D9 · I8 (L1) — mechanics vs policy split.** `git-workflow.md` carries **mechanics** (branch naming, open/attach/teardown, merge/tag commands, detection). **Policy** (who gates: owner-only commit, owner merge) stays in the agent mandates / `CLAUDE.md.template` / `senate.md` and is **referenced**, not duplicated. *Affected:* `git-workflow.md` (references policy homes).
- **D10 · I11 (L3) — policy knobs.** `worktree` / `commit_authority` / `scope` documented as a **named config block** in `git-workflow.md`, default-OFF, with an explicit note: *no reader consumes these today — deferred scaling seams.* *Affected:* `git-workflow.md`.
- **D11 · I9 — weed session-starters.** Remove the stale `git worktree add ../TICKET-XXX-branch` line; replace with the branch-driven setup referencing `git-workflow.md`. *Affected:* `session-starters.md`.
- **D14 · G4 — seam honesty.** `git-workflow.md` states explicitly that auto-open prepares the merge-time seam; under owner-only-final-commit a branch carries **no protection until its first commit** — until then it is a label on `main`'s HEAD. Framing note, not a behaviour rule (the agent acts the same either way). Prevents the skill implying the branch protects on its own. *Affected:* `git-workflow.md`.

**Cleanup surface (bounded by grep).** Stale git references in the generic repo exist ONLY in `praetor.md` (lines 24/28/34/43) and `session-starters.md` (line 17). `CLAUDE.md.template:20` is the canonical owner-only-commit policy — KEEP, do not touch.

**Master-handled / out of this execution group:**
- **D12 · I13** — PoC marked adopted/refined + ticket Target path-drift (`docs/specifications/poc/…` → `docs/spqr_self/poc/…`) reconciled → **wrap-up master action** (not an execution file edit).
- **D13 · I12** — Foodoire `CLAUDE.md` `## Branching` is the OLD worktree/milestone model and must be **replaced** (not merely added). **DESCOPED to a post-1.5 owner action** (owner decision: no active Foodoire development now).

**Open item (flag only — owner creates ticket):**
- Censura has skill files but **no `docs/agents/censura.md` mandate file** — latent process-debt, independent of git (Censura has no git authority). NOT blocking SAW-32. Candidate ticket under the SAW-25 (Operations / process-debt) epic — owner decides at wrap-up.

## Brief

GROUP: Git workflow single-source + session wiring
ORDER: 2/2
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/02-git-branching-strategy.md
RATIONALE: one cohesive git lifecycle — author the single source, wire the sessions to it, weed the old copies; no shared-file conflicts across the four files
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  docs/spqr_self/poc/Git Branching Strategy — PoC.md   (the design — authoritative for CONTENT)
  docs/spqr_self/upgrades/v1.5/02-git-branching-strategy.md   (this file — Decisions D1–D13 are binding)
  docs/upgrade/execution.md
  docs/agents/praetor.md , docs/agents/session-starters.md   (cleanup targets — current stale state)
  docs/skills/censura-output.md   (GREEN handoff block — where commit_message is added)
  docs/skills/   (FORM exemplar — match existing skill-file shape: frontmatter + section style)
  CLAUDE.md.template , docs/agents/senate.md   (the no-commit POLICY homes — reference, do not duplicate)
CONVENTIONS (mandatory — match existing form, do not invent a new shape):
  - git-workflow.md → mirror the existing `docs/skills/*.md` form (frontmatter `name`/`description`, terse imperative sections, NEVER list). It is a MECHANICS reference, not a tutorial.
  - praetor.md / session-starters.md → preserve their existing structure; only swap the worktree mechanic for a named reference to git-workflow.md and make isolation mechanism-agnostic.
  - The PoC is authoritative for CONTENT; the Decisions block above (D1–D13) overrides the PoC where they differ (PoC is a proposal). Existing skill/agent files are authoritative for FORM.
FILES:
  docs/skills/git-workflow.md: CREATE — the single source of git mechanics. Sections: branching model (GitHub Flow, feature/DEV-XXX-slug, sequential chain) + seam-honesty note (auto-open prepares the merge-time seam; a branch carries no protection until its first commit — D14) / branch naming derived from ticket ID / open + attach + existing-branch detection (`git branch --list 'feature/DEV-XXX-*'`) + STOP-on-existing rule / commit_authority config block (owner; references no-commit policy in senate.md + CLAUDE.md.template, no duplication) / no-intermediate-commit + restart-on-failure / merge gate (owner) / release tag / policy-knobs named block (worktree, commit_authority, scope — default-OFF, "no reader today"). MECHANICS only; policy referenced (D9).
  docs/agents/praetor.md: EDIT — make Isolation mechanism-agnostic ("within the assigned branch/working directory"); add auto-open-branch step (deterministic name from ticket ID, before coding); add existing-branch → STOP + ask owner; replace the four worktree lines (24/28/34/43) with a named reference to git-workflow.md. Worktree becomes an optional switch, not identity.
  docs/agents/session-starters.md: EDIT — remove the stale `git worktree add ../TICKET-XXX-branch` line (17); replace with the branch-driven setup pointing to git-workflow.md.
  docs/skills/censura-output.md: EDIT — add a `commit_message` field to the GREEN handoff OUTPUT FORMAT block (title + human-readable bullets at deliverable altitude, from ticket trail + diff). Text output only; Censura never commits.

OUT OF SCOPE (do not do): any Foodoire / consuming-project file (CLAUDE.md ## Branching is a post-1.5 owner action — D13); creating a `censura.md` mandate file (open item, not this ticket); building executable/deterministic git tooling (markdown definitions only); touching `CLAUDE.md.template:20` (canonical policy — keep); marking the PoC adopted or editing the SAW-32 Target field (wrap-up master action — D12); any git commit/push.

## Changes Made

### 1. `docs/skills/git-workflow.md` — CREATE (the single source)
New skill file, the one home for git **mechanics**. Form mirrors existing `docs/skills/*.md` (frontmatter `name`/`description`, terse UPPERCASE sections, NEVER list). Sections authored:
- **SCOPE** — declares mechanics-only; names the policy homes (`senate.md`, `CLAUDE.md.template`) for owner-only commit and the owner merge gate, **referenced not duplicated** (D9). States agents reference by name, never embed commands → divergence structurally impossible (D1).
- **BRANCHING MODEL — GitHub Flow** — one green `main` + short-lived `feature/DEV-XXX-slug` per ticket; dependent tickets as a **sequential chain** from `main`, not stacked; Git Flow rejected (D2).
- **SEAM HONESTY** — auto-open prepares the merge-time seam; a branch carries no protection until its first commit — until then a label on `main`'s HEAD; framing note, agent acts the same either way (D14).
- **BRANCH NAMING** — deterministic from ticket ID, `feature/DEV-XXX-slug` (D2/D3).
- **OPEN + ATTACH** — Praetor auto-opens before coding (`git switch -c …`); downstream agents attach to the same branch/folder sequentially (D3).
- **EXISTING-BRANCH DETECTION + STOP** — `git branch --list 'feature/DEV-XXX-*'`; if found → STOP + ask owner, never delete/reset/resume (D4).
- **COMMIT AUTHORITY** — `commit_authority: owner` as a config value an agent reads now, **not** a time-based "~6 months" rule (D5); references the no-commit policy home, no duplication; no intermediate commits; restart-and-discard on failure.
- **COMMIT MESSAGE** — points to `censura-output.md` `commit_message`; owner copies; no agent commits (D6).
- **MERGE GATE** — owner merges `feature → main`; no agent merges (D7).
- **RELEASE MARKER** — `git tag` on `main`, not a branch; `release/x.y` only if a real freeze-need appears (D8).
- **POLICY KNOBS** — named block `worktree` / `commit_authority` / `scope`, default-OFF, explicit "no agent reads these today" note; expressed as state transitions, no time anchors (D10).
- **NEVER list** — embed git in a mandate; agent commit/merge/tag; intermediate commit; autonomous branch delete/reset/resume; stack dependent branches; treat an uncommitted branch as protection.

### 2. `docs/agents/praetor.md` — EDIT
Structure preserved; targeted swaps only:
- Added a **BRANCH** section (after STAGE SKILLS): auto-open the ticket branch before coding, deterministic name from ticket ID, mechanics deferred to `git-workflow.md`; existing branch → STOP + ask owner (D3/D4).
- Line 24 `Edit, Write (source files within worktree only)` → `… within the assigned branch / working directory`.
- Line 28 `Isolation: worktree — never write outside worktree` → mechanism-agnostic: "work within the assigned branch / working directory … a worktree is an optional switch, not the isolation identity"; references `git-workflow.md` (D3).
- Line 34 `- File delete outside worktree` → `… outside the assigned working directory`.
- Line 43 `Never modify files outside the worktree` → `… outside the assigned branch / working directory`.
- Added one NEVER line: "Never delete, reset, or resume an existing ticket branch autonomously — STOP and ask owner" (reinforces D4 in existing form).

### 3. `docs/agents/session-starters.md` — EDIT
- Line 17 stale `git worktree add ../TICKET-XXX-branch TICKET-XXX-branch` removed; PRAETOR PRE-STEP replaced with branch-driven setup ("ensure repo on `main` and clean; Praetor auto-opens `feature/DEV-XXX-slug`; existing branch → stop and ask") pointing to `git-workflow.md` (D11). Rest of the template untouched.

### 4. `docs/skills/censura-output.md` — EDIT
- Added `commit_message` field to the GREEN handoff OUTPUT FORMAT block (after `addressed`): one-line title + human-readable bullets at deliverable altitude, from ticket trail + diff, GREEN-only, empty on YELLOW/RED; explicit "text output only — Censura never commits" (D6).
- Added one NEVER line: "Never omit commit_message on GREEN — owner copies it into the commit." Handoff channel (the existing Notion ticket comment) unchanged.

### Verification — OUT OF SCOPE respected
- **MAIN folder-note `v1.5.md` & sibling sub-docs:** not touched. (`v1.5.md`'s `M` status in `git status` is pre-existing from before this session, not from this run.)
- **Foodoire / consuming-project files** (incl. `CLAUDE.md ## Branching` — D13 post-1.5 owner action): not touched.
- **`censura.md` mandate file:** not created (open item, owner decides at wrap-up).
- **`CLAUDE.md.template:20`** (canonical owner-only-commit policy): not touched — only **referenced** as a policy home in `git-workflow.md`.
- **PoC adoption / SAW-32 Target field** (D12 wrap-up master action): not touched.
- **git commit / push:** none run — owner commits.
- **Grep check:** only `worktree` mention remaining in the two cleanup targets is the intentional optional-switch framing in `praetor.md:32`; all four stale worktree lines (24/28/34/43) converted; `git-workflow.md` referenced by name from `praetor.md`, `session-starters.md`, and (via `commit_message`) `censura-output.md`.
