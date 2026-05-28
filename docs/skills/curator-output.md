VERDICT DECLARATION
Declare verdict per area before issuing final verdict — no silent pass.
Format per area: [area] — [PASS | NEEDS ATTENTION | NEEDS WORK] — [one sentence]
Final verdict is the highest-severity finding across all 8 areas.

VERDICT DEFINITIONS
Ready to Merge: all 8 areas PASS
Needs Attention: no blocker; one or more areas flagged — pipeline continues, owner awareness required
Needs Work: any area NEEDS WORK — pipeline stops; owner resolves before merge

NEEDS ATTENTION PROTOCOL
Every Needs Attention item must be explicitly listed in ticket comment.
Censura loads these as mandatory input — vague or implicit items are invalid.

CLAUDE.md AREA
If claude=NEEDS ATTENTION or NEEDS WORK: output exact flag per doc-maintenance.md format.
⚠️ CLAUDE.md UPDATE NEEDED
What changed: [one sentence]
Why: [one sentence]
Suggested addition: [exact text — copy-paste ready]
Vague flags ("something about X should be added") are invalid — HIGH finding.

TICKET COMMENT
Post using ticket-comment.md protocol.
Required fields:
  still_solving: [ticket goal restated]
  mode: CURATOR
  verdict: [Ready to Merge | Needs Attention | Needs Work]
  areas: build=[P|NA|NW], lint=[P|NA|NW], claude=[P|NA|NW], phase=[P|NA|NW], i18n=[P|NA|NW], dead-code=[P|NA|NW], risk=[P|NA|NW], scope=[P|NA|N/A]
  needs_attention: [area — specific item] | none
  addressed: [confirmation prior expected_outputs met — or gap noted]
  expected_outputs: [what Censura must verify | "pipeline complete" if Censura skipped]
  routing: → Senate:Censura | → OWNER (Needs Work)

CONSTRAINTS
Never declare final verdict before all 8 areas are checked
Never omit an area from the areas field — silence is not a pass
Never route to Senate:Censura if verdict is Needs Work
Never list vague Needs Attention items — Censura loads these; specificity required
Never carry prior agent opinions into verdict reasoning
