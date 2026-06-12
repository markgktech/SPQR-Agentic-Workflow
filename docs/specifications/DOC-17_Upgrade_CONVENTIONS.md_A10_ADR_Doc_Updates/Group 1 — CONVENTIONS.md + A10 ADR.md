---

---
## Brief

GROUP: [CONVENTIONS.md](http://conventions.md/) + A10 ADR

ORDER: 1/1

REPO: Foodoire

NOTION_REF: this page

RATIONALE: Items 2-4 touch the same file ([CONVENTIONS.md](http://conventions.md/)); Item 5 is independent but small and same repo; all doc-only, no dependencies between items

FILL_CHANGES_MADE: yes

PRE_FLIGHT:

- DOC-17 ticket (full item content + exact replacement texts): [[DOC-17 Pending Doc Updates — CLAUDE.md, CONVENTIONS.md, A10 ADR]]
- Read docs/decisions/[a10-aiservice-isolation.md](http://a10-aiservice-isolation.md/) before editing (no anchor in ticket — determine insertion point from file structure)

FILES:

- `docs/CONVENTIONS.md`: (a) replace full ## Services section with exact text from DOC-17 Item 2 — includes service list + actor isolation table + DefaultActorIsolation note; (b) add service error convention after Toast/Banner/Modal line in ## Error Patterns — DOC-17 Item 3; (c) remove two provisional inline comments from ## MV vs MVVM code example — DOC-17 Item 4
- `docs/decisions/a10-aiservice-isolation.md`: add Phase 1 note to ADR body — DOC-17 Item 5; read file first to confirm insertion point (after main Decision section or end of file)

EXECUTION ORDER: [CONVENTIONS.md](http://conventions.md/) Items 2, 3, 4 (same file — one edit session) → [a10-aiservice-isolation.md](http://a10-aiservice-isolation.md/) Item 5

FORMAT RULES:

- No --- decorative separators or **bold** section headers introduced
- Actor isolation table from DOC-17: render as plain Markdown table (not Notion table syntax)
- Do not reformat surrounding content

OUT OF SCOPE: [CLAUDE.md](http://claude.md/) — owner applies manually after this group completes

ACCEPTANCE CRITERIA (from ticket):

- [CONVENTIONS.md](http://conventions.md/) ## Services: actor isolation map + DefaultActorIsolation note + MarkdownService constraint present
- [CONVENTIONS.md](http://conventions.md/) ## Error Patterns: typed enum convention + Sendable + empty catch = Tribunus BLOCK present
- [CONVENTIONS.md](http://conventions.md/) ## MV vs MVVM: provisional RecipeService signature comment removed; `throws` sync confirmed
- docs/decisions/[a10-aiservice-isolation.md](http://a10-aiservice-isolation.md/): Phase 1 note added

## Changes Made

**docs/**[**CONVENTIONS.md**](http://conventions.md/)

- 
    ## Services: replaced full section — service list updated (CookingListService added; RecipeService unwrapped to single line; MarkdownService constraint added); actor isolation table added (11 services, 4 columns); DefaultActorIsolation = MainActor note added
- 
    ## Error Patterns: inserted 5-line service error convention block after Toast/Banner/Modal line
- 
    ## MV vs MVVM: removed two provisional inline comments from softDelete code example

**docs/decisions/**[**a10-aiservice-isolation.md**](http://a10-aiservice-isolation.md/)

- Phase 1 note added after Consequences line (typed error stub pattern supersedes #if DEBUG guard)