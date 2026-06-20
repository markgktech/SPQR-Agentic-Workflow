# Audit protocol — the warehouse audit layer (B5)

The audit layer runs **deterministic, graph-structural tripwires** over the
graph. It **only ever FLAGS** — it never mutates, fixes, or rewrites a target.
This document is the agent-facing contract; it travels with the package at
import (sibling of `NODE_FORMAT.md` / `QUERY_PROTOCOL.md` / `WRITE_PROTOCOL.md`).

This is the cheap, continuous tier of the S6 two-tier auditor. The **semantic /
contradiction audit** (owner-driven) and **code/convention freshness** (SAW-40)
are NOT part of it — the structural audit stays purely graph-shaped.

## The three tripwires (A14)

Measurable predicates; the numeric parts are **placeholder dials** calibrated
later from real data (the B3 budget-dial precedent — no real values are minted
pre-calibration).

| Tripwire | `flag_type` | Predicate |
|---|---|---|
| Orphan watch | `orphan` | an **active** knowledge node (decision/constraint/lesson) with **zero incident knowledge-plane edges**, **excluding** foundational nodes |
| relates-to overuse | `relates-to-overuse` | a node that is the **source** of **more than K** `relates-to` edges (**K = 5**, placeholder) |
| Missing recommended edge | `missing-recommended-edge` | a node whose **kind** is expected to carry an edge it lacks, per a per-kind table |

Definitions that matter:

- **Knowledge-plane edges** are the S3 typed set — `supersedes`, `derived-from`,
  `constrains`, `about`, `relates-to`. The audit-plane edges (`flags`,
  `resolves`) do **not** count as connectivity: a flag pointing at a node never
  makes it non-orphan (otherwise flagging would "heal" the very thing it flags).
- **Foundational** = `origin: inherited` — platform axioms (e.g. Apple HIG,
  Swift naming) legitimately stand alone, so they are never orphans.
- The **recommended-edge table** is seeded from Session 3 with the single
  architecture-stated rule **`lesson → about`** (strongly recommended). It grows
  **only by governance** — no invented rules.
- The audit watches the **live** graph: retired and superseded nodes are out of
  scope (a superseded node carries an inbound `supersedes` edge anyway).

## Flags — a separate, append-only audit plane

A flag is a node on the **audit plane** (id marker `f`), self-similar to the
knowledge graph but never a knowledge kind:

```
---
id: demo-f3
kind: flag
status: active
title: Orphan watch: demo-n14 has no knowledge edges
flag_type: orphan
origin: observed
timestamp: 2026-06-20T12:00:00Z
schema_version: 1
edges:
  - type: flags
    target: demo-n14
---

<why the tripwire fired>

severity: medium (placeholder fixed floor — the real frequency x damage metric
is the parked measurement lane; B5 emits structural flags only).
```

- The flag points at its target via a **`flags` edge** and **never touches the
  target** — a target node is byte-for-byte unchanged by an audit run.
- **Open/resolved is DERIVED**, never stored: a flag is `open` unless an
  incoming **`resolves` edge** points at it (`v_flag_status`) — the mirror of
  S3's "superseded is derived". **Resolution is a write-path / retro act**
  (the B4 gate / SAW-31), **not** the audit's job.
- **Multiple flags per node** are independent flag-nodes; node **"heat"** = the
  count of its open flags.
- **Severity** is a minimal **placeholder** in the body prose (a small fixed
  floor per tripwire) — never a schema column. The real `frequency × damage`
  metric is parked; B5 does not calibrate.

Flags are emitted through the **same single ID-allocation primitive** the write
gate uses (`id_counter` burn → markdown → fold), but they **do not enter the
antechamber / Senate flow**: a structural tripwire is deterministic robot
output, not a proposal needing semantic judgment.

## Idempotency (re-run safety)

A flag is keyed to **(target, flag_type)**. The audit emits a flag only when no
**open** flag of that type already targets the node, so re-running over a
standing condition is a **no-op, never a duplicate**. A *resolved* flag does
**not** block re-emission — a condition that recurs after resolution is a real,
new finding.

## CLI

```
audit --warehouse-root P
```

JSON on stdout:

```json
{
  "verb": "audit",
  "emitted":          [{"flag_id": "demo-f3", "target": "demo-n14", "flag_type": "orphan"}],
  "skipped_existing": [{"target": "demo-n11", "flag_type": "orphan"}],
  "open_flag_count":  2,
  "heat":             [{"target": "demo-n14", "open_flags": 1}, {"target": "demo-n11", "open_flags": 1}]
}
```

Exit codes (mirroring `check`): **0** clean — no open flags · **1** findings —
open flags exist · **2** robot error (e.g. no derived index — run `reconcile`
first). The audit warns on stderr if the index lags the markdown but never
refuses (a stale read is degraded, not dangerous). The robot writes files; it
never runs git (G3).
