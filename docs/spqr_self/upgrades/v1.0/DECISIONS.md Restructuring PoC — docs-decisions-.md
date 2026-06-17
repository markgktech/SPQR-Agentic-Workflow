---

---
| Field | Value |
| --- | --- |
| Status | Draft |
| Type | Documentation / Architecture |
| Created | 2026-05-24 |
| Author | Project Owner + Claude |

## Overview

The current `docs/DECISIONS.md` is 513 lines after a single spike session — a monolith anti-pattern. Individual ADR files replace it: one decision per file, a lightweight `docs/decisions/INDEX.md` as the only always-scanned entry point. No Notion dependency. All files are readable via the Read tool on demand.

## Motivation

A 513-line file loaded in full costs tokens proportional to its size. Most of that content is irrelevant to any given ticket. Individual files let the agent load exactly the ADR it needs. The [INDEX.md](http://index.md/) stays compact (~25 lines) so it can be scanned cheaply. Entries that belong elsewhere ([CONVENTIONS.md](http://conventions.md/), DATA_[MODEL.md](http://model.md/), [CLAUDE.md](http://claude.md/)) are migrated out — tracked in the Documentation Modernization PoC — leaving only true architectural decisions.

## Target Structure

```javascript
docs/
  decisions/
    INDEX.md          ≈ 25 lines — always-scanned list of all ADRs
    a01-recipe-counter-storage.md
    a02-rich-text-storage.md
    ...
    a18-recipe-limit-scope.md
  DECISIONS.md        ← frozen, deleted only when new set is fully deployed
```

## [INDEX.md](http://index.md/) Format

```javascript
# ADR Index
# One line per decision. Load individual file for full rationale.

A1   Recipe counter storage — SwiftData UserPreferences, never decrement on delete
A2   Rich text storage — Markdown String, not AttributedString
A3   No draft entity — @State only, data lost on crash (Phase 3 deferred)
A4   Image compression — 0.8 → 0.6 → Banner error
A5   Content moderation — deferred to Phase 2, VNClassifyImageRequest [borderline]
A6   String Catalog (.xcstrings) — supersedes legacy Localizable.strings
A7   AppCoordinator — @Observable + typed AppDestination enum + recipeSheet property
A8   Position field — Double, gap-based (prev+next)/2.0
A9   Cook count split — manualCookCount + sessionCookCount, UI shows sum
A10  AIService isolation — client-side Phase 1, proxy Phase 2
A11  AnalyticsService isolation — PostHog recommended, Phase 1 event list
A12  Default navigation — push default, modal/sheet/alert exceptions
A13  AppCoordinator pattern — why centralized coordinator, deep link rationale
A14  Error display — Toast / Banner / Modal three-tier
A15  SwiftData migration — VersionedSchema from Phase 1, lightweight vs SchemaMigrationPlan
A16  currentVersion relationship — @Relationship replaces UUID pointer, referential integrity
A17  CleanupService trigger — BGTaskScheduler primary + scenePhase fallback
A18  Recipe limit scope — Phase 1 device-level, Phase 2 account-level TBD [borderline]
```

## Individual ADR File Format

```javascript
# [ID] — [Title]
Status: Accepted | Superseded by [ID] | Deprecated
Context: [why this decision was needed — 1-3 sentences]
Options: [alternatives considered — brief]
Decision: [what was chosen]
Rationale: [why this over the alternatives]
Consequences: [risks, follow-up required, phase notes]
```

Target length: 10–20 lines per file. No decorative formatting. Code snippets only if essential.

## Content Disposition

| Category | Count | Destination | Status |
| --- | --- | --- | --- |
| Clean ADRs | ~16–18 | docs/decisions/ A1–A18 | This PoC |
| Borderline (A5, A18) | 2 | docs/decisions/ or delete — owner decides | This PoC |
| [CONVENTIONS.md](http://conventions.md/) content | 4 | [CONVENTIONS.md](http://conventions.md/) | Already noted in Documentation Modernization PoC |
| DATA_[MODEL.md](http://model.md/) content | ~7 | DATA_[MODEL.md](http://model.md/) | Already noted in Documentation Modernization PoC |
| [CLAUDE.md](http://claude.md/) content | 1 | [CLAUDE.md](http://claude.md/) critical rules | Already noted in Documentation Modernization PoC |
| Trivial — delete | ~14 | Deleted | This PoC |

**Trivial entries to delete:** field notes with no architectural rationale (lastCookedAt, shareToken, importHash, currentTags, CookingSession skeleton), UI micro-decisions (swipe-to-delete, bullet format, drag constraints, step numbering, tips order, auto-bold, exit confirmation, save button behavior), JSON blob monitor note (no change decision).

**Old **[**DECISIONS.md**](http://decisions.md/)** numbering is dropped entirely.** New A1–A18 is the only numbering going forward.

## Maintenance Model

Maintenance rules (flag format, who proposes, when flags are executed) are defined in the doc-maintenance skill — not here. See: [[Doc Maintenance Skill PoC — doc-maintenance.md]]

[**INDEX.md**](http://index.md/)** update:** owner adds one line to [INDEX.md](http://index.md/) when a new ADR file is created.

## Execution Order

```javascript
1. Create docs/decisions/ folder
2. Create INDEX.md (stub, ~5 lines)
3. Migrate content going to CONVENTIONS.md / DATA_MODEL.md / CLAUDE.md (per Documentation Modernization PoC)
4. Write individual ADR files A1–A18 from remaining DECISIONS.md content
5. Fill INDEX.md with all A1–A18 entries
6. Delete trivial entries (they are simply not carried over)
7. Delete old docs/DECISIONS.md
```

Steps 3–7 happen in one session after Documentation Modernization is complete — not before.

## Recommendations

### Do now

- No file changes yet — this is a design PoC only
- Decide on borderline entries A5 (content moderation deferred) and A18 (recipe limit scope) — keep or delete

### Defer

- Actual file creation — after Documentation Modernization PoC execution is complete
- ADR file slug naming convention — decide at creation time (e.g. `a01-recipe-counter-storage.md`)

### Discard

- Old numbering (A1–A25, N2, N4, D2, D9, R1–R10, S1–S7) — entirely replaced by new A1–A18
- Keeping [DECISIONS.md](http://decisions.md/) as a living document — individual files replace it

## Descoped

- [ARCHITECTURE.md](http://architecture.md/) ADR content migration — tracked in Documentation Modernization PoC
- ADR tooling (adr-tools, etc.) — plain files are sufficient at this scale
- Retroactive ADRs for Phase 2+ decisions — written when those phases begin

## References

- Documentation Modernization PoC: [[Documentation Modernization PoC — CLAUDE.md + CONVENTIONS + DATA_MODEL + ARCHITECTURE]]
- Doc Maintenance Skill PoC: [[Doc Maintenance Skill PoC — doc-maintenance.md]]
- Current [DECISIONS.md](http://decisions.md/): `/Users/kovacsmark/Documents/RecipeAPP/Foodoire/docs/DECISIONS.md` (513 lines, frozen)