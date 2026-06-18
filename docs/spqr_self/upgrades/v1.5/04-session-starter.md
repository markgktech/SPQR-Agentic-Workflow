You are an execution agent for SPQR upgrade run v1.5, Group 4 (CORRECTIO bug pipeline — SAW-29).

PRE-FLIGHT (load in order):
  - docs/upgrade/execution.md                                          (execution protocol — receive brief, execute only)
  - docs/spqr_self/upgrades/v1.5/04-bug-pipeline.md                    (YOUR BRIEF — FILES, passes, guardrails — binding)
  - docs/spqr_self/poc/SAW-29 Bug Pipeline — PoC.md                    (CONTENT source — Decisions D1–D27; the brief derives from it; PoC wins on conflict)
  - docs/skills/{consilium-input,consilium-discussion,probator-input,curator-input}.md   (FORM exemplar — skill phase-boundary convention for the NEW bug-pipeline.md)
  - docs/agents/{praetor,probator,senate,tribunus,curator}.md , docs/skills/{debugging-tribunus-input,git-workflow}.md , docs/agents/session-starters.md   (edit targets — read current form first)
  - docs/skills/{collegium-veto,praetor-revision}.md                   (the veto/revision mechanic the bug flow REUSES — D26; read, do not edit)
  - /Users/kovacsmark/Documents/RecipeAPP/Foodoire/docs/work_documents/templates/{bug_output_template,ticket_hub_template,handover_template}.md   (FORM reference ONLY — DO NOT edit; Foodoire is out of scope)

YOUR BRIEF + WHERE YOU WRITE: RUN_DOC = docs/spqr_self/upgrades/v1.5/04-bug-pipeline.md

Read the Brief there, do the work on the 9 FILES listed (2 passes), then fill its "## Changes Made" section
(replace the _(pending execution)_ sentinel) — file by file, with a short Verification block confirming OUT OF SCOPE was respected.

Key reminders (full list in the brief):
  - The NEW docs/skills/bug-pipeline.md MUST follow the existing skill convention (frontmatter, LOAD ORDER, explicit phase boundaries mirroring OPUS/EXPLORACIO, NEVER block) — D25.
  - The runtime NEVER rules you WRITE INTO the bug-flow agent definitions are constraints on the consuming-project agents, NOT on you now.
  - Severity vocabulary is HIGH / MED / LOW (never sev1/2/3). Quaestor escalation = a normal EXPLORACIO spike ticket; do NOT edit quaestor.md (D12).
  - Do not touch any Foodoire / consuming-project file or template. Do not touch the MAIN folder-note (v1.5.md) or sibling sub-docs. Do not pin model tiers (D10 descoped). Do not run git commit or git push.

Report at the end of each PASS; flag any out-of-scope discovery for the master — do not act on it.
