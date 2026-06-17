## Metadata
**Ticket:** https://www.notion.so/Git-Branching-Strategy-adopt-PoC-into-SPQR-process-agent-mandates-37e68d5de1e881b49f5bde30b552565a?v=37268d5de1e88125adb5000ce8e8fa12&source=copy_link
**Epic:** 
**Component:** 
**Document status:** ADOPTED — refined & integrated via SAW-32 (run: v1.5, see [[02-git-branching-strategy]])
**Date:** 2026-06-13
**Session ID:** 938f2e2c-6256-4f5e-8112-6d01e6beb803
**Usage:** 15.3k input, 74.2k output, 3.4m cache read, 198.7k cache write ($5.61)
**Session scope:** Git branching, commit & merge strategy for Foodoire (and, where relevant, the companion warehouse) — solo now, scaling to parallel agents / team later.
**Purpose:** Propose a PoC branching/commit/merge approach and an agent role-division for the SPQR OPUS pipeline. These are well-prepared proposals ("how the meal *could* be cooked"), not fixed decisions — an SPQR developer agent will pick them up, refine with its own decisions, and validate them.
**Status legend:**

# Adoption (SAW-32, run v1.5)
Adopted and refined into the SPQR process via SAW-32. Decisions recorded in [[02-git-branching-strategy]] (D1–D14). Divergences from this proposal:
- **D5/L2** — `commit_authority` is expressed as a config value (`commit_authority: owner`), not the PoC's time-bounded "~6 months" phrasing (an agent cannot measure time).
- **D9/L1** — mechanics vs policy split: the new `docs/skills/git-workflow.md` carries git **mechanics** only; the owner-only-commit / merge **policy** stays in `senate.md` + `CLAUDE.md.template` and is referenced, not duplicated.
- **D6** — the Censor commit message lands as a `commit_message` field in Censura's existing Notion handoff (`censura-output.md`); Censura authors text only and never commits.
- **D14/G4** — the skill states explicitly that an uncommitted feature branch carries no protection until its first commit (seam honesty).
- **Descoped:** Foodoire `CLAUDE.md ## Branching` replacement → post-1.5 owner action (D13). **Open item:** no `censura.md` mandate file → candidate ticket under SAW-25.

# Overview
This PoC explores the ideal git branching, commit, and merge approach for Foodoire and how it should be reflected in the SPQR process and agent behaviour. The trigger is that the original AI-devised, worktree-per-milestone approach was flagged as an antipattern and over-complicated things. **In scope:** the branching model, branch lifecycle, who-does-what (role division), commit/merge gating, and the seams that let it scale later. **Out of scope:** building the mechanics now, push timing, and the parallel-execution machinery — these are noted but deliberately not designed here to avoid premature complexity. The angle of this document is **what changes in the SPQR process and what affects agents**, not a full git tutorial.

# Motivation
The branching process was originally assembled with AI and used **git worktrees to copy the repo** at milestone/ticket granularity (a separate folder per milestone worktree). Two signals showed this was wrong:

