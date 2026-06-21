---
type: poc
title: "Warehouse Robot Propagation"
decides: "How warehouse_robot propagates to a consuming project, and what protects already-ingested warehouse data when a future release changes the note format — SAW-44"
status: done         # draft | done
date: 2026-06-21
tags: [poc]
---

# Warehouse Robot Propagation

## Context / question

**Ticket:** SAW-44 — *Extend propagation surface to warehouse_robot + define warehouse data-migration contract.*

SAW-38 built the generic→project propagation mechanism but deliberately deferred `warehouse_robot/` ("decided at the warehouse stage, not here") because the warehouse was not built yet. It is now built (v1.5, B1–B5). This PoC settles two things, kept deliberately minimal:

1. Does `warehouse_robot/` propagate to a consuming project, and how?
2. What protects a project's already-ingested warehouse data (nodes + links) when a future release changes the warehouse note format?

Related: [[SPQR_Propagation_Mechanism_PoC]] (SAW-38). Constraint AM4 holds — the mechanism stays agent-driven (markdown instructions), **no new code**.

## Findings

- **`warehouse_robot/` is generic-owned tooling** (the warehouse engine built in v1.5), already living at the repo root. It is the program that reads/writes the warehouse; it is not project content.
- **The robot carries no per-project tokens.** Per-instance identity (`project_prefix`, `scope_vocabulary`) lives in `warehouse.config.json` at the project's warehouse root, which is project-owned. So the robot is a plain copy — no placeholder re-instantiation.
- **The project's warehouse data is off-surface and safe by construction.** Nodes and flags are append-only markdown (the robot never overwrites an existing node); the SQLite index is derived/disposable/rebuildable. Propagation writes only the core surface and never runs the robot, so the copy cannot touch a single node or link.
- **The only real risk is a deliberate, future note-format change.** Today there is one format. Incompatibility can only arise if a future SPQR version intentionally changes the node format — a rare, human-initiated event the owner controls when shipping that version. That does not justify any standing machinery (number comparisons, robot commands); a documented stop rule is sufficient and stays within AM4.

## Recommendation / decision

### D1 — `warehouse_robot/` propagates as core (CLOSED)
`warehouse_robot/` joins the `propagate` surface as a directory line in the manifest, moving with the version snapshot like the rest of the core. This **supersedes the SAW-38 deferred note** (which had it updating out-of-band "only when the robot needs a fix"); record the supersession in the manifest so the reversal is not silent. **#decision**

### D2 — Plain source copy; copy is data-safe (CLOSED)
The robot propagates as a plain file copy of its **source** (the package + `tests/`, `fixtures/`, `docs/`), not generated artifacts — never a stray `index.sqlite` or `__pycache__`. Mechanism: copy the tracked source set (e.g. `git ls-files warehouse_robot/`), a read-only step, no new code. Propagation **only copies the robot, never runs it**, and never touches the project's warehouse data (nodes/flags/`warehouse.config.json`). The copy is reversible (revert the commit). **#decision**

### D3 — Format-change stop rule (the "handbrake") (CLOSED)
A single rule added to the propagation agent's instructions, no machinery:

> If this SPQR version changes the **warehouse note format**, propagation **HALTS** at the warehouse step: it tells the owner a migration is required, does **not** migrate, and does **not** write the version stamp. Otherwise the robot copy proceeds normally.

The format-change **trigger is owner-provided at the dry-run confirmation gate** — not an artifact the agent reads autonomously (there is no machine-readable "release notes" source in the propagation mechanism, and adding one would be the kind of machinery this scope rejects). This keeps the project from being marked "current" while running a robot whose format its data does not match. The migration itself is owner-initiated and **out of scope here**. **#decision**

### Out of scope (deferred)
- The migration **engine** (the re-fold transform that converts existing nodes to a new format) — a future, owner-decided activity, not part of propagation.
- Any number-comparison / robot-reported-version machinery — explicitly rejected as overkill for a rare, human-initiated format change.

## References
- SAW-44 (Notion) — the ticket this PoC settles
- [[SPQR_Propagation_Mechanism_PoC]] — SAW-38, the propagation mechanism this extends
- `docs/upgrade/propagation-manifest.md`, `docs/upgrade/propagation-agent.md` — the two files the briefs will edit
