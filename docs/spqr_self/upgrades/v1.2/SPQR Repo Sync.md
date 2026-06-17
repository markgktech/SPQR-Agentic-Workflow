---

---
## What

Sync all v1.2 changes from Foodoire to the generic public SPQR repo. One-way copy with mandatory substitutions. No Foodoire-specific data may enter the public repo.

**Foodoire (source):** `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/docs/`

**SPQR (target):** `/Users/kovacsmark/Documents/GitHub/Marks-agentic-workflow-SPQR/docs/`

---

## Step 1 — Foodoire pre-fix (missed in Group 3)

Two files still have hardcoded names in Foodoire — fix before syncing:

- `docs/skills/consilium-discussion.md` — Tomi → [Name 1], Zsombi → [Name 2], Peti → [Name 3]
- `docs/skills/censura-discussion.md` — Tomi → [Name 1], Zsombi → [Name 2], Peti → [Name 3]

---

## Step 2 — Substitution Rules

Apply ALL of these on every file copied to SPQR.

**Names:** Tomi → [Name 1] · Zsombi → [Name 2] · Peti → [Name 3] · Timi → [Name 4]

**Project boundaries** — in [ticket-slicing.md](http://ticket-slicing.md/), replace iOS/SwiftData content with:

`[PROJECT_BOUNDARIES]`

`Replace with project-specific layer and entity slicing rules.`

**Notion IDs — replace every occurrence:**

- Spike ticket ID → `[SPIKE_TEMPLATE_ID]`
- Feature ticket ID → `[FEATURE_TEMPLATE_ID]`
- Bug ticket ID → `[BUG_TEMPLATE_ID]`
- Doc ticket ID → `[DOC_TEMPLATE_ID]`
- Spike document template ID → `[SPIKE_DOCUMENT_TEMPLATE_ID]`
- Exploracio/Spiking parent page ID → `[SPIKE_DOC_PARENT_PAGE_ID]`

---

## Step 3 — Files to Copy

**Skill files (copy + substitution rules):**

- `docs/skills/ticket-slicing.md`
- `docs/skills/censura-ticketing-input.md`
- `docs/skills/censura-ticketing-discussion.md`
- `docs/skills/censura-ticketing-output.md`
- `docs/skills/quaestor-relatio-output.md`
- `docs/skills/censura-input.md`
- `docs/skills/censura-output.md`
- `docs/skills/quaestor-relatio.md`
- `docs/skills/consilium-output.md`
- `docs/skills/quaestor-doc-execute.md`
- `docs/skills/consilium-discussion.md`
- `docs/skills/censura-discussion.md`

**Agent files (copy + substitution rules):**

- `docs/agents/senate.md`
- `docs/agents/quaestor.md`
- `docs/agents/session-starters.md` — PERSONAS section must use [Name 1]/[Name 2]/[Name 3]/[Name 4], not real names

---

## Step 4 — Mandatory Verification

After all files copied, run both grep commands. Both must return zero results. Any match = fix before closing.

```javascript
grep -r "Tomi\|Zsombi\|Peti\|Timi" /Users/kovacsmark/Documents/GitHub/Marks-agentic-workflow-SPQR/docs/
```

```javascript
grep -r "36.68d5d" /Users/kovacsmark/Documents/GitHub/Marks-agentic-workflow-SPQR/docs/
```

---

## Changes Made

**Step 1 — Foodoire pre-fix**

- `consilium-discussion.md` — already clean, no action needed
- `censura-discussion.md` — already clean, no action needed

**New skill files created in SPQR**

- `ticket-slicing.md` — created; iOS/SwiftData boundaries → `[PROJECT_BOUNDARIES]` placeholder
- `censura-ticketing-input.md` — created; all 6 Notion template IDs → placeholders
- `censura-ticketing-discussion.md` — created; clean copy
- `censura-ticketing-output.md` — created; clean copy
- `quaestor-doc-execute.md` — created; clean copy

**Existing skill files updated in SPQR**

- `censura-discussion.md` — Tomi/Zsombi/Peti → [Name 1]/[Name 2]/[Name 3]
- `censura-input.md` — added [ticket-slicing.md](http://ticket-slicing.md/) load step + EXPLORACIO pre-check block
- `censura-output.md` — added TICKETING PHASE TRIGGER + EMERGENT GAPS sections
- `consilium-output.md` — added TICKET BODY HANDOFF; expected_outputs moved from comment to ticket body
- `consilium-discussion.md` — Tomi/Zsombi/Peti → [Name 1]/[Name 2]/[Name 3]
- `quaestor-relatio-output.md` — spike doc location → parent page; [SPIKE_DOC_PARENT_PAGE_ID]; added TICKET PROPOSALS section; richer HANDOFF BLOCK
- `quaestor-relatio.md` — added DOC-XXX pre-flight step; date orientation rule; position-change flag; 80% context alert

**Agent files updated in SPQR**

- `senate.md` — [Name 1]/[Name 2]/[Name 3] personas; added CENSURA TICKETING conditional; updated PIPELINE section
- `quaestor.md` — Timi → [Name 4]; added DOC ticket pre-flight reference
- `session-starters.md` — PERSONAS section: real names → [Name 1]/[Name 2]/[Name 3]/[Name 4]

**Bonus fix (outside copy list, caught by verification grep)**

- `spike-document.md` — hardcoded Notion template URL → `[SPIKE_DOCUMENT_TEMPLATE_ID]`

**Law 4 deviation logged**

- `senate.md` — Foodoire source: "for all Foodoire features"; preserved existing SPQR wording "project features" to avoid regression