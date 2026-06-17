# Upgrading SPQR

When gaps surface in the workflow — through Censura retrospectives, spike findings, or operational experience — use the structured upgrade process to apply changes consistently across all files.

## How to start

Load `docs/upgrade/session-starter.md` into a new Claude Code session. Fill in the PERSONAS section with your team's names before running.

## What it covers

The upgrade process runs in six phases: context loading, roundtable, decision making, planning, execution, and wrap-up. Each phase is defined in the skill files under `docs/upgrade/`.

## Where the work is recorded

Each upgrade run is recorded in the repo (not Notion) as a run container under `docs/spqr_self/upgrades/<version>/` — a MAIN folder-note plus one ordered sub-md per execution group, created from the templates in `docs/spqr_self/templates/`. Ticketing stays in Notion (SAW tickets); only the work record is repo-native.

## Propagating a release to a consuming project

Upgrades change the generic SPQR (this repo) — the source of truth. Content flows one way, generic→project: once a new generic version is released, a consuming project is brought current by the **propagation agent** (`docs/upgrade/propagation-agent.md`), which writes the manifest-defined core surface into that project at the target version. The propagation boundary — which paths propagate, stay generic-only, are consumed once at init, or are project-owned — is declared in `docs/upgrade/propagation-manifest.md`. Each consuming project carries its own `spqr.config` (token values + version stamp), created at first instantiation from `spqr.config.template`. Project insight travels back up only as a SAW ticket, never as an automatic content sync.
