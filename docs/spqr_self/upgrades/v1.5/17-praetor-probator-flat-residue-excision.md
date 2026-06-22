---
up: "[[v1.5]]"
group: "Praetor/Probator flat-file convention+testing residue excision (SAW-49)"
order: 17/17
tags: [group]
---

# Group 17 — Praetor/Probator flat-file convention+testing residue excision (SAW-49)

## Brief
GROUP: Praetor/Probator flat-file convention+testing residue excision (SAW-49)
ORDER: 17/17
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/17-praetor-probator-flat-residue-excision.md
RATIONALE: SAW-42 (group 13) excised the Quaestor/Senate/Curator flat-knowledge surface but left the Praetor/Probator convention+testing tokens, treated too leniently in the SAW-47 propagation as "known project-specific placeholders pending SAW-40." On owner review they are flat-file residue, not config tokens — they contradict warehouse-primary and dangle (`ios-testing.md` / `swift-patterns.md` no longer exist). Completes the v1.5 warehouse-primary transition for the execution+QA surface.
SOURCE_OF_TRUTH: SAW-49 ticket (https://app.notion.com/p/38768d5de1e88134b990fb3fe62bdedf). No PoC — the ticket carries the exact Replace/With diffs and the owner-confirmed SAW-40 design anchor; no open decision to deliberate (roundtable + decision-making dropped per owner).
FILL_CHANGES_MADE: yes
EXECUTION: master-inline (owner-authorized 2026-06-22 at the SCOPE GATE — five fully-specified single-line edits with verbatim Replace/With text; a fresh-context execution agent adds no validation value here). The standing "never edit product files directly" rule was crossed on explicit owner consent, per the group 16 (SAW-48) precedent.
PRE_FLIGHT:
  - SAW-49 ticket
  - docs/agents/praetor.md (target — STAGE SKILLS block; WAREHOUSE QUERY POLICY already present, mirror its phrasing)
  - docs/agents/probator.md (target — STAGE SKILLS block; WAREHOUSE QUERY POLICY already present)
  - docs/skills/praetor-output.md · probator-input.md · probator-output.md (targets)
  - docs/spqr_self/upgrades/v1.5/13-flat-file-residue-excision.md (SAW-42 precedent — the same warehouse-primary excision pattern; this group is its Praetor/Probator continuation)

FILES:
  - docs/agents/praetor.md:22 (Item 1) — STAGE SKILLS `Reference (on-demand): [project-skill-files] — domain patterns before writing code` → warehouse-query wording (query by scope per WAREHOUSE QUERY POLICY; no flat pattern file; empty slice = legitimate ABSENT).
  - docs/skills/praetor-output.md:3 (Item 2) — IMPLEMENTATION RULES `Pattern first: load [project-skill-files] before writing domain code.` → warehouse-query wording (empty slice = legitimate ABSENT; never fall back to a flat pattern file).
  - docs/agents/probator.md:30 (Item 3) — STAGE SKILLS `Reference (on-demand): [project-testing-guidelines]` → warehouse-query wording, combined with the general test criteria in probator-input.md (no flat testing-guidelines file).
  - docs/skills/probator-input.md:17 (Item 4) — TEST PATH MAPPING `Reference [project-testing-guidelines] — What to Test / What Not to Test — before marking paths as in-scope.` → warehouse-query wording + general criteria in this skill; no hit = legitimate ABSENT (close + flag); never fall back to a flat testing-guidelines file.
  - docs/skills/probator-output.md:10 (Item 5) — FINDINGS DECLARATION `Untestable path (per ios-testing.md scope rules) = document reason, not a finding` → `per project testing constraints from the warehouse; general judgment if ABSENT`.

SCOPE GUARD:
  - Generic-only. Do NOT edit the Foodoire copy. Foodoire is frozen; the fix reaches it via the propagation agent on the next bring-current (one-way rule), BEFORE normal Praetor/Probator pipelines are unfrozen (AC #5) — no local Foodoire edit.
  - These tokens are RETIRED, not re-homed: do NOT add `[project-skill-files]` / `[project-testing-guidelines]` to `CONFIGURE.md §1` or `spqr.config*` (AC #4 — no second convention store).
  - SAW-40 unaffected (AC #6): it later builds capture→antechamber proposal→Senate/owner accept→warehouse convention→freshness-check; it does NOT restore these files.
  - Do not commit.

## Changes Made

Five files edited, all generic SPQR surface. Text taken verbatim from the SAW-49 ticket Replace/With diffs. Master-inline (owner-authorized at the scope gate, group 16 precedent). Foodoire copy untouched. Not committed.

- **Item 1 — `docs/agents/praetor.md:22`** (STAGE SKILLS). `Reference (on-demand): [project-skill-files] — domain patterns before writing code` → `Reference (on-demand): project conventions/patterns are warehouse knowledge — query by scope per the WAREHOUSE QUERY POLICY and apply the returned conventions before writing domain code (no flat pattern file; empty slice = legitimate ABSENT).` Consistent with the WAREHOUSE QUERY POLICY block already in the file (`:37`).
- **Item 2 — `docs/skills/praetor-output.md:3`** (IMPLEMENTATION RULES). `Pattern first: load [project-skill-files] before writing domain code.` → `Pattern first: query the warehouse by scope (WAREHOUSE QUERY POLICY) and apply the returned project conventions before writing domain code — an empty slice is a legitimate ABSENT, never fall back to a flat pattern file.`
- **Item 3 — `docs/agents/probator.md:30`** (STAGE SKILLS). `Reference (on-demand): [project-testing-guidelines]` → `Reference (on-demand): project-specific testing constraints are warehouse knowledge — query by scope per the WAREHOUSE QUERY POLICY, combined with the general test criteria in probator-input.md (no flat testing-guidelines file).` Consistent with the WAREHOUSE QUERY POLICY block already in the file (`:32`).
- **Item 4 — `docs/skills/probator-input.md:17`** (TEST PATH MAPPING). `Reference [project-testing-guidelines] — What to Test / What Not to Test — before marking paths as in-scope.` → `Query the warehouse by scope (WAREHOUSE QUERY POLICY) for project-specific testing constraints and combine them with the general What to Test / What Not to Test criteria in this skill before marking paths as in-scope. No hit = legitimate ABSENT (close + flag); never fall back to a flat testing-guidelines file.`
- **Item 5 — `docs/skills/probator-output.md:10`** (FINDINGS DECLARATION criteria). `Untestable path (per ios-testing.md scope rules) = document reason, not a finding` → `Untestable path (per project testing constraints from the warehouse; general judgment if ABSENT) = document reason, not a finding`. The dangling `ios-testing.md` reference is gone.

### Verification (verbatim)

```
=== AC1 — no [project-skill-files] / [project-testing-guidelines] token in generic surface (expect exit 1 = 0 hits) ===
grep -rn '\[project-skill-files\]\|\[project-testing-guidelines\]' docs/agents/ docs/skills/   → exit=1 (no hits)

=== AC2 — no hardcoded ios-testing.md / swift-patterns.md in generic surface (expect exit 1 = 0 hits) ===
grep -rn 'ios-testing\.md\|swift-patterns\.md' docs/agents/ docs/skills/   → exit=1 (no hits)

=== AC4 — tokens NOT added to CONFIGURE.md / spqr.config (expect exit 1 = 0 hits) ===
grep -rn '\[project-skill-files\]\|\[project-testing-guidelines\]' docs/CONFIGURE.md spqr.config*   → exit=1 (no hits)

=== 5 new warehouse-query lines confirmed in place ===
praetor.md:22         → project conventions/patterns are warehouse knowledge …
praetor-output.md:3   → query the warehouse by scope (WAREHOUSE QUERY POLICY) and apply the returned project conventions …
probator.md:30        → project-specific testing constraints are warehouse knowledge …
probator-input.md:17  → Query the warehouse by scope (WAREHOUSE QUERY POLICY) for project-specific testing constraints …
probator-output.md:10 → per project testing constraints from the warehouse; general judgment if ABSENT …
```

**Result — all acceptance criteria satisfied.**
- AC1 — no `[project-skill-files]` / `[project-testing-guidelines]` token remains in the generic surface.
- AC2 — no hardcoded `ios-testing.md` / `swift-patterns.md` reference remains.
- AC3 — Praetor/Probator wording now sources conventions + testing constraints from the warehouse query (scope-based); no flat-doc fallback instruction; ABSENT handled as a legitimate verdict + flag.
- AC4 — tokens NOT added to `CONFIGURE.md §1` / `spqr.config` (retired, not re-homed).
- AC5 — change lands in the generic only; Foodoire copy not touched. Re-sync into Foodoire via the propagation agent BEFORE unfreezing normal pipelines is a separate downstream owner-run step (Foodoire frozen).
- AC6 — SAW-40 scope unaffected (capture/promotion/freshness workflow only; does not reintroduce these files).

### Out-of-scope / open items
- No new out-of-scope discoveries during execution. The five tokens were exactly as the ticket described; all five verified present before the edit and absent after.
- **Downstream (AC #5):** Foodoire bring-current propagation of this generic change is a separate owner-run step via the propagation agent — must land before normal Praetor/Probator pipelines are unfrozen, else executors hit the (now-removed) dangling references.
