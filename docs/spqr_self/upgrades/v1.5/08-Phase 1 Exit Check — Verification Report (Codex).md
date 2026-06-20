---
up: "[[v1.5]]"
group: "Warehouse Initiation — verification"
status: red
date: 2026-06-20
tags: [warehouse, verification]
---

# Phase 1 Exit Check — Independent Verification Report (Codex)

## Verdict

**OVERALL: RED.** The implementation behavior tested here passes all requested functional checks, including both parts of A8. Phase 1 nevertheless does not have a complete exit record: the B4 and B5 delivery notes have blank session IDs, so A10's required proof that this independent verifier session differs from every build session cannot be made. The B1–B3 notes also do not satisfy the later A11 receipt/environment format. These are evidence/governance failures, not observed runtime defects; no code fix was made.

Verification was independent: delivery-note GREEN statements were treated only as claims. All instances were created below a `tempfile.TemporaryDirectory` in the system temp directory and deleted automatically. No canonical path was used.

## Environment

Command:

```console
$ python3 -c "import sys,sqlite3; print(sys.version.split()[0], sqlite3.sqlite_version)"
3.9.6 3.51.0
```

This exactly matches the B4/B5 recorded environment, so the A8 byte comparison has no environment qualification.

## 1. Baseline suite — PASS

The requested command was run verbatim from the repository root:

```console
$ for i in 1 2 3 4 5; do python3 -m unittest discover -s warehouse_robot/tests -t . 2>&1 | tail -1; done
OK
OK
OK
OK
OK
```

Because `tail -1` suppresses the count, a separate full-output run established it:

```console
$ python3 -m unittest discover -s warehouse_robot/tests -t . 2>&1 | tail -3
Ran 241 tests in 5.819s

OK
```

Observed count: **241**. This agrees with the latest B5 claim. The elapsed time is naturally different from the note's historical receipt and is not a discrepancy.

## 2. Independent vertical slice — PASS

A custom Python script, not the project tests, initialized disposable instances, copied the versioned fixtures, and called the public package surfaces. Representative output:

```text
FOLD {"check_clean": true, "edges": 12, "nodes": 14, "schema_version": "1"}
QUERIES {"fetch": {"ids": ["demo-n1"], "verb": "fetch"}, "find": {"count": 0, "verb": "find"}, "open_scope": {"count": 1, "verb": "open_scope"}, "trace_verbs": ["open_scope", "find", "fetch", "traverse"], "traverse": {"nodes": [], "verb": "traverse"}}
QUERY_NONEMPTY {'find_ids': ['demo-n6'], 'traverse_ids': ['demo-n1']}
WRITE_STATE {"content_files": ["demo-p1.md", "demo-p1.r2.md"], "mirror": [["demo-p1", "ingested", "demo-n13"]], "node_id": "demo-n13", "round": 2, "states": ["pending-senate", "proposed", "pending-senate", "ingested"]}
```

The fold indexed all 14 standard fixtures and its divergence check was clean. Each B3 verb (`open_scope`, `find`, `fetch`, `traverse`) executed and wrote the expected trace verb. A second fresh-instance query used known matching data to prove non-empty FTS and traversal results.

The B4 state-machine walk was:

1. valid proposal → `pending-senate`;
2. Senate verdict `revise` → `proposed`;
3. revised append-only content → `pending-senate`, round 2;
4. Senate verdict `ingested` → node `demo-n13` and an `ingested` mirror row.

Both `demo-p1.md` and the append-only revision `demo-p1.r2.md` remained in the antechamber.

The B5 controls produced:

```text
AUDIT_CLEAN {"emitted": [], "open_flag_count": 0}
AUDIT_BROKEN_SURVIVAL {
  "required_all_flagged": true,
  "emitted": [
    {"flag_id":"demo-f1","flag_type":"missing-recommended-edge","target":"demo-n5"},
    {"flag_id":"demo-f2","flag_type":"orphan","target":"demo-n4"},
    {"flag_id":"demo-f3","flag_type":"relates-to-overuse","target":"demo-n6"}
  ]
}
```

Thus the clean graph emitted zero flags, while the deliberately broken graph independently triggered all three A14 predicates: orphan `demo-n4`, lesson missing `about` `demo-n5`, and six `relates-to` edges `demo-n6` (> K=5).

## 3. A8 exit criterion — PASS

The same markdown tree and carried operational state were reconciled twice. SHA-256 was calculated on each complete SQLite file:

```text
sha1 f2d746206a61ed8bd4fee3925e76fa5da37d4184ab61c44d876800a83827d3d8
sha2 f2d746206a61ed8bd4fee3925e76fa5da37d4184ab61c44d876800a83827d3d8
byte_identical true
```

Live incremental and both rebuild logical digests were:

```text
f85e517c713a718b91e7db98bcf5ad6a711c04d11372f7f96af95afa78cc5de0
```

The rebuild carried 4 trace rows and 1 antechamber row. Therefore A8(a) byte determinism and A8(b) live-vs-rebuild logical equivalence both pass under the required SQLite build.

## 4. Write-state and flag survival — PASS

