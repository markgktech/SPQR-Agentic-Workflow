---

---
## The principle

Execution order follows dependencies. The general pattern: project-specific repo first, generic repo sync after, documentation-only groups last. Deviating from this requires explicit rationale in the brief.

---

## Why project-specific first

The project-specific repo (e.g. Foodoire) contains real content in a testable context. Execution agents can verify changes against actual usage. The generic repo sync is mechanical substitution — it depends on the project-specific version being correct first.

---

## Generic repo sync rules

**Risk-first analysis before briefing.** Before writing the sync group brief, identify what could leak or be left unfilled: sensitive data, hardcoded values, project-specific references, empty placeholders. Write the substitution list from this analysis. Jumping straight to "what needs to change" skips the failure modes.

The sync group runs after all project-specific groups are complete and owner-confirmed. It is always its own execution group.

Mandatory substitutions during sync:

- Real persona names → [Name 1]–[Name 4] / [Master Persona 1]–[Master Persona 2]
- Project-specific content → [PROJECT_BOUNDARIES] or equivalent placeholder
- Hardcoded Notion page IDs → named placeholders from [CONFIGURE.md](http://configure.md/)

Mandatory grep after sync — check for:

- Real names that slipped through
- Hardcoded Notion page IDs (32-character hex strings)
- Full Notion URLs ([notion.so/](http://notion.so/)...)
- Project-specific paths, layer names, or entity references
- Unfilled [PROJECT_BOUNDARIES] placeholders left empty rather than substituted

---

## Owner confirmation between groups

The master does not launch the next group until the owner confirms the previous group's output. This is a hard gate — not a suggestion.

Confirmation requires the Changes Made section to be filled in by the execution agent. An empty or missing Changes Made section means the execution is not complete — the gate does not open until it is filled.

Confirmation can otherwise be lightweight: owner reads the Changes Made section and says go. It does not require a full review of every changed file.

---

## Parallel execution

Groups run sequentially. Two groups do not run in parallel even if they appear independent — the owner confirmation gate between groups prevents this by design.