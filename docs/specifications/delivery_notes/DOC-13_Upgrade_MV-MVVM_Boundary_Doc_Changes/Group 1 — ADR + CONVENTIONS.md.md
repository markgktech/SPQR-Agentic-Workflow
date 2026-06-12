---

---
## Brief

GROUP: ADR + [CONVENTIONS.md](http://conventions.md/)

ORDER: 1/1

REPO: Foodoire

NOTION_REF: this page

RATIONALE: All doc-only changes to Foodoire project repo; ADR and [CONVENTIONS.md](http://conventions.md/) are independent but ticket-sequenced (ADR → [CONVENTIONS.md](http://conventions.md/))

FILL_CHANGES_MADE: yes

PRE_FLIGHT:

- DOC-13 ticket (full item content): [[DOC-13 AI MV-MVVM Boundary — Apply SPIKE-002 Censura doc changes]]

FILES:

- `docs/decisions/a21-mv-mvvm-boundary.md`: create new file — exact content from DOC-13 Item 1
- `docs/decisions/INDEX.md`: add one line after A20 — exact text from DOC-13 Item 1
- `docs/CONVENTIONS.md`: (a) replace full ## MV vs MVVM section + add 3rd code example — DOC-13 Item 2; (b) add RecipeService entry after NotificationService in ## Services — DOC-13 Item 3

EXECUTION ORDER: [a21-mv-mvvm-boundary.md](http://a21-mv-mvvm-boundary.md/) → [INDEX.md](http://index.md/) → [CONVENTIONS.md](http://conventions.md/)

OUT OF SCOPE: [CLAUDE.md](http://claude.md/) — owner applies manually after this group completes

ACCEPTANCE CRITERIA (from ticket):

- `docs/decisions/a21-mv-mvvm-boundary.md` created with exact content
- `docs/decisions/INDEX.md` A21 line added after A20
- `CONVENTIONS.md` ## MV vs MVVM section fully replaced
- `CONVENTIONS.md` ## MV vs MVVM third code example added after existing two
- `CONVENTIONS.md` ## Services RecipeService entry present after NotificationService
- No `---` decorative separators or `**bold**` section headers introduced

## Changes Made

- `docs/decisions/a21-mv-mvvm-boundary.md`: created new file — verbatim content from DOC-13 Item 1 including DEV-XXX placeholder
- `docs/decisions/INDEX.md`: added A21 line after A20 entry
- `docs/CONVENTIONS.md` (## MV vs MVVM): replaced text content — new boundary criterion, updated screen lists, "does NOT make MVVM" block, cascade mutation note
- `docs/CONVENTIONS.md` (## MV vs MVVM): added third Swift code example (VaultView / RecipeService / softDelete) after existing two examples
- `docs/CONVENTIONS.md` (## Services): added RecipeService entry after NotificationService line