After reconcile, the antechamber table was deliberately cleared to ensure the next result was a real directory re-derivation rather than carried state. `write_gate.reconcile_antechamber` rebuilt one row:

```text
ANTECHAMBER_REDERIVE {"check_clean": true, "cleared_then_rebuilt": 1, "equal": true, "rows": [["demo-p1", "ingested", "demo-n13"]]}
```

For the broken graph, audit-created flag markdown was present both before and after reconcile (`demo-f1.md`, `demo-f2.md`, `demo-f3.md`). The rebuilt database contained the same three target/type pairs. The canonical logical digest was stable:

```text
live    f493602a298418ff134d8669c6de81ade52dad854f895d5997b6c63182a10fec
rebuild f493602a298418ff134d8669c6de81ade52dad854f895d5997b6c63182a10fec
```

## 5. Negative checks — PASS

Initial and post-test `git status --short --untracked-files=all` were identical. They contained the expected pre-existing B4/B5 working-tree changes and no generated warehouse node, flag, proposal, sidecar, or index. A repository search found no `index.sqlite`, `index.sqlite-wal`, or `index.sqlite-shm` outside `.git`.

Canonical-path checks after all tests:

```text
canonical warehouse absent: project_memory/warehouse
canonical antechamber absent: project_memory/antechamber
```

Disposable initialization generated coverage for both stores:

```text
warehouse .gitignore: index.sqlite, index.sqlite-wal, index.sqlite-shm, nodes/, flags/
antechamber .gitignore: *
```

Git-invocation searches:

```console
$ rg -n '^import subprocess|^from subprocess|subprocess\.|os\.system|Popen\(|\[.?git.?\]' warehouse_robot --glob '*.py' --glob '!tests/**'
# no output
```

A broader textual search found only comments/docstrings stating that git is not run. Test modules use `subprocess` to invoke the robot CLI, but no non-test package module imports a process API or executes git. **No robot git invocation was found.**

## 6. Delivery-note cross-check

| Claim | Independent observation | Result |
|---|---|---|
| B1: 65 tests at B1 close | Historical count cannot be reproduced from the combined current tree; current tree has 241. No evidence contradicts the historical count. | Not independently reproducible now |
| B2: 95 cumulative tests and repaired A8 determinism | Current A8 byte and logical checks pass independently. | PASS |
| B3: 171 cumulative tests; four verbs, trace, budgets | Current four verbs and trace pass; current total is 241 after B4/B5 additions. | PASS behavior; historical count not reproducible now |
| B4: 215 cumulative tests | Current total is 241 after the claimed 26 B5 additions; arithmetic is consistent. | PASS consistency only |
| B5: 241 tests | Independent suite run reports 241, five requested passes all `OK`. | PASS |
| B4/B5: Python 3.9.6 / SQLite 3.51.0 | Exact independent match. | PASS |
| B4/B5: no SQLite schema change; schema version remains 1 | `config.SCHEMA_VERSION == 1`; manifest/meta report 1; `schema.py` is not modified in the working tree. | PASS |
| D6: broad gitignore is disposable-test-only | Production constant is index-only; `--disposable` adds `nodes/`, `flags/`, and sibling antechamber `*`. | PASS |
| D9: ID burn is `SELECT` + `UPDATE`, not `RETURNING` | `_burn_id` contains exactly a counter `SELECT` followed by `UPDATE`. | PASS |
| D13: `antechamber_root` is not persisted | Manifest keys are exactly project prefix, schema version, and scope vocabulary; sibling/default or CLI override is used. | PASS |
| PC1b: shared `append_node` | Both B4 `_ingest` and B5 `_emit_flag` call `write_gate.append_node`; `_burn_id` is the shared allocation site. | PASS |

### Discrepancies and contradictions

1. **B4 and B5 session IDs are blank.** Both notes contain `Session ID: _(filled by the owner from the session record)_`. A10 requires an independent verifier to assert its session ID differs from every delivery-note session ID. That assertion is impossible against two missing values. This is the reason for the overall RED verdict.
2. **B1–B3 receipts do not meet A11's final evidence format.** B1 says `Ran 65 tests — OK` inline, B2 reports “95/95” prose, and B3 reports “171 tests” prose. They do not contain a verbatim decisive stdout receipt. This is already anticipated by A11's rationale but remains an uncorrected delivery-record discrepancy.
3. **B1–B3 omit SQLite versions.** B4 explicitly acknowledges this. A11 requires SQLite alongside Python so A8 environment equivalence can be checked. B4 and B5 comply; the older notes were not backfilled.
4. **The B4/B5 notes' “no test artifact” claim is supported, but their broad `git status` phrasing must be read against an intentionally dirty working tree.** Independent before/after comparison showed no new artifact; the tree itself was not clean because B4/B5 are uncommitted as stated in the verification brief.
5. No discrepancy was found for the specifically flagged implementation deviations D6, D9, D13, or PC1b. They are present exactly as documented.

## Final disposition

The software surfaces and data invariants required by tasks 1–5 are **GREEN on this environment**. Phase 1 exit remains **RED on evidence completeness** until the owner records the B4 and B5 session IDs and resolves the A11 receipt/environment gaps (or explicitly amends the governance requirement). This report makes no fixes and schedules none.
