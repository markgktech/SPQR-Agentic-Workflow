---
name: git-workflow
description: Single source of git mechanics for the SPQR pipeline — GitHub Flow branch lifecycle, naming, open/detect/STOP, merge, tag, and the scaling policy knobs. MECHANICS only; commit/merge policy lives in its mandate homes and is referenced, never duplicated.
---

APPLIES TO: Praetor (branch open + detect), all OPUS agents (work on the assigned branch), owner (commit, merge, tag)
LOAD: on demand — when a ticket opens a branch or reaches merge / release

SCOPE
This file carries git MECHANICS only — branch naming, open, attach, existing-branch detection, merge, tag.
Git POLICY (who may commit, who merges) lives in its mandate homes and is referenced here, never restated:
  owner-only commit: senate.md ("never run shell commands") + CLAUDE.md.template (git commit/push: NEVER)
  owner merge gate: documented below as an owner action — no agent merges
Agents reference this file by name; they never embed git commands. One copy only — divergence is structurally impossible.

BRANCHING MODEL — GitHub Flow
One main, always green / releasable.
One short-lived feature branch per ticket, merged back to main when done.
Dependent tickets run as a sequential chain — the next branch is cut from main after the previous one merges; never stacked.
Git Flow (develop / release / hotfix) is rejected — overkill at this scale.

SEAM HONESTY (framing, not a behaviour rule)
Auto-opening the branch prepares the merge-time seam — nothing more.
Under owner-only final commit, a branch carries NO protection until its first commit; until then it is only a label on main's HEAD.
A commit on a feature branch never reaches main by itself — main receives changes only at merge time.
The agent acts the same either way; this note exists so the skill is not read as "the branch protects the work on its own".

BRANCH NAMING
Derived deterministically from the ticket ID: feature/DEV-XXX-slug
  DEV-XXX — the ticket ID, verbatim
  slug — short kebab-case of the ticket title
No human judgement in the name — the same ticket always yields the same branch name.

OPEN + ATTACH
Praetor auto-opens the branch before coding (cheap + reversible → no gate):
  git switch -c feature/DEV-XXX-slug
Downstream agents (Tribunus → Probator → Curator → Censura) work on the same branch, one folder, sequentially — they attach, they do not branch. Downstream fixes are continued work, not new branches.

EXISTING-BRANCH DETECTION + STOP
Before opening, detect:
  git branch --list 'feature/DEV-XXX-*'
If a branch already exists for the ticket → STOP and ask owner.
Never delete, reset, or resume it autonomously — branch deletion is destructive (HITL / owner decision).

COMMIT AUTHORITY
commit_authority: owner
The owner is the only committer — a value an agent reads now, not a time-bounded rule. Policy home is senate.md + CLAUDE.md.template; referenced here, not duplicated.
No intermediate / checkpoint commits inside an OPUS run — the pipeline runs on an uncommitted working tree to the end.
On failure → restart the ticket, discard the changes, no commit. Tickets are sliced small enough that restart is cheap.

COMMIT MESSAGE
Censura emits the final commit message at green pass (see censura-output.md commit_message): title + human-readable bullets at deliverable altitude, synthesized from the ticket trail + diff.
Owner copies it into the commit. No agent runs the commit.

MERGE GATE
Owner merges feature → main when all is green (irreversible → human gate).
No agent merges; agents never run merge commands.

RELEASE MARKER
A release milestone is a git tag on main (logical, searchable), not a branch.
A dedicated release/x.y branch is introduced only if a "freeze a release while development continues" need actually appears — not now.

POLICY KNOBS (scaling seams — default OFF; no reader consumes these today)
worktree:         off (sequential, one folder) → on when parallel agents run. A worktree is a second folder sharing one .git, needed only when two branches must be checked out at once.
commit_authority: owner → orchestrator, under explicit rules (e.g. green build + clean review) when a master orchestrator exists.
scope:            implicit "one ticket, from main" → a Consilium-written Branch property when bundling / parallel work arrives.
Documented seams only — no agent reads them today. Listed so scaling is a switch, not a rewrite.

NEVER
Never embed git commands in an agent mandate — reference this file by name; one copy only.
Never let an agent commit, merge, or tag — those are owner actions.
Never make an intermediate commit inside an OPUS run — restart and discard on failure.
Never delete, reset, or resume an existing ticket branch autonomously — STOP and ask owner.
Never stack dependent ticket branches — chain them sequentially from main.
Never treat an uncommitted feature branch as protecting the work — it is a label on main's HEAD until its first commit.
