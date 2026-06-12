---

---
## What

Update the generic SPQR repo [README.md](http://readme.md/) for v1.2. Insert changes in the right place — not appended. Review the full file first. Update version history.

**Repo:** `/Users/kovacsmark/Documents/GitHub/Marks-agentic-workflow-SPQR/README.md`

---

## Changes Required

**Title:** `SPQR v1.1` → `SPQR v1.2`

**How to adopt — before the numbered steps:** Add one non-technical sentence pointing to [CONFIGURE.md](http://configure.md/) as the starting point for setup. Audience: someone reading this for the first time. Example tone: "Before filling anything in, open `docs/CONFIGURE.md` — it lists every placeholder in the workflow, which file it lives in, and what to put in it."

**How to adopt — Step 4 (Set up Notion):** Update to mention that Notion setup now includes ticket templates (one per type: Spike, Feature, Bug, Doc) and a spike doc parent page. Point to [CONFIGURE.md](http://configure.md/) for the full list of IDs needed. Keep it short — don't duplicate [CONFIGURE.md](http://configure.md/).

**How to adopt — Step 5 (**[**session-starters.md**](http://session-starters.md/)**):** Add PERSONAS section alongside [PROJECT_PATH]: "fill in [PROJECT_PATH] and the PERSONAS section with your persona names."

**File structure:** Add missing v1.2 files in the correct positions:

- `docs/CONFIGURE.md` — top-level in docs/ (above agents/)
- `docs/skills/ticket-slicing.md`
- `docs/skills/censura-ticketing-input.md`
- `docs/skills/censura-ticketing-discussion.md`
- `docs/skills/censura-ticketing-output.md`
- `docs/skills/quaestor-doc-execute.md`

**Version History — add v1.2 entry (concise, what changed and why):**

```javascript
### v1.2 (2026-05)
- Ticket creation automated: Quaestor proposes → Censura validates → owner approves → 
  Notion tickets created; shared ticket-slicing.md skill (two modes)
- Censura two-phase model: VERIFY (existing) + TICKETING phase (3 new skill files)
- Agent hygiene: 8 fixes from SPIKE-004 — handoff accuracy, date validation, context 
  alerts, spike doc location, discussion depth calibration
- DOC process: new quaestor-doc-execute.md for DOC-type ticket handling with 
  per-fix re-verification
- SPQR repo public-ready: all project-specific data replaced with named placeholders; 
  CONFIGURE.md setup guide added
```

---

## Rules

- Read the full README before making any change
- Insert content at the correct structural position — never append to section end if a better anchor exists
- [CONFIGURE.md](http://configure.md/) reference must be human-friendly, non-technical, one sentence
- Version history: terse — one bullet per theme, no implementation detail
- Do not change anything not listed above

---

## Changes Made

*Fill in at close.*