- A test engineer flagged "copy the repo via worktree and work tickets into it" as an **antipattern**.
- The worktree created a **separate folder** (the "milestone-0" worktree appeared as its own repo and wouldn't open), which **over-complicated** the work and was abandoned.

If we did nothing: the SPQR git guidance stays **scattered and diverged** (e.g. `session-starters.md` still carries the old hard-coded worktree line while the Branch Strategy note describes a newer model), and scaling to parallel agents or a team would be painful and bias-prone. We want a single coherent approach now, with explicit seams for later growth.

# Findings
- **A branch is not a folder copy.** A plain branch (`git switch`) reuses one working directory — no copy. A **worktree** is a second folder sharing the same `.git`, and is only needed when **two branches must be checked out simultaneously** (i.e. true parallelism). The old worktree felt like an antipattern because it was used for *sequential* work, where a branch suffices.
- **Current state:** Foodoire and SPQR are both `main`-only with no live worktrees. The foundation tickets (DEV-001/002/003) were committed **directly to main** (bundling, reasonable for the "betonalap" phase). The new process being designed here is the deliberate move away from that.
- **GitHub Flow fits; Git Flow is overkill.** GitHub Flow = one long-lived `main` + short-lived feature branch per ticket. Git Flow = heavy multi-branch (`develop`/`release`/`hotfix`) for scheduled releases — unnecessary at this scale. (The near-identical names are a historical accident, not the same thing.)
- **Asymmetric gating is the organizing principle.** Cheap, reversible actions (open a branch) are automated; costly, irreversible actions (commit, merge, delete) are owner-gated.
- **Owner-only commits, no intermediate commits in OPUS.** For the foreseeable future (~6 months, until a master orchestrator) only the owner commits. Tickets are well-sliced; if something breaks badly the ticket is **restarted and the changes discarded** — no commit. The whole pipeline runs on an uncommitted working tree until the end.
- **The Censor produces the final commit message** at green pass: a human-readable title + bullet body at the *deliverable* altitude, synthesized from the ticket trail + diff, describing the final delivered state (not the veto journey).
- **Scaling is a switch, not a rewrite.** The same convention works solo and in a team; parallelism (worktrees) and delegated commits layer on later via policy knobs, with no agent rewrite.

# Breakdown

## Branching model — GitHub Flow
One `main` (always green / releasable) + a short-lived `feature/DEV-XXX-slug` branch per ticket, merged back to `main` when done. Chosen over Git Flow because it is light for a solo dev, yet scales to a team without rework. Dependent tickets run as a **sequential chain** (the next branches from `main` after the previous merges) rather than stacked branches, to avoid complexity now.

## Branch vs worktree — the folder clarification
| | Plain branch (now) | Worktree (later, parallel only) |
|---|---|---|
| Folders on disk | **one** — files morph in place on `git switch` | **two+** — a second folder, same `.git` |
| When | sequential work, single agent at a time | multiple agents/branches checked out at once |
| Status | default | OFF until parallelization (~3 months) |

A commit on a feature branch **never reaches `main` by itself** — `main` only receives anything at merge time. This is the safety property the whole model rests on.

## Lifecycle & role division
| Step | Who | Why |
|---|---|---|
| Scope + base | owner (now implicit: "one ticket, from `main`") | judgement call; trivial now, future Consilium `Branch` property for bundling/parallel |
| Branch **open** (`git switch -c feature/DEV-XXX-slug`, before coding) | Praetor (auto) | cheap + reversible → no gate; name deterministically derived from ticket |
| Existing branch found for the ticket | Praetor: **STOP + ask owner** | never delete or resume on its own; deletion is destructive (HITL) |
| Code + fixes across stages | all agents (Praetor → Tribunus → Probator → Curator → Censura) on the **same branch, one folder, sequentially** | downstream fixes are continued work, not new branches |
| **Commit** | **owner only** (~6 months) | writing history = owner gate |
| Intermediate saves in OPUS | **none** | well-sliced tickets; on failure → restart ticket, discard changes, no commit |
| **Commit message** | **Censor** at green pass (title + human-readable bullets) | deliverable altitude; synthesized from ticket trail + diff; describes final state, not the veto path |
| Branch **close / merge** | **owner** (via GitHub Mac app; terminal only if needed; merge to `main` after push when all good) | irreversible → human gate |
| Release marker | **git tag** (logical milestone), not a branch | cheap, searchable |

## Release / cutover
Not built now. The heavy QA/cutover process is justified only when **(a)** a bad release can't be cheaply rolled back (real users with data) **or (b)** more than one person ships. The seam is `feature → main → tag`; a dedicated `release/x.y` branch is introduced only if/when the "freeze a release while development continues" conflict actually appears.

## Policy knobs (scaling seams, default OFF now)
- **worktree:** off (sequential) → on when parallel agents run.
- **commit_authority:** `owner` → `orchestrator` (~6 months, under rules e.g. green build + clean review).
- **scope:** implicit "one ticket, from `main`" → Consilium-written `Branch` property when bundling/parallel arrives.

# Recommendations
- **Do now:** adopt feature-branch-per-ticket (GitHub Flow); Praetor auto-opens the branch before coding; existing-branch → STOP + ask owner; owner-only commits with **no** intermediate OPUS commits; Censor emits the final bullet commit message at green pass; owner is the merge gate (GitHub Mac app); tag for release milestones.
- **Defer (note, do not design now):** the git-workflow skill (and its scope — mechanics only vs. + merge/tag policy); SPQR cleanup & template sync (`session-starters.md`, `praetor.md`); Foodoire `CLAUDE.md` `## Branching` section (owner action); formalizing scope/base on Consilium; worktrees (until parallel); the intermediate `release/x.y` branch; squash (until a multi-commit-per-ticket style is actually used).
- **Discard:** per-ticket / per-milestone worktree for sequential work; the old "copy the repo via worktree and work tickets into it" approach.

# Descoped
- **Push timing / remote sync** — owner-managed; explicitly not documented here.
- **Metadata fields** (Epic, Component, Document status, Phase, Status legend) — owner fills.
- **Intermediate / checkpoint commits in OPUS** — descoped because the current model is one commit per ticket with restart-on-failure; revisit if rollback granularity becomes a need.
- **Parallel-execution mechanics** (worktree wiring, multi-branch coordination) — descoped to a future phase; only the seam is kept now.

# References
- `.claude/rules/AGENT_LAWS.md` — agent laws (Stay in Character, Anti-Meeseeks, Don't be Dory, Be like Spock).
- `docs/agents/praetor.md` — Praetor identity, allowed tools, sensitive-op / worktree lines (cleanup target).
- `docs/agents/session-starters.md` — still carries the old hard-coded worktree pre-step (cleanup target).
- `docs/specifications/delivery_notes/Sequential_Agentic_Workflow_v1.0_SPQR version/Upgrade — Sequential Agentic Workflow v1.3/5. Branch Strategy.md` — prior `Branch` property model; SPQR template sync still pending.
- Foodoire repo (`/Users/kovacsmark/Documents/RecipeAPP/Foodoire`) — current `main`-only state; DEV-001/002/003 committed directly to main.
