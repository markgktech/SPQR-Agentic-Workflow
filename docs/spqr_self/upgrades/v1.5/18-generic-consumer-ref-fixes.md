---
up: "[[v1.5]]"
group: "Generic consumer-incorrect config/policy ref fixes (SAW-50)"
order: 18/18
tags: [group]
---

# Group 18 — Generic consumer-incorrect config/policy ref fixes (SAW-50)

## Brief
GROUP: Generic consumer-incorrect config/policy ref fixes (SAW-50)
ORDER: 18/18
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/18-generic-consumer-ref-fixes.md
RATIONALE: Three propagate-surface refs name generic-only init artifacts (`CONFIGURE.md`, `CLAUDE.md.template`) that are ABSENT in a consumer project. Propagate-surface files describe the consumer runtime, so they must point at the instantiated artifacts (`spqr.config`, `CLAUDE.md`) — consistent with the rest of the surface. Reference-only; no runtime/enforcement path affected. Direct sibling of SAW-48/group 16.
SOURCE_OF_TRUTH: SAW-50 ticket (https://app.notion.com/p/38768d5de1e8811c98f3e988321ae53d). No PoC — the ticket carries the exact diffs and rationale; no open decision to deliberate (owner-confirmed; roundtable + decision-making dropped per owner; PoC not justified).
FILL_CHANGES_MADE: yes
EXECUTION: master-inline (owner-authorized 2026-06-22 at the SCOPE GATE — three fully-specified single-line ref fixes; a fresh-context execution agent adds no validation value here). The standing "never edit product files directly" rule was crossed on explicit owner consent.
PRE_FLIGHT:
  - SAW-50 ticket
  - docs/skills/warehouse-usage.md:15 (target — Item 1)
  - docs/skills/git-workflow.md:12,52 (target — Items 2+3)
FILES:
  - docs/skills/warehouse-usage.md:15 — Item 1: `CONFIGURE.md` §1 → `spqr.config` (§1 drops — spqr.config is a flat key map, not a sectioned catalogue).
  - docs/skills/git-workflow.md:12 — Item 2: `CLAUDE.md.template` → `CLAUDE.md`.
  - docs/skills/git-workflow.md:52 — Item 3: `CLAUDE.md.template` → `CLAUDE.md`.

SCOPE GUARD:
  - Generic-only. Do NOT edit the Foodoire copy — that is drift; the fix reaches Foodoire via the next bring-current propagation (one-way rule, AC #4).
  - Touch ONLY the three named lines. Leave plain `CLAUDE.md` references elsewhere (already correct) and legitimate generic-only `CONFIGURE.md`/`CLAUDE.md.template` references in non-propagated docs untouched.
  - Do not commit.

## Changes Made

One real change to the propagate surface across two skill files: `docs/skills/warehouse-usage.md` and `docs/skills/git-workflow.md`. Foodoire copy untouched. Not committed.

### `docs/skills/warehouse-usage.md`
- **Item 1 — line 15.** `The warehouse and antechamber root paths are set in `​`CONFIGURE.md` §1`​`; the` → `… set in `​`spqr.config`​`; the`. The `§1` section pointer drops because `spqr.config` is a flat key map, not a sectioned catalogue. Rest of the sentence unchanged ("… the antechamber root is optional and, when unset, the robot defaults to an `antechamber` sibling of the warehouse root (A3).").

### `docs/skills/git-workflow.md`
- **Item 2 — line 12.** `owner-only commit: senate.md ("never run shell commands") + CLAUDE.md.template (git commit/push: NEVER)` → `… + CLAUDE.md (git commit/push: NEVER)`.
- **Item 3 — line 52.** `Policy home is senate.md + CLAUDE.md.template; referenced here, not duplicated.` → `Policy home is senate.md + CLAUDE.md; referenced here, not duplicated.`

### Independent completeness check (Law 4)
Before editing, grepped the whole propagate surface (`docs/skills/`) for both tokens: the only hits were exactly these 3 — no stray refs the ticket missed. The other `CONFIGURE.md`/`CLAUDE.md.template` mentions in the repo live in generic-only docs (upgrade records, init guides) where those artifacts genuinely exist, and are correctly left untouched.

### Verification (verbatim)

```
=== AC1 — no CONFIGURE.md reference remains on propagate surface (expect 0 hits) ===
grep -rn "CONFIGURE.md" docs/skills/   → exit=1 (no hits)

=== AC2 — no CLAUDE.md.template reference remains on propagate surface (expect 0 hits) ===
grep -rn "CLAUDE.md.template" docs/skills/   → exit=1 (no hits)

=== AC3 — the 3 fixed spots now name the instantiated artifacts ===
warehouse-usage.md:15 → set in `spqr.config`; the
git-workflow.md:12    → … + CLAUDE.md (git commit/push: NEVER)
git-workflow.md:52    → Policy home is senate.md + CLAUDE.md; referenced here, not duplicated.
```

**Result:** all acceptance criteria satisfied. AC1 — no `CONFIGURE.md` on the propagate surface. AC2 — no `CLAUDE.md.template` on the propagate surface; both git-workflow.md spots now reference `CLAUDE.md`, consistent with the rest of the surface. AC3 — plain `CLAUDE.md` references elsewhere left untouched. AC4 (propagation into Foodoire via the agent, no local edit) is owner-run and remains pending — the generic now carries the fix; the Foodoire copy was deliberately not touched.

### Out-of-scope / open items
- None. The three refs were exactly as the ticket described; the completeness grep found no additional propagate-surface offenders.
- AC #4 (re-sync into frozen Foodoire via the propagation agent, before unfreezing pipelines) is a downstream owner action, not part of this generic-side change.
