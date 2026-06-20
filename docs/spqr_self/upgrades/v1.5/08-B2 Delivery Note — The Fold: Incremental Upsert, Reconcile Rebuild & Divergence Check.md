---
up: "[[v1.5]]"
group: "Warehouse Initiation — build (B1–B5)"
order: 8/8
saw: [SAW-30]
ticket: B2
status: green
tags: [group, warehouse, delivery]
---

## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Warehouse Initiation Project — B2 delivery note

**Ticket scope:** The fold: incremental upsert + reconcile rebuild + divergence check. Markdown is truth; the index is derived and disposable.

**Date:** 2026-06-13

**Usage:** claude-fable-5:  4.8k input, 63.5k output, 3.7m cache read, 171.0k cache write ($10.30)

**Session ID**: d4a7f782-d457-42d7-9e5a-1dfea91b6f65

**Dependency gate at session start:** B1 delivery note present with exit status GREEN (65/65 tests). PASS.

---

# 1. Scope delivered

All B2 scope items live in the existing **`warehouse_robot/`** package:

| Item | Where it lives |
|---|---|
| Incremental upsert (hot path): node row + edges + manual FTS5 sync in a single write transaction; idempotent; maintains the id_counter invariant (`next_value >= max+1` per plane) | `warehouse_robot/fold.py` — `upsert_node`, `upsert_node_file` (library API only, no CLI — see section 2) |
| Reconcile rebuild (cold path): fresh index from markdown in deterministic order (nodes by plane+number, edges sorted), counter re-derived as markdown max+1 per plane (S7), `meta.created_at` + `trace` + `antechamber` rows carried over verbatim (A8), WAL checkpoint, atomic swap via rename; `fresh=True` recovery escape hatch for a corrupt previous index | `warehouse_robot/fold.py` — `rebuild`, `CarryOver`, `RebuildResult` |
| Canonical logical digest (A8 part 2): ordered dump-hash of `meta`, `nodes`, `edges`, `id_counter` + FTS5 integrity check | `warehouse_robot/fold.py` — `logical_digest`, `logical_digest_of` |
| Divergence check (cheap, per-file): missing-in-index / missing-in-markdown / hash-mismatch / misplaced / unreadable / counter-behind / FTS-corrupt / index-missing | `warehouse_robot/fold.py` — `check`, `DivergenceReport` |
| CLI: `check` (exit 0 clean / 1 divergent) and `reconcile [--fresh]` (prints counts + logical digest) | `warehouse_robot/cli.py` |
| Test suite: 30 new tests (upsert, rebuild determinism, digest equivalence, divergence scenarios, CLI) | `warehouse_robot/tests/test_fold.py`, `test_reconcile.py`, `_fold_helpers.py` |

Small extensions to B1 modules, both in service of B2: `errors.py` gained `FoldError`; `schema.create_index` gained an optional `created_at` parameter (the carry-over seam the A8 determinism criterion requires).

# 2. Decisions made in-session

