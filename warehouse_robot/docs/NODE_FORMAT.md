# Warehouse Node Format & Physical Layout

**Component:** warehouse_robot — canonical node file format, identity scheme, and instance layout (B1)

**Status:** Active. This spec travels with the robot package at import (A2 plain copy).

---

## 1. Instance layout

A warehouse instance is created by `python3 -m warehouse_robot init --warehouse-root PATH --prefix PREFIX`. The warehouse root is a mandatory parameter on every robot invocation; no default exists (A4).

```
<parent, e.g. project_memory/>
├── warehouse/                  ← --warehouse-root
│   ├── warehouse.config.json   ← instance manifest (versioned)
│   ├── .gitignore              ← ignores the derived index
│   ├── nodes/                  ← knowledge plane, one file per node: <id>.md
│   ├── flags/                  ← audit plane, one file per flag node: <id>.md
│   └── index.sqlite            ← derived, disposable projection (never versioned)
└── antechamber/                ← pending proposals (markdown), sibling by default (A3/G6)
```

- Markdown is the source of truth; the SQLite index is rebuildable from it at any time (S7).
- The store is append-only: the robot never overwrites an existing node file (S3).
- The node file layout is flat — `scope` lives in frontmatter and in the index, never in the directory structure.

## 2. Identity

ID form: `<project-prefix>-<plane-marker><number>` — e.g. `food-n23`, `food-f4`.

- `prefix` — per-instance, from the manifest, `[a-z][a-z0-9]*`.
- plane marker — `n` knowledge plane, `f` audit/flag plane. The marker does **not** encode the kind (S3: no kind in the ID).
- `number` — sequential per plane, allocated only by the robot gate (B4 monopoly); unique but not gapless.

The filename is always `<id>.md` and must match the frontmatter `id`.

## 3. Frontmatter grammar — the canonical subset

The codec is **strictly rejecting**: any input outside this subset raises an explicit error; the codec never guesses or repairs. The robot only writes this form, and round-trips are byte-identical (`serialize(parse(text)) == text`) — the precondition for B2's byte-identical reconcile.

A node file is exactly:

```
---
<frontmatter lines>
---
<one blank line>
<body prose, ends with newline>
```

Frontmatter lines are `key: value` scalars in **canonical key order**, with `edges:` always last:

| # | Key | Required | Constraint |
|---|---|---|---|
| 1 | `id` | yes | matches the ID grammar; equals the filename stem |
| 2 | `kind` | yes | plane `n`: `decision` / `constraint` / `lesson`; plane `f`: `flag` |
| 3 | `status` | yes | `active` / `retired` — `superseded` is **derived, never stored** (S3) |
| 4 | `title` | yes | plain scalar |
| 5 | `scope` | optional | `[a-z][a-z0-9-]*`; governed vocabulary (G5) |
| 6 | `verdict` | optional | `GREEN` / `YELLOW` / `RED`; only on `kind: lesson` (S5) |
| 7 | `flag_type` | optional | `[a-z][a-z0-9-]*`; only on the audit plane |
| 8 | `origin` | yes | `decided` / `inherited` / `observed` (S3 provenance) |
| 9 | `timestamp` | yes | `YYYY-MM-DDTHH:MM:SSZ` (UTC, ingest time) |
| 10 | `ticket` | optional | external work-item handle (S3: supersedes the dropped `run` field) |
| 11 | `agent` | optional | subject agent (S5: single-valued, the erring/deciding agent) |
| 12 | `source` | optional | provenance source for inherited constraints |
| 13 | `schema_version` | yes | positive integer (A2: stamped per node) |
| 14 | `edges` | optional | block, see below; at least one entry when present |

Scalar values: plain strings matching `[A-Za-z0-9(][A-Za-z0-9 ._:/()&+,;'?-]*`, no trailing space. No quoting, no flow style (`[...]`, `{...}`), no multi-line values, no comments, no tabs, no blank lines inside the frontmatter. Optional keys are omitted, never written empty.

The `edges:` block:

```
edges:
  - type: <edge-type>
    target: <node-id>
```

Edge types (S3 ontology + S6 audit plane): `supersedes`, `derived-from`, `constrains`, `about`, `relates-to` (knowledge), `flags`, `resolves` (audit). Edges are directed and live on the source node; there are no inverse edges — the index reads them both ways. `motivated-by` is an external reference in the body prose, never an internal edge (S3).

## 4. Derived status (never stored)

- Knowledge plane: a node with an incoming `supersedes` edge is **superseded**; `retired` (stored) wins over derived `superseded`. Realised as the `v_effective_status` view.
- Audit plane: a flag with an incoming `resolves` edge is **resolved**, otherwise **open** (S6). Realised as the `v_flag_status` view.

## 5. Example

```
---
id: demo-n7
kind: decision
status: active
title: Adopt result-based error envelopes
scope: error-handling
origin: decided
timestamp: 2026-06-05T09:30:00Z
ticket: DEMO-5
agent: Praetor
schema_version: 1
edges:
  - type: supersedes
    target: demo-n2
---

Services return a Result-based envelope; the rationale and the frozen
input snapshot live here in the body prose.
```

## 6. Out of scope for this spec (owned by later tickets)

- Per-kind conditional field requirements (decision→`scope`, constraint→`source`, lesson→`agent`+`ticket`) and edge endpoint-kind rules (e.g. `supersedes` is decision→decision) — the B4 hard-schema write gate.
- The fold (markdown → index sync) and the reconcile rebuild — B2.
- Trace emission and query verbs — B3. Flag emission — B5.
