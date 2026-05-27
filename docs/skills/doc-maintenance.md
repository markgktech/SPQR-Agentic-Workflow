APPLIES TO: Consilium, Praetor, Tribunus, Senate Censura
LOAD: on demand — only when a ticket explicitly touches documentation

FILE SCOPE
Six protected files. No agent writes directly to any of them.

CLAUDE.md — always loaded every session; ~80 lines hard ceiling 200
  scope: stack, critical rules, coding principia, phase boundaries, navigation, agent workflow, doc refs
  not: patterns, code examples, entity detail — those belong in CONVENTIONS.md / DATA_MODEL.md

AGENT_LAWS.md (.claude/rules/) — always auto-loaded; ~20 lines hard ceiling 40
  scope: 4 Laws — behavioral constraints, every agent every session; no project-specific content
  not: project-specific rules — those belong in CLAUDE.md or skill files

CONVENTIONS.md — on demand; no ceiling
  scope: all coding patterns: naming, folder structure, architecture patterns, services, DI, error patterns
  not: schema detail, architecture overview, decision rationale

DATA_MODEL.md — on demand; no ceiling
  scope: schema reference — entity tree, @Model definitions, JSON structs, constants, image storage, schema versioning, business invariants; code blocks stay — they are the documentation
  not: architecture, patterns, decisions

ARCHITECTURE.md — on demand; ~15 lines hard ceiling 30
  scope: system topology map + architectural invariants not covered elsewhere; ~15 lines unique content only
  not: patterns (CONVENTIONS.md), decisions (docs/decisions/), schema detail (DATA_MODEL.md)

docs/decisions/ — on demand; INDEX.md ~25 lines; ADR files 10–20 lines each
  scope: one architectural decision per file (A1–Ax); INDEX.md is entry point — load individual files by ID when relevant
  not: trivial decisions, field notes, UI micro-decisions, deferred items without rationale

FORMAT RULES
All six files must maintain:
  No --- decorative separators
  No **bold** on section headers
  No decorative empty lines between sections
  Code blocks stay — they are content, not decoration
  Pointers over copies: CLAUDE.md references CONVENTIONS.md and DATA_MODEL.md, never duplicates them
  Every new section must fit the file's canonical scope — cross-scope content goes in the correct file

AGENT BEHAVIOR
Never write directly to any protected file.
If a doc change is needed: output an exact, copy-paste ready flag — vague flags are invalid.
Flag mid-pipeline; execute only after Senate Censura closes the ticket and owner reviews proposed text.
The flag captures the decision immediately — only the file write is deferred until code is stable.

FLAG FORMATS
For file updates (CLAUDE.md, CONVENTIONS.md, DATA_MODEL.md, ARCHITECTURE.md, AGENT_LAWS.md):
  ⚠️ [FILE] UPDATE NEEDED
  What changed: [one sentence]
  Why: [one sentence — the non-obvious reason]
  Suggested addition: [exact text, copy-paste ready — not optional]

For new ADR entries (docs/decisions/):
  ⚠️ ADR NEEDED
  Title: [decision title]
  Suggested file: docs/decisions/aXX-[slug].md
  Suggested content: [full file content — copy-paste ready, 10–20 lines]

EXECUTION ORDER (owner executes after ticket closes)
1. docs/decisions/ → new ADR file(s) + one line added to INDEX.md
2. DATA_MODEL.md → no dependency on other files, update independently
3. ARCHITECTURE.md → no dependency on other files, update independently
4. CONVENTIONS.md → after DATA_MODEL (may reference schema concepts)
5. CLAUDE.md → always last — references CONVENTIONS.md and DATA_MODEL.md

PIPELINE ROLES
Consilium — loads when session involves architecture or new decisions; primary proposer of ARCHITECTURE.md changes and new ADRs
Praetor — loads when ticket touches any doc file or when writing any ⚠️ flag; proposes ⚠️ ADR NEEDED if implementation reveals undocumented architectural decision
Tribunus — loads when reviewing output with ⚠️ flags; flag without Suggested addition/content = HIGH finding
Senate Censura — loads every ticket close; collects all ⚠️ flags, validates format, confirms owner reviewed proposed text before closing
Probator — never loads; doc changes are not testable
Curator — never loads content; scans ticket comments for ⚠️ prefix only — does not validate flag content

CONSTRAINTS
Never write directly to CLAUDE.md, CONVENTIONS.md, DATA_MODEL.md, ARCHITECTURE.md, AGENT_LAWS.md, or any file in docs/decisions/
Never output a flag without Suggested addition or Suggested content — "something about X should be added" is invalid
Never add content to a file outside its canonical scope — wrong-file placement is a bug, not a shortcut
Never restore decorative formatting: ---, **Section Header**, empty spacing lines
Never duplicate content that belongs in another file
Never execute a doc update mid-pipeline — file write waits for ticket close and owner review
Never create an ADR for a trivial decision (field notes, UI micro-decisions, deferred items without rationale)
