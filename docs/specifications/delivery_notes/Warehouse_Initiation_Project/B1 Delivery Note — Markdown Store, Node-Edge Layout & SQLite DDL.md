## Metadata

**Epic:** SPQR Agentic Workflow — knowledge architecture & token optimization

**Component:** Warehouse Initiation Project — B1 delivery note

**Ticket scope:** Markdown store + node/edge layout + SQLite DDL (nodes, edges, FTS5, counter, flag plane, antechamber mirror, trace tables). Warehouse-root parameter as a hard requirement from the first line of code.

**Date:** 2026-06-12

**Dependency gate at session start:** B1 has no dependencies; no prior delivery notes existed. PASS.

---

# 1. Scope delivered

All B1 scope items are built and live in the new top-level **`warehouse_robot/`** package (owner-renamed from the proposed `warehouse/` to avoid collision with the `project_memory/warehouse/` content directory after import):

| Item | Where it lives |
|---|---|
| Per-call CLI (`init` command), warehouse-root mandatory, FTS5 runtime probe with hard fail | `warehouse_robot/cli.py`, `__main__.py` |
| Instance manifest (prefix, schema_version, governed scope vocabulary) | `warehouse_robot/config.py`, written as `warehouse.config.json` at the warehouse root |
| ID scheme (`<prefix>-<n|f><number>`, plane marker, no kind in ID) | `warehouse_robot/ids.py` |
| Markdown store: canonical frontmatter codec (strictly rejecting), node file I/O (append-only), plane-split layout (`nodes/` vs `flags/`) | `warehouse_robot/store.py` |
| Node/edge layout specification | `warehouse_robot/docs/NODE_FORMAT.md` (travels with the package at import) |
| Full SQLite DDL: `meta`, `nodes` (both planes), `edges`, `nodes_fts` (FTS5/BM25), `id_counter` (per plane), `antechamber` mirror (S6 state enum), `trace` (S4 intent/verdict bracket), plus derived-status views `v_effective_status` and `v_flag_status` | `warehouse_robot/schema.py` |
| Fixture set: 12 knowledge nodes + 2 flag nodes, `demo` prefix, covering all 3 kinds, both planes, all 7 edge types, all 3 verdicts, one derived-superseded node, one open + one resolved flag, two orphan candidates | `warehouse_robot/fixtures/nodes/`, `warehouse_robot/fixtures/flags/` |
| Test suite: 65 tests across ids/config/codec/schema/CLI/fixtures | `warehouse_robot/tests/` |

`init` creates the A3 layout: warehouse root with `nodes/`, `flags/`, manifest, instance-level `.gitignore`, derived `index.sqlite` (WAL), and the antechamber as a sibling directory by default (`--antechamber-root` override available). The repo-level `.gitignore` additionally ignores `index.sqlite*` and `__pycache__/`.

# 2. Decisions made in-session

| Decision | Rationale | Authority |
|---|---|---|
| Language/runtime: Python 3.9+, stdlib only | `sqlite3` with FTS5 built in; zero-dependency package maximises A2 plain-copy portability | Owner-approved (Q1), with the added condition: `init` probes FTS5 at runtime and hard-fails if missing — implemented and tested |
| Zero-dep canonical frontmatter codec instead of PyYAML | Schema is fixed and flat; the robot only writes its own canonical form | Owner-approved (Q2), with the added condition: strictly rejecting, never guesses — implemented; 20+ rejection tests |
| Package name `warehouse_robot/` | Avoids name collision with `project_memory/warehouse/` after import | Owner decision (Q3 rejection of `warehouse/`); agent concurred |
| `--warehouse-root` mandatory, antechamber defaults to sibling, `--antechamber-root` override | Matches ticket wording and the A3 layout simultaneously | Owner-approved (Q4) |
| Manifest `warehouse.config.json` at warehouse root; created by `init --prefix` | Per-instance identity: prefix, schema_version, governed scope vocabulary (G5), vocabulary starts empty (S5 re-derive guard) | Owner-approved (Q5) |
| **Manifest on full reset:** `init` never overwrites an initialised root (refuses, exit 2). A full reset deletes the entire warehouse root — manifest included — and re-runs `init`, which recreates the manifest from its parameters. The scope vocabulary is intentionally lost on reset: Phase 2 migration re-derives it against real content (G11/S5 mandatory guard). | Reset must stay cheap and unambiguous (Execution Plan Phase 5 reset path); a half-spared manifest would be a hidden state carrier | Owner-required recording (Q5 condition); mechanism is agent judgment |
| Flat `nodes/` layout, filename = `<id>.md`; flags physically separate in `flags/` | Scope lives in frontmatter + index; directory-encoding it is drift risk; plane separation made physical | Owner-approved (Q6 default) |
| Fixture IDs hand-assigned with `demo` prefix | The "no hand-minted IDs" interim rule guards canonical warehouses; fixtures are synthetic test assets that never enter a canonical path | Owner-approved (Q7); contradiction surfaced and closed |
| Audit-plane nodes use `kind: flag` + optional `flag_type` field | Reuses the universal-node machinery (S6) without pre-deciding B5's flag taxonomy | Agent judgment |
| `antechamber.state` enum has no `revise` state | S6: revise is not a separate state — the proposal re-enters at `proposed`; the DDL CHECK enforces this | Agent judgment (direct S6 reading) |
| Derived statuses realised as SQL views, never columns | `superseded` (S3) and `resolved` (S6) stay derived by construction | Agent judgment (S3/S6 invariant) |
| Node body stored in the `nodes` table; FTS5 as external-content table | The index is disposable, so duplication is free; gives BM25 over title+body | Owner-approved (Q8 default) |
| Append-only enforced at the store: `write_node_file` refuses to overwrite | S3: a node is never mutated after birth | Agent judgment |
| stdlib `unittest`, tests run against disposable instances under the system tmp directory | Suite travels dep-free with the package (A4); system tmp is outside git entirely | Owner-approved (Q10 default) |

