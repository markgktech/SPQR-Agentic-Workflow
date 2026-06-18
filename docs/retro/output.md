---
name: retro-output
description: RETROACTIO output protocol — local retro file mirroring the template EXACTLY; rule-rot pass; max 3 actions; flag-only; records the next marker
---

PRECONDITION
Owner has explicitly closed the discussion phase with an affirmative (per docs/retro/discussion.md). Never produce output before closure.

TEMPLATE FIDELITY
Follow the local retro template `templates/retro_template.md` (in the consuming project's work_documents/ vault — not Notion) EXACTLY — same sections, same order, no additions or removals.
Read it first, then populate each section. Do not invent sections; do not drop "skip on first run" sections — mark them skipped.

OUTPUT TARGET (D13)
Create the retro as a local file in the work_documents/ vault (not a Notion child page).
Title / H1 format: Retro #[N] — [Milestone name]; add the file to `Retroactio.md` (the retro MOC).
Frontmatter:
  content: retro
  retro_n: [N — start at 1; increment by reading the prior retro for the last number]
  phase: [the project phase this retro covers]
  verdict: [the retro template's OWN vocabulary — NOT Censura GREEN/RED]
  tickets_reviewed: [[<TICKET-ID>]]   # one wikilink per in-scope ticket hub
  session_id: [$CLAUDE_CODE_SESSION_ID from input.md; `—` if unset]

DOES NOT FOLLOW ticket-comment.md
Output is a local retro file, not a handover block — ticket-comment.md does NOT apply. No routing / still_solving / impl_doc fields.

ACTIONS
Max 3 action items. Every item has a type (DOC / SPIKE / owner decision) and an owner decision.
Flag candidates only — NEVER create DOC / SPIKE / SAW tickets. The owner decides what becomes a ticket.

RULE-ROT PASS
Run a pruning pass alongside the additive findings: flag pipeline rules / skills that no longer fire — never triggered a real catch in recent runs — as removal candidates.
Evidence-based: judged from the external record (which rules actually caught something in LESSONS / Censura), NOT from model self-report.
Flag only — the owner removes. Rule-rot candidates count toward the max-3 actions or are listed as a clearly-marked subset, never as silent additions.

CLOSING MARKER
Record the closing marker for the next retro (a date or explicit marker) — this defines input.md's <marker> for the next run. State it explicitly on the page so the next Retrospector can find it.

NEVER
Never add, remove, or reorder template sections
Never create DOC / SPIKE / SAW tickets — flag only
Never exceed 3 action items
Never report rule-rot from self-report — evidence from the record only
Never omit session_id from the frontmatter
Never omit the closing marker
Never produce output before explicit owner closure
