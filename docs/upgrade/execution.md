SYNC GROUP: RISK-FIRST
NOTE — pending: generic→project propagation redesign. This sync group (direction, substitutions, grep) is unchanged by this rework and under review in a separate session. The run container (work record under docs/spqr_self/) is local and is NEVER synced. Do not redesign the sync here.
Master obligation before writing the sync group brief: identify what could leak or be left unfilled. Analyze failure modes first; derive the substitution list from that analysis. Do not jump to "what needs to change" — skipping failure mode analysis produces incomplete substitution lists.
Execution agent receives a brief that has already completed this analysis. The substitution list and grep checklist in the brief are its output.
Sync group runs after all project-specific groups are complete and owner-confirmed. Always its own execution group.

MANDATORY SUBSTITUTIONS
During sync, replace:
- Real persona names → [Name 1]–[Name 4] / [MASTER_PERSONA_1_NAME]–[MASTER_PERSONA_2_NAME]
- Project-specific content → [PROJECT_BOUNDARIES] or equivalent placeholder
- Hardcoded Notion page IDs → named placeholders from CONFIGURE.md

MANDATORY GREP
After sync, check for:
- Real names that slipped through
- Hardcoded Notion page IDs (32-character hex strings)
- Full Notion URLs (notion.so/...)
- Project-specific paths, layer names, or entity references
- Unfilled [PROJECT_BOUNDARIES] placeholders left empty rather than substituted

TRACEABILITY (SAW ↔ run)
At execution start, post a comment on the SAW ticket linking the run container (the RUN_CONTAINER path). At wrap-up, post a comment confirming completion. The external record is truth (Law 3) — write the link as a checkpoint, not only at the end.

RUN ISOLATION
A target file may be owned by at most one open run. Before opening a new run, the master greps the MAIN folder-notes for `status: open` touching the same files. Never run two open runs over the same file.

OWNER CONFIRMATION GATE
Hard gate — not a suggestion. Master does not launch next group until owner confirms.
Changes Made condition: the execution agent must fill Changes Made in its run-container sub-md before the gate opens — i.e. the "_(pending execution)_" sentinel is replaced with the actual record. An unreplaced sentinel = execution incomplete; gate does not open.
Confirmation can be lightweight: owner reads the sub-md's Changes Made and says go. Full file review not required.

SESSION HANDOFF
Master writes the complete session starter for each execution group (from templates/session_starter_template.md) and saves it in the run container. Owner copies it and opens a new session. Keep it minimal and sharp — it points to the group sub-md (RUN_DOC); the brief lives there, not duplicated in the starter. Master does not hand off verbally or summarize. The written brief IS the handoff. An incomplete brief produces an incomplete execution session.

OUT-OF-SCOPE DISCOVERY
Report in output summary only. Do not handle unilaterally. Master decides whether to add a new group or open a ticket.

BLOCKERS
Post a blocker comment on the SAW ticket and stop. Owner decides next step. Do not retry indefinitely or make assumptions to work around the blocker.

NEVER
- Launch next group without owner confirmation
- Confirm group complete when the "_(pending execution)_" sentinel is unreplaced
- Write to the MAIN folder-note or a sibling sub-md — the execution agent writes only its own sub-md's Changes Made
- Expand execution scope beyond brief
- Run parallel groups
- Handle out-of-scope discovery unilaterally
- Modify files outside the brief
- Plan, architect, or scope — receive the brief and execute only
- Run git commit or git push — the owner commits and pushes
