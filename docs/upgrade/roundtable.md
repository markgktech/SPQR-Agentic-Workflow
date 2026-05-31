ROUNDTABLE SKILL

PREPARATION
Master reads all relevant tickets and forms an initial reading before invoking. Roundtable confirms, challenges, or extends that reading — it does not generate from blank slate. Roundtable called without prior preparation produces shallow output.

TRIGGER
Mandatory: Phase 2 — before item list is finalised and Phase 3 begins
Master's call (no owner approval needed):
- After execution group output containing out-of-scope finding, stalled item, or Changes Made section deviating from brief
- When a Phase 3 decision has significant architectural implications (cross-cutting, unresolved — master's judgment; lean against if no concrete uncertainty exists)
- When two items appear to conflict
Not needed: routine execution group outputs with no surprises; minor wording or formatting decisions; questions owner has explicitly closed

PERSONAS
Defined in upgrade-agent.md CONFIG — loaded before this file.
Roles: Persona 1 = Dev Process Architect, Persona 2 = Agentic Trends Expert. Focus areas are fixed.

RULES
- Each persona arrives with independent position — no deference to the other's prior statement
- Both personas can update position when challenged with new evidence
- Neither persona adjusts conclusions based on the master's apparent preference
- Master synthesises — personas do not reach consensus on behalf of the master
- Roundtable produces findings, not approvals; master decides what to do with them

AGENT-ACTIONABILITY TEST
Primary lens for every roundtable review: can a stateless execution agent apply this rule without additional context?
If uncertain — raise as finding, do not clean pass.
Non-actionable patterns to flag:
- Time-based rules an agent cannot measure ("under 10 minutes")
- Conditional logic with no stated condition ("field is always yes")
- Ambiguous variants with no selection criteria ("two formats, no rule for which to use")

CLEAN PASS RULE
If a persona finds no genuine problem, state it explicitly with justification:
"CLEAN PASS — checked [specific aspects], no issues found."
Unjustified clean pass is not valid.
Law 4 (Be like Spock) applies both ways: suppress nothing real, invent nothing.

EXECUTION PROTOCOL (mandatory — treat as checklist, not prose)
1. Run first round
2. Apply all modifications found
3. CHECK: did the first round produce any modifications?
   YES → run second round on modified/new content only, then go to step 4
   NO  → justified clean pass, go to step 4
4. Write output summary and close

OUTPUT
Master produces a short summary at the end of every roundtable:
- Decisions made or confirmed
- Points to update (which phase, which file, which Notion page)
- Open items requiring new tickets (flagged only — ticket creation and ID assignment is the owner's action)
Summary drives next action — not the discussion itself.

NEVER
- Reopen questions the owner has explicitly closed
- Use roundtable as an approval gate — master does not need roundtable sign-off to proceed
- Treat roundtable as substitute for owner confirmation at the three explicit checkpoints
- Let personas reach consensus on behalf of the master
- Suppress a roundtable finding or issue a silent clean pass (Law 4)
- Invoke roundtable before reading all relevant tickets and forming an initial reading (both steps required)
- Skip the output summary — no action follows a roundtable without a written summary
- Create or assign ticket IDs for open items — flag only; ticket creation is the owner's action
- Invent findings when none exist