# 3. Deviations from the Execution Plan / Planning Decisions

None of substance. Two notes:

- The Execution Plan's "gitignored/tmp directory" test discipline is implemented as **system tmp** (`tempfile.TemporaryDirectory`), which is outside the repository entirely — strictly stronger isolation than a gitignored in-repo directory.
- The A4 fixture definition includes a query set; the query set is **not** part of this delivery (see section 5).

# 4. Test evidence

- Final run: **65 tests, 0 failures, 0 errors** (`Ran 65 tests — OK`), Python 3.9.6 (macOS system interpreter), 2026-06-12.
- Re-run from the repo root: `python3 -m unittest discover -s warehouse_robot/tests -t .`
- Manual smoke test: `init` into a disposable tmp `project_memory/warehouse` produced the full A3 layout (nodes/, flags/, sibling antechamber/, manifest, instance .gitignore, WAL index); a second `init` on the same root was refused with exit code 2; instance deleted afterwards.
- Coverage highlights: codec round-trip is byte-identical in both directions (precondition for B2's byte-identical reconcile); 20+ strict-rejection cases (tabs, quoting, flow style, key order, duplicate keys, stored `superseded`, cross-plane field misuse); DDL CHECK constraints verified by attempted violations; derived-status views verified for superseded/retired precedence and open/resolved flags; FTS5 MATCH verified; missing-FTS5 hard-fail verified via mock; two-instance isolation verified.
- `git status` after the final run shows only the intended deliverables (`warehouse_robot/`, `.gitignore`, this note) — no test artifact is visible to git; the canonical-path rule is moot in this repo (no `project_memory/` exists here by design, A1).

# 5. Flagged out-of-scope findings (not built — Law 1 scope fence)

- **Fixture query set (A4):** fixtures currently contain nodes only. The query set must be authored in **B3** against the real verbs (`open_scope`/`find`/`fetch`/`traverse`) — building it now would guess B3's parameter surface.
- **Per-kind conditional validation** (decision→`scope`, constraint→`source`, lesson→`agent`+`ticket`) and **edge endpoint-kind rules** (e.g. `supersedes` is decision→decision) are deliberately absent from the codec — they are the **B4** hard-schema gate. The codec validates structure only. Fixtures already conform to the per-kind rules so B4 can tighten without fixture churn.
- **ID allocation logic** (consuming `id_counter` inside the serializing gate) is **B4**; B1 ships the table and seeds only.
- **Fold/FTS sync**: `nodes_fts` is created but not populated by any production path — population is the **B2** fold's job (tests sync it manually to prove the DDL).
- The macOS system Python is 3.9 — fine for everything built here, but if a future ticket wants newer stdlib features, the floor should be raised consciously, not silently.

# 6. Open questions for the next ticket (B2 — the fold)

1. **Divergence-check granularity:** count + content-hash per file vs a single tree-level hash. Per-file hashes are already stored (`nodes.content_hash`); recommendation: per-file, so reconcile can report *which* file diverged.
2. **FTS5 sync strategy at the fold:** manual insert/delete on `nodes_fts` inside the same write transaction (external-content tables do not auto-sync). The DDL assumes this.
3. **Counter rebuild rule:** on reconcile rebuild, `id_counter` must be re-derived as markdown max+1 per plane (S7) — B2 must implement this; the table seeds at 1 only on `init`.
4. **Byte-identical rebuild definition:** the exit check compares index bytes; B2 should define the comparison against a freshly folded index (deterministic insert order, e.g. ID-sorted) so WAL checkpointing noise cannot break byte-identity.

# 7. Exit status

**GREEN** — full B1 scope delivered; 65/65 fixture tests green against disposable instances; no deviation requiring owner action.