| Decision | Rationale | Authority |
|---|---|---|
| **A8 amendment written** (Planning Decisions): the Phase 1 "byte-identical" exit criterion is a two-part check — (1) rebuild determinism: two rebuilds from the same markdown tree are byte-identical; (2) live-vs-rebuild equivalence via the canonical logical digest. A literal whole-file byte comparison between the live and rebuilt index is impossible by construction (trace/antechamber rows, created_at, insertion-order-dependent page layout) | Surfaced as a planning-phase contradiction (anticipated by B1 open question #4) | Owner-approved |
| Starter B verification task 3 updated to match A8, including the same-Python/SQLite-build environmental constraint — the record stays self-consistent | Owner instruction with the A8 approval | Owner-approved |
| `trace` + `antechamber` rows carried over verbatim on rebuild, in deterministic order; if the index file is lost, the trace is lost with it (accepted cost) | They are not derivable from warehouse markdown; the trace is the S7 measurement proxy | Owner-approved |
| Incremental upsert is **library API only** — no CLI command. The production caller is the B4 serializing gate | A public fold command would open a gate-bypassing write path | Owner-approved |
| The fold mirrors a hand-edited file as-is (markdown is truth); detecting append-only violations is the job of `check` and the B5 audit, not the fold | The fold is a mechanism, not a gate | Owner-approved |
| Reconcile-trigger wiring ("at boot / periodically", S7) handed to B3 — B2 ships explicit `check`/`reconcile` commands only | The robot is per-call (G1); the natural hook is the query path, which is B3's surface | Owner-approved (see section 6) |
| `--fresh` flag on `reconcile`: rebuilds without carry-over when the previous index is unreadable | The recovery path must work precisely when the old index cannot be read; the error message points at it | Agent judgment (mechanism for the owner-approved carry-over decision) |
| Upsert advances `id_counter` to `max(next_value, number+1)` | A fold of pre-existing files (reconcile, tests) must not leave the counter behind the markdown; harmless when the B4 gate pre-allocates | Agent judgment |
| `logical_digest` commits after the FTS5 integrity check | The check is INSERT-shaped, so python sqlite3 opens an implicit transaction; left open it blocks the WAL checkpoint and would break byte-determinism | Agent judgment (found while building) |
| Rebuild deletes a stale `index.sqlite.rebuild` leftover before starting | A crashed rebuild must not poison the next one | Agent judgment |

# 3. Deviations from the Execution Plan / Planning Decisions

- The Execution Plan's literal exit-check wording ("reconcile rebuild reproduces the index byte-identically") is **redefined by amendment A8** (owner-approved, recorded in Planning Decisions + Starter B). This is a record change, not a silent deviation.
- **Post-close validation finding and fix (2026-06-13):** the first GREEN shipped a ~10%-flaky A8 hard criterion. Building the tmp index in WAL mode and finishing with `PRAGMA wal_checkpoint(TRUNCATE)` left the SQLite header file-change-counter (offsets 24–27, mirrored at 92–95) non-deterministic — WAL checkpoint bookkeeping sometimes bumped it twice. Fix per owner instruction: the rebuild now builds its tmp index in **rollback-journal mode** and switches to `journal_mode=WAL` as the single, deterministic final canonicalization step before close+rename (`schema.create_index` gained a `wal=` parameter). A8 was **not** weakened — header bytes stay inside the comparison; the system was fixed to meet the criterion as written. Both byte-comparison tests now loop ≥5 rebuilds so this flake class cannot ship green again.
- No other deviations.

# 4. Test evidence

- Final verification after the flake fix (section 3): **full suite run 10×, 95/95 tests, 0 failures, 0 errors on every run**, Python 3.9.6 (macOS system interpreter), 2026-06-13. Each run includes two 5-iteration byte-comparison loops (with and without carried operational rows), so the 10× verification covers 100+ rebuild byte comparisons.
- Re-run from the repo root: `python3 -m unittest discover -s warehouse_robot/tests -t .`
- All tests build disposable instances under the system tmp directory and delete them (A4); no test artifact is visible to git (`git status` shows only the intended deliverables).
- A8 criteria proven in-suite: ≥5 consecutive rebuilds byte-identical (SHA-256 of the index file, with and without carried trace/antechamber rows); live-vs-rebuild logical digest equal despite deliberately different insertion orders (fixtures fold in sorted-glob order, rebuild in plane+number order).
- CLI smoke tests (disposable tmp instances, deleted afterwards): `init` → copy fixtures → `check` correctly reported 14 missing index rows + both counters behind (exit 1) → `reconcile` folded 14 nodes / 12 edges → final `check` clean (exit 0). After the flake fix: 6 consecutive reconciles byte-identical, and the swapped-in index confirmed to be in `journal_mode=wal`.
- One test fixed during the session: an over-strong assertion (expecting a fresh `created_at` to *differ* at second resolution) — the assertion was wrong, not the code; replaced with the correct recovery assertions.
- Honest record: the original close declared GREEN on a single double-rebuild comparison, which passed by luck at a ~10% flake rate; the validation finding, root cause, and fix are in section 3.

# 5. Flagged out-of-scope findings (not built — Law 1 scope fence)

- **Reconcile picks up hand-placed node files.** Any canonical file someone drops into `nodes/`/`flags/` is folded by `rebuild` — the fold cannot distinguish it from gate-written content. Detecting hand-minted artifacts is the job of `check` (hash/counter divergence) and the **B5** audit; the interim "never hand-mint warehouse artifacts" rule remains a process rule, not a fold-enforced one.
- **Non-`.md` stray files in `nodes/`/`flags/` are invisible** to both fold and check (only `*.md` is scanned). A B5 tripwire candidate.
- **`check` and `reconcile` are manual commands.** Nothing triggers them automatically yet — wiring the cheap divergence check into the query path is B3's surface (see section 6); a scheduled reconcile remains in the parked lane.
- The B1 finding stands: the fixture query set is still to be authored in **B3** against the real verbs.

# 6. Open questions for the next ticket (B3 — query interface)

1. **Divergence-check-on-open:** should every query verb (or just `open_scope`) run the cheap `check` first and warn/refuse on divergence? Recommendation: run it once per CLI invocation, warn on stderr, do not refuse (queries against a slightly stale index are degraded, not dangerous; refusal would block reads during the crash window the reconcile exists to heal).
2. **Trace writing:** the `trace` table is in place and survives reconcile (A8 carry-over); B3 writes the intent/verdict bracket rows. `fold.logical_digest` deliberately excludes `trace`/`antechamber` — B3 must not add operational tables to the digest.
3. **FTS5 query surface:** `find` should reuse the external-content `nodes_fts` table as-is (BM25 ranking, title+body). The fold guarantees its sync; B3 should not write to it.
4. **Fixture query set (A4):** author it in B3 against the real verb signatures, as flagged in B1.

# 7. Exit status

**GREEN** — full B2 scope delivered; A8 amendment + Starter B kept the record self-consistent; 95/95 tests green against disposable instances; byte-determinism and live-vs-rebuild equivalence both proven in-suite and in a CLI smoke test.
