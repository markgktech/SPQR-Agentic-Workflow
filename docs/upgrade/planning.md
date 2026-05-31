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

NOTION UPGRADE DOC
Before execution starts, the master creates:
- one main page for the upgrade (title, overview, implementation groups)
- one sub-page per execution group (brief + Changes Made section)
The execution agent fills in Changes Made. The master fills in everything else.
Creating sub-pages is part of planning, not documentation of a completed plan — naming groups and scopes surfaces dependencies and ordering issues. If you cannot name a group cleanly, the grouping is wrong.

BRIEF FORMAT
Every brief uses typed format:

GROUP: [name]
ORDER: N/N
REPO: Foodoire | SPQR | Both
NOTION_REF: [URL of this group's sub-page]
RATIONALE: [one line — why this is one group]
FILL_CHANGES_MADE: yes
PRE_FLIGHT:
  [skill file or Notion URL the execution agent must load]
  [skill file or Notion URL the execution agent must load]
FILES:
  [filename]: [what changes — one line]
  [filename]: [what changes — one line]

Brief must be complete enough that the execution agent can start without clarifying questions. If writing the brief surfaces ambiguity, resolve it before handing off — ambiguity found during planning is far cheaper than ambiguity found mid-execution.

BRIEF LENGTH
A brief should be writable in under 10 minutes. If it takes longer, the group is too large or too ambiguous. Split along file ownership boundaries or resolve the ambiguity first.

NEVER
- Split file ownership across groups
- Brief execution agent without PRE_FLIGHT refs
- Start briefing before grouping decisions are finalised
- Move to execution before Notion sub-pages are created
- Split groups by effort or time instead of file ownership boundaries
