# Write protocol — the warehouse write gate (B4)

The write gate is the **only legal way knowledge enters** the warehouse. It is
a two-stage path: a cheap deterministic robot **hard-gate** (well-formedness),
then escalation to the **Senate** (semantic judgment) only when needed. This
document is the agent-facing contract; it travels with the package at import
(sibling of `NODE_FORMAT.md` / `QUERY_PROTOCOL.md`).

## Proposal file format

A proposal is a candidate node **without identity**. It is the node frontmatter
(`NODE_FORMAT.md`) **minus the three robot-stamped keys** — `id`, `timestamp`,
`schema_version` — which the gate stamps at ingest. Setting any of them in a
proposal is a structural error (the proposer must not mint an id — A15).

```
---
kind: decision
status: active
title: Adopt event sourcing for the ledger
scope: ledger
origin: decided
ticket: SAW-30
agent: Praetor
edges:
  - type: derived-from
    target: demo-n1
---

<body prose>
```

Canonical key order (optional keys omitted, never empty):
`kind · status · title · scope · verdict · flag_type · origin · ticket · agent · source`,
then the `edges:` block. The plane is derived from `kind` (`flag` → audit
plane `f`, otherwise knowledge plane `n`).

## Hard-schema gate (no Senate cost)

A proposal is rejected as **`rejected-malformed`** (persisted, never costs a
Senate call) if it fails any of:

- **required spine:** `kind`, `status`, `title`, `origin`;
- **node-format validity** (reused from the codec): scalar subset, `status` ∈
  {active, retired} (`superseded` is derived, never written), `origin` enum,
  `verdict` only on a lesson, `flag_type`/`scope` slugs, known edge types,
  non-empty body;
- **per-kind required fields (S3):** decision → `scope`; constraint → `source`;
  lesson → `agent` + `ticket`;
- **per-edge source-kind (S3):** `supersedes`/`derived-from` only from a
  decision; `constrains` only from a constraint; `about` only from a lesson;
  `flags` only from a flag; `relates-to` and `resolves` from any node.

A file that is not even proposal-shaped (bad fence, unknown/out-of-order key, a
robot-stamped key present) is **raised at the door** (`MalformedProposal`, CLI
exit 2) and **never persisted** — distinct from `rejected-malformed`.

## State machine

```
proposed --[hard-gate]--> rejected-malformed
                      \-> validated --[pre-check + escalation]-->
                              auto-ingested            (promoted class; empty policy now)
                              pending-senate --[resolve verdict]-->
                                     ingested | rejected | revise
```

- **`auto-ingested`** is reachable but its promotion policy is empty (Cluster C
  / SAW-31); every validated proposal escalates to `pending-senate` today.
- **`revise`** is not a stored state: the proposal re-enters at `proposed`
  (awaiting a resubmit via `revise`). Bounded to N rounds (placeholder dial,
  default 3); at the bound, `resolve … revise` raises an owner escalation.
- **`retire`** is not an operation: there is no in-place mutation. A born-retired
  node is ingested with `status: retired`; retiring live knowledge means
  ingesting a **new superseding node** (A15).

## ID allocation (the robot's monopoly)

At ingest only, inside the serialized gate, the node id is **burned from
`id_counter`** (never markdown-max, A15) in its own committed transaction —
then the markdown is written (truth first), then folded. A crash after the burn
leaves a **gap**, never a collision (S7: unique, not gapless). Proposal keys
(`<prefix>-p<n>`) are a separate namespace, derived from the antechamber dir.

## Antechamber (outside the warehouse — G6/A3)

```
project_memory/
├── warehouse/      ← canonical nodes (truth) + derived index (gitignored)
└── antechamber/    ← proposals: <key>.md (+ .rN.md revisions), <key>.state.json
```

- **Content** files are **append-only** (a revision is a new `<key>.rN.md`).
- The **`<key>.state.json` sidecar** holds the mutable lifecycle (state,
  node_id, round, timestamps). The antechamber is a *queue*, not canonical
  knowledge — only the sidecar is mutable.
- The SQLite **`antechamber` table is a disposable mirror**, excluded from the
  A8 digest and re-derivable from the dir via `reconcile-antechamber`. The
  proposals therefore survive an index rebuild **and** an index loss (L4/R3).

## CLI

```
propose  --warehouse-root P [--antechamber-root P] --ticket T --agent A --file F|-
revise   --warehouse-root P [--antechamber-root P] --proposal-key K --file F|-
resolve  --warehouse-root P [--antechamber-root P] --proposal-key K --verdict ingested|rejected|revise
reconcile-antechamber --warehouse-root P [--antechamber-root P]
check    --warehouse-root P [--antechamber-root P]   # now also reports the antechamber
```

`--ticket`/`--agent` on `propose` are the self-declared submitter **binding**
(the revise-wake handle, L5) — distinct from the node's provenance fields.
JSON on stdout. Exit codes: **0** accepted (validated/pending/auto/ingested) ·
**1** recorded rejection (`rejected-malformed`/`rejected`) or revise-limit
escalation (packet on stdout) · **2** robot error (structural / protocol).

Who issues the verdict — the **Senate wake** — is SAW-31, not the gate. The
robot writes files; it never runs git (G3).
