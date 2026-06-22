---
up: "[[v1.5]]"
group: "Generic warehouse-usage.md inaccurate-ref fixes (SAW-48)"
order: 16/16
tags: [group]
---

# Group 16 — Generic `warehouse-usage.md` inaccurate-ref fixes (SAW-48)

## Brief
GROUP: Generic warehouse-usage.md inaccurate-ref fixes (SAW-48)
ORDER: 16/16
REPO: SPQR
RUN_CONTAINER: /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5
RUN_DOC:       /Users/kovacsmark/Documents/GitHub/SPQR-Agentic-Workflow/docs/spqr_self/upgrades/v1.5/16-warehouse-usage-ref-fixes.md
RATIONALE: Two byte-identical generic-source doc defects spotted in the SAW-47 (v1.3→v1.5) Foodoire propagation; one-way rule → fix in the generic, reaches projects on next bring-current. Reference-only file, no runtime/enforcement path affected.
SOURCE_OF_TRUTH: SAW-48 ticket (https://app.notion.com/p/38768d5de1e8815580cce7554c5f808e). No PoC — the ticket carries the exact diffs and rationale; no open decision to deliberate (owner-confirmed, roundtable + decision-making dropped per owner; PoC not justified).
FILL_CHANGES_MADE: yes
EXECUTION: master-inline (owner-authorized 2026-06-22 at the SCOPE GATE — fully-specified 2-line doc fix; a fresh-context execution agent adds no validation value here). The standing "never edit product files directly" rule was crossed on explicit owner consent.
PRE_FLIGHT:
  - SAW-48 ticket
  - docs/skills/warehouse-usage.md (target)
  - docs/CONFIGURE.md §1 (confirms SAW-46 reconciliation landed → the "pending" note is stale)
  - warehouse_robot/docs/ (confirms real filenames: QUERY_PROTOCOL.md, WRITE_PROTOCOL.md, AUDIT_PROTOCOL.md, NODE_FORMAT.md)
FILES:
  - docs/skills/warehouse-usage.md:8 — Item 1: the shorthand `{QUERY,WRITE,AUDIT,NODE_FORMAT}_PROTOCOL.md` brace-expands to a non-existent `NODE_FORMAT_PROTOCOL.md`. Real file is `NODE_FORMAT.md` (no `_PROTOCOL`). Replace with an accurate form.
  - docs/skills/warehouse-usage.md:15–18 — Item 2: (a) delete the stale "(Catalogue note: … pending CONFIGURE.md token-catalogue reconciliation … to be added before first propagation …)" parenthetical — that reconciliation is DONE (SAW-46, group 15: both tokens now in CONFIGURE.md §1). (b) rephrase the lead sentence so it no longer embeds `[WAREHOUSE_ROOT]`/`[ANTECHAMBER_ROOT]` as value-slots in prose (on instantiation `[WAREHOUSE_ROOT]` substituted into a sentence about itself; empty optional `[ANTECHAMBER_ROOT]` yielded broken inline-code — both observed live in the SAW-47 Foodoire copy).
  - docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md:15 — optional (AC #4): same NODE_FORMAT shorthand in the generic-only PoC "Sources:" line (not propagated; fixed for consistency).

SCOPE GUARD:
  - Generic-only. Do NOT edit the Foodoire copy (`/Users/kovacsmark/Documents/RecipeAPP/Foodoire/docs/skills/warehouse-usage.md`) — that is drift; the fix reaches Foodoire via the next bring-current propagation (one-way rule).
  - Touch ONLY warehouse-usage.md lines 8 + 15–18 and the SAW-31 PoC line 15. Leave the legitimate `--warehouse-root [WAREHOUSE_ROOT]` value-slots in the §2 command examples intact.
  - Do not commit.

## Changes Made

Two files edited: `docs/skills/warehouse-usage.md` (propagate-surface skill) and `docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md` (generic-only master record). Foodoire copy untouched. Not committed.

### `docs/skills/warehouse-usage.md`
- **Item 1 — line 8.** `` (`warehouse_robot/docs/{QUERY,WRITE,AUDIT,NODE_FORMAT}_PROTOCOL.md`) `` → `` (`warehouse_robot/docs/{QUERY,WRITE,AUDIT}_PROTOCOL.md` + `NODE_FORMAT.md`) ``. The brace now expands only to the three real `*_PROTOCOL.md` files; `NODE_FORMAT.md` is cited separately by its real name. No `NODE_FORMAT_PROTOCOL.md` is implied.
- **Item 2 — lines 15–18.** Deleted the stale "(Catalogue note: `[WAREHOUSE_ROOT]` rides the pending CONFIGURE.md token-catalogue reconciliation — Group-9 discovery F1 — to be added before first propagation; it is not re-discovered here.)" parenthetical (false since SAW-46/group 15 catalogued both tokens in CONFIGURE.md §1). Rephrased the lead sentence to refer to the paths by concept rather than embedding the bracket tokens as value-slots:
  > The warehouse and antechamber root paths are set in `CONFIGURE.md` §1; the antechamber root is optional and, when unset, the robot defaults to an `antechamber` sibling of the warehouse root (A3).
  No `[WAREHOUSE_ROOT]`/`[ANTECHAMBER_ROOT]` token now appears in descriptive prose, so on instantiation nothing substitutes into a sentence about itself and the empty optional token can no longer yield broken inline-code. The `--warehouse-root [WAREHOUSE_ROOT]` slots in the §2 command examples (legitimate command templates) were left untouched.

### `docs/spqr_self/poc/SAW-31 Warehouse Cutover — PoC.md`
- **Line 15 (AC #4, optional).** Same NODE_FORMAT shorthand in the "Sources:" line corrected: `{QUERY,WRITE,AUDIT,NODE_FORMAT}_PROTOCOL.md` → `{QUERY,WRITE,AUDIT}_PROTOCOL.md` + `NODE_FORMAT.md`. Generic-only PoC, not on the propagation surface — fixed for consistency only.

### Verification (verbatim)

```
=== AC1 — no NODE_FORMAT_PROTOCOL implied; brace residue gone (expect exit 1 = 0 hits) ===
grep -rn "NODE_FORMAT}_PROTOCOL" docs/   → exit=1 (no hits)
warehouse-usage.md:8 → (`warehouse_robot/docs/{QUERY,WRITE,AUDIT}_PROTOCOL.md` + `NODE_FORMAT.md`)

=== AC2 — stale "pending CONFIGURE reconciliation" note gone (expect exit 1 = 0 hits) ===
grep -n "pending CONFIGURE\|token-catalogue reconciliation\|Catalogue note" warehouse-usage.md → exit=1 (no hits)

=== AC3 — no config token as value-slot in prose (lines 15-17) ===
"The warehouse and antechamber root paths are set in `CONFIGURE.md` §1; the
 antechamber root is optional and, when unset, the robot defaults to an
 `antechamber` sibling of the warehouse root (A3)."   → no bracket token present

=== AC4 — SAW-31 PoC line 15 ===
warehouse_robot/docs/{QUERY,WRITE,AUDIT}_PROTOCOL.md` + `NODE_FORMAT.md`
```

**Result:** all four acceptance criteria satisfied. AC1 — the four robot-doc files are referenced accurately, no `NODE_FORMAT_PROTOCOL.md` implied (and the residue grep is clean repo-wide). AC2 — the stale "pending reconciliation" note is removed. AC3 — no `[WAREHOUSE_ROOT]`/`[ANTECHAMBER_ROOT]` is embedded as a value-slot in descriptive prose. AC4 — the same shorthand is corrected in the SAW-31 PoC. The fix lands in the generic only; it reaches consuming projects on the next bring-current propagation — no manual downstream edit (the Foodoire copy was deliberately not touched).

### Out-of-scope / open items
- No new out-of-scope discoveries during execution. The two defects were exactly as the ticket described; both confirmed live in the SAW-47 Foodoire copy before the fix.
