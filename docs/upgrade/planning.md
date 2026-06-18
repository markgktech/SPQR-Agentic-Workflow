GROUPING RULES
Items that touch the same file belong in the same group.
Items with a dependency (B requires A) must be in the same group, or A's group must precede B's.
One group = one execution session; completable without hitting context limits.
If a group is too large, split only along file ownership boundaries — never by effort or time.
Generic repo sync is always after all project-specific groups.

DEPENDENCY RULE
If two groups touch the same file, merge them into one session. Never split file ownership across groups.

EXECUTION ORDER
Order is dependency-driven, not category-driven. General pattern:
1. project-specific repo groups first (real content, testable context)
2. generic repo sync group after (depends on project-specific being done)
3. documentation-only or cross-cutting groups last (when they have no upstream dependency)
If a group has no dependency on anything before it, its position is flexible — place it where it causes least disruption.
NOTE — pending: generic→project propagation redesign. The generic-sync ordering above (and the sync group itself) is unchanged by this rework and under review in a separate session. Do not redesign it here.

RUN CONTAINER
The run's decisions are NOT authored here — they live in the run's PoC (poc/ lane, from poc_template, written in Phase 3). The MAIN folder-note links the PoC (its poc: frontmatter); the group briefs are DERIVED FROM it.
Before execution starts, the master creates the run container at docs/spqr_self/upgrades/<version>/, from templates:
- the MAIN folder-note <version>.md (from templates/run_main_template.md): title, summary, why-now, covered SAW tickets, implementation groups
- one ordered group sub-md per execution group, NN-<slug>.md (from templates/group_submd_template.md): the brief + a "## Changes Made — _(pending execution)_" sentinel
The master pre-creates every group sub-md (with the sentinel) at planning. The execution agent fills in only its own sub-md's Changes Made; the MAIN folder-note is master-write-only.
Creating the sub-md files is part of planning, not documentation of a completed plan — naming groups and scopes surfaces dependencies and ordering issues. If you cannot name a group cleanly, the grouping is wrong.

BRIEF FORMAT
Every brief uses typed format (it lives in the group sub-md's Brief section):

GROUP: [name]
ORDER: N/N
REPO: [YOUR_PROJECT] | SPQR | Both
RUN_CONTAINER: [absolute path to the version folder]
RUN_DOC: [absolute path to this group's sub-md]
RATIONALE: [one line — why this is one group]
SOURCE_OF_TRUTH: [path to the run's PoC — authoritative for decisions/content; derive the brief from it, do not re-decide]
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  [skill file or repo path the execution agent must load]
  [skill file or repo path the execution agent must load]
FILES:
  [filename]: [what changes — one line]
  [filename]: [what changes — one line]

Brief must be complete enough that the execution agent can start without clarifying questions. If writing the brief surfaces ambiguity, resolve it before handing off — ambiguity found during planning is far cheaper than ambiguity found mid-execution.

BRIEF LENGTH
A brief is too large if it requires more than 7 FILES entries or a RATIONALE longer than one line. If either threshold is hit, split along file ownership boundaries or resolve the ambiguity first.

NEVER
- Split file ownership across groups
- Brief execution agent without PRE_FLIGHT refs
- Start briefing before grouping decisions are finalised
- Move to execution before the run-container sub-md files are created (pre-created with the Changes Made sentinel)
- Split groups by effort or time instead of file ownership boundaries
