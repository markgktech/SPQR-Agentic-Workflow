APPLIES TO: Consilium, Praetor, Tribunus, Senate Censura
LOAD: on demand — only when a ticket explicitly touches documentation

SCOPE OF THIS SKILL
Knowledge — prior decisions, constraints, conventions, schema, architecture, lessons —
lives in the warehouse, the sole knowledge authority (post-SAW-31 cutover). New knowledge
is authored as a proposal via docs/skills/warehouse-ingest.md, never written to a flat doc.
This skill governs only the two protected flat files that are NOT warehouse knowledge.

FILE SCOPE
Two protected files. No agent writes directly to either.

CLAUDE.md — always loaded every session; ~80 lines hard ceiling 200
  scope: stack, critical rules, coding principia, phase boundaries, navigation, agent workflow, warehouse pointer
  not: patterns, schema, decisions, lessons — those are warehouse knowledge, queried per the WAREHOUSE QUERY POLICY

AGENT_LAWS.md (.claude/rules/) — always auto-loaded; ~20 lines hard ceiling 40
  scope: 4 Laws — behavioral constraints, every agent every session; no project-specific content
  not: project-specific rules — those belong in CLAUDE.md or skill files

FORMAT RULES
Both files must maintain:
  No --- decorative separators
  No **bold** on section headers
  No decorative empty lines between sections
  Code blocks stay — they are content, not decoration
  Pointers over copies: CLAUDE.md points at the warehouse for knowledge, never duplicates it
  Every new section must fit the file's canonical scope — knowledge content goes to the warehouse, not here

AGENT BEHAVIOR
Never write directly to either protected file.
New knowledge (a decision / constraint / lesson) is NOT a doc edit — author it as a warehouse
proposal via docs/skills/warehouse-ingest.md; the Senate judges and ingests on owner HITL.
If a CLAUDE.md / AGENT_LAWS.md change is needed: output an exact, copy-paste ready flag in
the agent's handover block — vague flags are invalid.
Flag mid-pipeline; execute the file write only after Senate Censura closes the ticket and
owner reviews proposed text. The flag captures the decision immediately — only the file write
is deferred until code is stable.
Flags live in the handover blocks of `<TICKET-ID>_handover.md` (D4).

FLAG FORMATS
For file updates (CLAUDE.md, AGENT_LAWS.md):
  ⚠️ [FILE] UPDATE NEEDED
  What changed: [one sentence]
  Why: [one sentence — the non-obvious reason]
  Suggested addition: [exact text, copy-paste ready — not optional]

For new knowledge (decision / constraint / lesson → warehouse):
  ⚠️ WAREHOUSE DECISION PROPOSAL NEEDED
  Title: [decision title]
  Submitted via: docs/skills/warehouse-ingest.md (propose → antechamber → Senate resolve on owner HITL)
  Suggested content: [proposal body — title / rationale / frozen context, copy-paste ready]

EXECUTION ORDER (owner executes after ticket closes)
1. Warehouse acceptance — the Senate resolves queued decision / constraint / lesson proposals (owner HITL); knowledge lands first
2. CLAUDE.md — always last; references the warehouse for knowledge, carries navigation only

PIPELINE ROLES
Consilium — loads when session involves architecture or new decisions; primary raiser of warehouse decision / constraint proposals
Praetor — loads when ticket touches CLAUDE.md/AGENT_LAWS.md or when writing any ⚠️ flag; raises a warehouse decision proposal if implementation reveals an undocumented architectural decision
Tribunus — loads when reviewing output with ⚠️ flags; flag without Suggested addition/content = HIGH finding
Senate Censura — loads every ticket close; collects all ⚠️ flags, validates format, confirms owner reviewed proposed text before closing
Probator — never loads; doc changes are not testable
Curator — never loads content; scans the handover blocks for ⚠️ prefix only — does not validate flag content

CONSTRAINTS
Never write directly to CLAUDE.md or AGENT_LAWS.md
Never write knowledge to a flat doc — a decision / constraint / lesson goes to the warehouse via warehouse-ingest.md
Never output a flag without Suggested addition or Suggested content — "something about X should be added" is invalid
Never add content to a file outside its canonical scope — knowledge belongs in the warehouse, not in CLAUDE.md
Never restore decorative formatting: ---, **Section Header**, empty spacing lines
Never duplicate warehouse knowledge into CLAUDE.md — point, never copy
