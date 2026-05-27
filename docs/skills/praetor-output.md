IMPLEMENTATION RULES
Implement ticket scope only — nothing beyond it.
Pattern first: load [project-skill-files] before writing domain code.
Surgical: one logical change at a time; no cleanup, no refactor outside ticket scope.

MUTATION RULES
Follow project mutation rules as defined in CLAUDE.md Critical Rules — no exceptions.

IMPL DOC
Load praetor-impl-doc.md and create the Implementation Notes child page before posting ticket comment.
Link the created page URL in the impl_doc field of the ticket comment.

TICKET COMMENT
Post using ticket-comment.md protocol at implementation completion.
Required fields for Praetor output:
  still_solving: [ticket goal restated]
  mode: PRAETOR
  approach_before_consilium: [1–2 sentence summary of independent approach from input phase]
  consilium_addressed: [one-line summary — detail in impl doc KEY DECISIONS]
  addressed: [empty on first run | confirmation of prior expected_outputs on revision]
  expected_outputs: [changed file list — detail in impl doc FILES CHANGED]
  impl_doc: [Notion child page URL]
  routing: → Tribunus

CLAUDE.md FLAG
If implementation reveals a needed CLAUDE.md update:
  ⚠️ CLAUDE.md UPDATE NEEDED — What changed: [describe] | Why: [rationale] | Suggested: [exact text]
Never update CLAUDE.md directly — flag only; owner decides.

CONSTRAINTS
Never implement beyond ticket scope
Never skip approach_before_consilium — even if brief
Never skip consilium_addressed — even if brief ("see impl doc" is valid)
Never skip impl doc creation — ticket comment without impl_doc URL is invalid
Never update CLAUDE.md directly — flag only
Never post ticket comment before impl doc exists and URL is linked
