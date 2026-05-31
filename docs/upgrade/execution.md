SYNC GROUP: RISK-FIRST
Master obligation before writing the sync group brief: identify what could leak or be left unfilled. Analyze failure modes first; derive the substitution list from that analysis. Do not jump to "what needs to change" — skipping failure mode analysis produces incomplete substitution lists.
Execution agent receives a brief that has already completed this analysis. The substitution list and grep checklist in the brief are its output.
Sync group runs after all project-specific groups are complete and owner-confirmed. Always its own execution group.

MANDATORY SUBSTITUTIONS
During sync, replace:
- Real persona names → [Name 1]–[Name 4] / [Master Persona 1]–[Master Persona 2]
- Project-specific content → [PROJECT_BOUNDARIES] or equivalent placeholder
- Hardcoded Notion page IDs → named placeholders from CONFIGURE.md

MANDATORY GREP
After sync, check for:
- Real names that slipped through
- Hardcoded Notion page IDs (32-character hex strings)
- Full Notion URLs (notion.so/...)
- Project-specific paths, layer names, or entity references
- Unfilled [PROJECT_BOUNDARIES] placeholders left empty rather than substituted

OWNER CONFIRMATION GATE
Hard gate — not a suggestion. Master does not launch next group until owner confirms.
Changes Made condition: execution agent must fill Changes Made in Notion before gate opens. Empty or missing Changes Made = execution incomplete; gate does not open.
Confirmation can be lightweight: owner reads Changes Made and says go. Full file review not required.

SESSION HANDOFF
Master writes the complete session starter for each execution group. Owner copies it and opens a new session. Master does not hand off verbally or summarize. The written brief IS the handoff. An incomplete brief produces an incomplete execution session.

OUT-OF-SCOPE DISCOVERY
Report in output summary only. Do not handle unilaterally. Master decides whether to add a new group or open a ticket.

BLOCKERS
Post blocker comment on the ticket and stop. Owner decides next step. Do not retry indefinitely or make assumptions to work around the blocker.

NEVER
- Launch next group without owner confirmation
- Confirm group complete when Changes Made is empty
- Expand execution scope beyond brief
- Run parallel groups
- Handle out-of-scope discovery unilaterally
- Modify files outside the brief
- Plan, architect, or scope — receive the brief and execute only
- Run git commit or git push
