---
name: warehouse-ingest
description: The proposer contract (S8) — how an authoring agent submits new knowledge to the warehouse antechamber via the write gate. Proposal format, read-before-propose, the propose/revise CLI, antechamber discipline.
---

PURPOSE
The write gate is the ONLY legal way knowledge enters the warehouse. You do not
write node files and you never mint an id — you author a **proposal**, submit it
with `propose`, the robot **hard-gates** it (deterministic well-formedness), it
queues in the **antechamber**, the **Senate** makes the semantic judgment and
executes `resolve` on owner HITL (owner consents, the Senate runs it). This skill
is the agent-facing contract.
Enforcement authority is `warehouse_robot/docs/WRITE_PROTOCOL.md` +
`warehouse_robot/docs/NODE_FORMAT.md` — this file is usage instruction.

WHO LOADS THIS
Authoring agents with a propose right: Praetor (execute), Quaestor (synthesize),
and the Senate's Censura (lesson-node proposals, D2c). Probator also loads this for
its ONE narrow authoring act — the CORRECTIO close lesson (D2c extension;
scrutinize-on-read ⊥ a narrow propose right). Among the scrutinize agents Probator
is the sole exception; Tribunus and Curator read but do not author. Read-before-propose
is mandatory for every proposer.

MANDATORY READ-BEFORE-PROPOSE (S6 three-layer dup defense)
Before every `propose`, run a query round against the warehouse to check the
assertion is not already present: a `find --text "…"` and/or
`open-scope --scope <scope>` round (see the WAREHOUSE QUERY POLICY block in your
agent file — same `--archetype`/`--session`/`--intent` bracket, closed with a
`verdict`). If the assertion already exists, do NOT re-propose; if it CONTRADICTS
an active node, author a superseding decision (a new node that `supersedes` the
old one), never an in-place edit — the store is append-only.

PROPOSAL FILE FORMAT
A proposal is a candidate node **without identity**: the NODE_FORMAT frontmatter
**minus the three robot-stamped keys** `id` / `timestamp` / `schema_version`.
Setting any of those (or hand-minting an id) is a structural error (A15). One
proposal = **one atomic assertion** (one decision / constraint / lesson) — split
compound findings into separate proposals.

Canonical key order (optional keys omitted, never written empty), `edges:` last:
`kind · status · title · scope · verdict · flag_type · origin · ticket · agent · source`

```
---
kind: decision
status: active
title: Adopt event sourcing for the ledger
scope: ledger
origin: decided
ticket: <TICKET-ID>
agent: Praetor
edges:
  - type: derived-from
    target: <node-id>
---

<body prose — the rationale / frozen context; non-empty, ends with a newline>
```

PER-KIND REQUIRED FIELDS (hard-gate; malformed bounces, no Senate cost)
- `decision`   → requires `scope`
- `constraint` → requires `source`
- `lesson`     → requires `agent` + `ticket`; `verdict` (GREEN/YELLOW/RED) allowed only here
- spine on every kind: `kind`, `status` (`active`/`retired` — `superseded` is derived, never written), `title`, `origin` (`decided`/`inherited`/`observed`), non-empty body.

PER-EDGE SOURCE-KIND (hard-gate)
- `supersedes` / `derived-from` — only from a **decision**
- `constrains` — only from a **constraint**
- `about` — only from a **lesson** (the recommended edge for a lesson: lesson → about)
- `relates-to` / `resolves` — from any node
Edge targets are existing node ids; edges are directed and live on the source.

CLI
```
propose --warehouse-root [WAREHOUSE_ROOT] --ticket <TICKET-ID> --agent <Agent> --file <proposal.md>|-
revise  --warehouse-root [WAREHOUSE_ROOT] --proposal-key <key> --file <revised.md>|-
```
- `--ticket`/`--agent` on `propose` are the self-declared submitter **binding**
  (the revise-wake handle) — distinct from the node's own provenance fields.
- `revise` resubmits content the Senate sent back; the proposal re-enters at
  `proposed` (bounded rounds; at the bound `resolve … revise` escalates to the
  owner). A revision is a **new** `<key>.rN.md` — content is append-only.
- JSON on stdout. Exit codes: **0** accepted (validated/pending/auto/ingested) ·
  **1** recorded rejection (`rejected-malformed` / `rejected`) or revise-limit
  escalation (packet on stdout) · **2** robot error (structural / protocol — e.g.
  a robot-stamped key present, bad fence, out-of-order key).

ANTECHAMBER DISCIPLINE
- Proposals live in `antechamber/` **outside** the warehouse: `<key>.md`
  (+ `.rN.md` revisions) are **append-only content**; the mutable lifecycle lives
  only in the `<key>.state.json` sidecar (state / node_id / round). The
  antechamber is a queue, not canonical knowledge.
- After `propose`, knowledge does NOT exist in the warehouse yet — it is
  `pending-senate`. The id is burned and the markdown written only when the Senate
  runs `resolve … ingested` on owner HITL. Do not assume your proposal is live; do not query for
  it as an active node until the ingest lands.

WHAT YOU NEVER DO
- Never mint an id / set `timestamp` / `schema_version`.
- Never run `resolve` or `grant` — those are privileged writes the Senate executes
  on explicit owner HITL (D2).
- Never edit or overwrite an existing proposal file — revise adds a new `.rN.md`.

RECEIPT (SAW-26 discipline)
Log the propose action + the gate verdict (the `propose` CLI stdout line: state +
proposal key) into your handover receipt — the immutable, within-pipeline record
that the write was attempted and how the gate ruled.
