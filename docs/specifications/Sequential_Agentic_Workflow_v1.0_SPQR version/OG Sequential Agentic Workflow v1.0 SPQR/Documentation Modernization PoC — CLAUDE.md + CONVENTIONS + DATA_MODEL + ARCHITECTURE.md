---

---
| Field | Value |
| --- | --- |
| Status | Draft |
| Type | Documentation / Architecture |
| Created | 2026-05-24 |
| Author | Project Owner + Claude |

## Overview

Three core documentation files need modernization: [CLAUDE.md](http://claude.md/) (agent behavior config), [CONVENTIONS.md](http://conventions.md/) (coding patterns), DATA_[MODEL.md](http://model.md/) (schema reference). The current state has triple duplication, human-readable formatting that wastes tokens, and missing content identified from Global Design Decisions. Target: each file has one canonical scope, machine-first format, no decorative elements.

## Motivation

[CLAUDE.md](http://claude.md/) is 280 lines — community consensus and Karpathy reference cap it at 65 lines. Research confirms more rules = all rules followed worse. Conventions content exists in three places simultaneously ([CLAUDE.md](http://claude.md/) + [CONVENTIONS.md](http://conventions.md/) + Global Design Decisions). DATA_[MODEL.md](http://model.md/) is missing 6 business-critical invariants from Global Decisions. Every decorative `---` separator and `**bold label**` is a recurring token cost loaded on every session.

## Content Map

| Content | Current location | Target | Action |
| --- | --- | --- | --- |
| Stack (iOS 26, SwiftData, arch) | [CLAUDE.md](http://claude.md/) | [CLAUDE.md](http://claude.md/) | Keep, compact |
| Critical rules (isDeleted, updatedAt, [context.save](http://context.save/)(), git push NEVER) | [CLAUDE.md](http://claude.md/) | [CLAUDE.md](http://claude.md/) | Keep, machine-first |
| API key security: hardcoding ban + xcconfig injection + DevOps scan script | [DECISIONS.md](http://decisions.md/) legacy | [CLAUDE.md](http://claude.md/) | New — addition to Critical rules; add as separate Coding Principia section: surgical, pattern first, no comments, no speculation |
| Phase boundaries (1–4) | [CLAUDE.md](http://claude.md/) | [CLAUDE.md](http://claude.md/) | Keep, compact |
| Navigation rules | [CLAUDE.md](http://claude.md/) | [CLAUDE.md](http://claude.md/) | Keep, 3 lines |
| Agent workflow + quality signals | [CLAUDE.md](http://claude.md/) | [CLAUDE.md](http://claude.md/) | Keep, compact |
| Docs references | [CLAUDE.md](http://claude.md/) | [CLAUDE.md](http://claude.md/) | Keep, 3 lines |
| Entity schema (~40 lines) | [CLAUDE.md](http://claude.md/)  • DATA_[MODEL.md](http://model.md/) | DATA_[MODEL.md](http://model.md/) | Remove from [CLAUDE.md](http://claude.md/) |
| searchIndex composition | [CLAUDE.md](http://claude.md/) | DATA_[MODEL.md](http://model.md/) | Move + Update (add Markdown stripping) |
| Constants table | [CLAUDE.md](http://claude.md/)  • DATA_[MODEL.md](http://model.md/) | DATA_[MODEL.md](http://model.md/) | Remove from [CLAUDE.md](http://claude.md/) |
| MV vs MVVM | [CLAUDE.md](http://claude.md/)  • [CONVENTIONS.md](http://conventions.md/)  • Global | [CONVENTIONS.md](http://conventions.md/) | Canonical — remove from others |
| MV/MVVM boundary: clearer criteria (MVVM = forms/editable state, MV = display-only) | [DECISIONS.md](http://decisions.md/) legacy | [CONVENTIONS.md](http://conventions.md/) | New — sharpens existing MV/MVVM section |
| Error patterns | [CLAUDE.md](http://claude.md/)  • [CONVENTIONS.md](http://conventions.md/)  • Global | [CONVENTIONS.md](http://conventions.md/) | Canonical — remove from others |
| Naming conventions | [CONVENTIONS.md](http://conventions.md/)  • Global | [CONVENTIONS.md](http://conventions.md/) | Canonical — remove from Global |
| Folder structure | [CONVENTIONS.md](http://conventions.md/)  • Global | [CONVENTIONS.md](http://conventions.md/) | Canonical — remove from Global |
| UserPreferences fetch-or-create code | [CONVENTIONS.md](http://conventions.md/) | [CONVENTIONS.md](http://conventions.md/) | Keep |
| Strings / xcstrings key format | [CLAUDE.md](http://claude.md/)  • [CONVENTIONS.md](http://conventions.md/) | [CONVENTIONS.md](http://conventions.md/) | Canonical |
| Position ordering code | [CLAUDE.md](http://claude.md/)  • [CONVENTIONS.md](http://conventions.md/) | [CONVENTIONS.md](http://conventions.md/) | Canonical |
| Position rebalancing: gap < 1e-10 → full rebalance, mandatory on every drag-drop write path | [DECISIONS.md](http://decisions.md/) legacy | [CONVENTIONS.md](http://conventions.md/) | New — mandatory companion to Position ordering |
| JSON blobs encode/decode code | [CONVENTIONS.md](http://conventions.md/) | [CONVENTIONS.md](http://conventions.md/) | Keep |
| OSLog setup | [CONVENTIONS.md](http://conventions.md/) | [CONVENTIONS.md](http://conventions.md/) | Keep |
| SwiftLint config | [CONVENTIONS.md](http://conventions.md/) | [CONVENTIONS.md](http://conventions.md/) | Keep |
| Commit message format | [CONVENTIONS.md](http://conventions.md/) | [CONVENTIONS.md](http://conventions.md/) | Keep |
| Entity tree + @Model code | DATA_[MODEL.md](http://model.md/) | DATA_[MODEL.md](http://model.md/) | Keep |
| StepJSON / IngredientLineJSON | DATA_[MODEL.md](http://model.md/) | DATA_[MODEL.md](http://model.md/) | Keep |
| Image storage rules | DATA_[MODEL.md](http://model.md/) | DATA_[MODEL.md](http://model.md/) | Keep |
| Schema versioning | DATA_[MODEL.md](http://model.md/) | DATA_[MODEL.md](http://model.md/) | Keep + extend |
| UserPreferences startup deduplication (A12) | Global Decisions | DATA_[MODEL.md](http://model.md/) | New |
| CleanupService 30-day soft delete detail (A13) | Global Decisions | DATA_[MODEL.md](http://model.md/) | New |
| CookingSession snapshot requirement (G9) | Global Decisions | DATA_[MODEL.md](http://model.md/) | New — Phase 2 flag |
| updatedAt WHY — CloudKit conflict reason (A18) | Global Decisions | DATA_[MODEL.md](http://model.md/) | New |
| deviceId reset warning (A19) | Global Decisions | DATA_[MODEL.md](http://model.md/) | New |
| Migration: lightweight vs SchemaMigrationPlan (A10) | Global Decisions | DATA_[MODEL.md](http://model.md/) | New |

## [ARCHITECTURE.md](http://architecture.md/) Content Map

| Content | Current location | Target | Action |
| --- | --- | --- | --- |
| System layers topology (UI → ViewModel → SwiftData) | [ARCHITECTURE.md](http://architecture.md/) | [ARCHITECTURE.md](http://architecture.md/) | Keep — unique, not in any other file |
| Architectural invariants: Services via @Environment, Views never navigate, AppCoordinator owns all navigation | [ARCHITECTURE.md](http://architecture.md/) | [ARCHITECTURE.md](http://architecture.md/) | Keep + make explicit |
| Architectural rationale: local-first WHY, coordinator pattern WHY | [ARCHITECTURE.md](http://architecture.md/) | docs/decisions/ | Move — these are ADRs |
| Navigation rules (duplicate) | [ARCHITECTURE.md](http://architecture.md/) | [CLAUDE.md](http://claude.md/) | Remove from [ARCHITECTURE.md](http://architecture.md/) |
| MV/MVVM rule (duplicate) | [ARCHITECTURE.md](http://architecture.md/) | [CONVENTIONS.md](http://conventions.md/) | Remove from [ARCHITECTURE.md](http://architecture.md/) |
| Data model principles overview (duplicate) | [ARCHITECTURE.md](http://architecture.md/) | DATA_[MODEL.md](http://model.md/) | Remove from [ARCHITECTURE.md](http://architecture.md/) |
| Phase boundaries (duplicate) | [ARCHITECTURE.md](http://architecture.md/) | [CLAUDE.md](http://claude.md/) | Remove from [ARCHITECTURE.md](http://architecture.md/) |
| Service layer list (duplicate) | [ARCHITECTURE.md](http://architecture.md/) | [CONVENTIONS.md](http://conventions.md/) | Remove from [ARCHITECTURE.md](http://architecture.md/) |

## Target State Per File

[**CLAUDE.md**](http://claude.md/)** — target: ~80 lines, machine-first, always loaded**

Only what every agent must know in every session. No pattern descriptions, no code examples, no entity detail. References [CONVENTIONS.md](http://conventions.md/) and DATA_[MODEL.md](http://model.md/) for everything else.

```javascript
Sections: stack | critical rules | coding principia | phase boundaries | navigation rules | agent workflow | docs refs
```

[**CONVENTIONS.md**](http://conventions.md/)** — on-demand, Praetor + Tribunus**

Canonical source for all coding patterns. Grows with the project — new patterns added via `⚠️ CONVENTIONS UPDATE NEEDED` flag after ticket closes. Machine-first format: no decorative separators, compact structure.

```javascript
Sections: naming | folder structure | MV/MVVM | services | UserPreferences | strings | position | isDeleted | JSON | OSLog | SwiftLint | commit messages | error patterns
```

> [!note] 📝
> Note — incorporate from [DECISIONS.md](http://decisions.md/) legacy when writing [CONVENTIONS.md](http://conventions.md/):
> - DI pattern: @Environment for Views, init injection for ViewModels (never @Environment inside ViewModel body)
> - SwiftData ModelContainer: in-memory config for tests (`ModelConfiguration(isStoredInMemoryOnly: true)`), fatalError on container init failure
> - Views/ folder detail: Components/ rule — if a View is used by 2+ features it goes to Views/Components/
> - OSLog detail: one static Logger per service category, subsystem `"com.foodoire.app"`, file `Utilities/Logger+Foodoire.swift`

```javascript
**DATA_**[**MODEL.md**](http://MODEL.md)** — on-demand, schema work only**
Canonical schema reference. Grows with each phase. Machine-first but code blocks stay — Swift code IS the documentation. Updated via `⚠️ DATA_MODEL UPDATE NEEDED` flag after ticket closes.
```

Sections: entity tree | per-entity @Model | JSON structs | constants | image storage | schema versioning | business invariants (new) | phase 2 flags (new)

```javascript
## Maintenance Model
**Flagging — any agent in the pipeline:**
```

⚠️ [FILE] UPDATE NEEDED

What changed: [description]

Why: [reason]

Suggested addition: [exact text — copy-paste ready]

```javascript
**When flags get acted on:**
```

Agent flags → flag stays in Notion comment

Senate Censura closes ticket → collects all flags → validates

Owner executes doc updates in a separate session

```javascript
Flag is not acted on mid-pipeline — code may still change within the same ticket. Only after ticket is closed.
**Future housekeeping agent** — a dedicated assistant agent will collect and execute flags. Deferred — not needed now.
[**ARCHITECTURE.md**](http://ARCHITECTURE.md)** — on-demand, Consilium only**
Unique content only: system topology map (\~5 lines) + architectural invariants not found in other files (\~5 lines). Target: \~15 lines. Everything else removed to eliminate divergence risk. Changes proposed by Consilium after whiteboarding sessions, or by Praetor when a ticket touches an architectural boundary.
```

Sections: system layers topology | architectural invariants

```javascript
## Execution Order
Files must be updated in this order — [CLAUDE.md](http://CLAUDE.md) last, because it references the others:
```

1. [ARCHITECTURE.md](http://architecture.md/) → reduce to ~15 lines (remove duplicates, keep topology + invariants, move ADR content to docs/decisions/)
2. DATA_[MODEL.md](http://model.md/)  → add 6 new entries, remove decorative formatting
3. [CONVENTIONS.md](http://conventions.md/) → receive content from [CLAUDE.md](http://claude.md/) + Global Decisions, machine-first
4. [CLAUDE.md](http://claude.md/)      → remove sections, add Coding Principia, reduce to ~80 lines

```javascript
## Recommendations
### Do now
- Update DATA_[MODEL.md](http://MODEL.md) — add 6 new entries from Global Decisions, machine-first reformatting
- Update [CONVENTIONS.md](http://CONVENTIONS.md) — make canonical, receive [CLAUDE.md](http://CLAUDE.md) content + Global Decisions Code Conventions section
- Update [CLAUDE.md](http://CLAUDE.md) — remove sections, add Coding Principia, reduce to ~80 lines; update Agent Workflow section: replace old agent names (Dev Engineer → Peer Reviewer → QA → DevOps) with Senate: Consilium → Praetor → Tribunus → Probator → Curator → Senate: Censura; update Mandatory checkpoints (DevOps verdict → Curator verdict, Master Architect RED → Senate Censura RED)
- Rebuild [CLAUDE.md](http://CLAUDE.md) Skills table: update agent names in existing rows (Dev Engineer → Praetor, Peer Reviewer → Tribunus, QA Specialist → Probator, Master Architect → Senate); retire whiteboarding.md row; add rows for all new skill files (Collegium pipeline, Senate, Quaestor, doc-maintenance)
- Note: DATA_MODEL.md Content Map rows reference pre-restructuring DECISIONS.md numbering (A10, A12, A13, G9, A18, A19) — cross-reference against new A1–A18 at execution time
- Add `⚠️ UPDATE NEEDED` signal format to every agent skill output section
- Add to Senate Censura output skill: "collect and confirm all UPDATE NEEDED flags before closing"
### Defer
- Remove Global Design Decisions Code Conventions section — after workflow design is complete
- Dedicated housekeeping agent for flag execution
- Full machine-first reformatting of [CONVENTIONS.md](http://CONVENTIONS.md) — iteratively, as files are touched
### Discard
- Human-readable formatting (`---`, `**bold labels**`, decorative empty lines) — from all three files
- Duplicated content — per the Action column above
## Descoped
- Global Design Decisions open questions (D1, D3, etc.) — stay in Notion, owner updates when reached
## References
- Collegium Pipeline PoC: <mention-page url="https://www.notion.so/36968d5de1e88197af07d6688d682a70"/>
- Global Design & Architecture Decisions: <mention-page url="https://www.notion.so/35268d5de1e8817a89e1f480107c3f03"/>
- [CLAUDE.md](http://CLAUDE.md): `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/CLAUDE.md`
- DATA_[MODEL.md](http://MODEL.md): `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/docs/DATA_MODEL.md`
- [CONVENTIONS.md](http://CONVENTIONS.md): `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/docs/CONVENTIONS.md`
- Karpathy [CLAUDE.md](http://CLAUDE.md) (65-line reference): [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- claudelint 150-line ceiling: [https://claudelint.com/rules/claude-md/claude-md-size](https://claudelint.com/rules/claude-md/claude-md-size)
```