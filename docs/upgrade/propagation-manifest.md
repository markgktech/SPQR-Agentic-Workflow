PROPAGATION MANIFEST

PURPOSE
Declarative, directory-level classification of every generic-side path: which paths propagate to a consuming project on a bring-current update, which stay generic-only, which are consumed once at init, and which the project owns and propagation never touches. Single source of truth for the propagation boundary — read by the propagation agent (propagation-agent.md); never inferred. Versioned with the generic repo.

RULES
- Classification is by directory, not by file. A new file under a `propagate` directory flows automatically with no manifest edit. The manifest is touched only on a structural change (a new top-level area, or reclassifying an existing one).
- Non-destructive: propagation never deletes files it does not own. Within the `propagate` surface it mirrors generic (including deletions, for snapshot integrity). Outside that surface it never deletes — a project's extra files stay intact.
- The unit of propagation is a full core-version snapshot: the entire `propagate` surface is brought to one target generic version, atomically. Not selective/cherry-pick.

CLASSIFICATION

propagate (CORE — flows on every ongoing bring-current update)
- docs/agents/    — live agent definitions the project runs
- docs/skills/    — live skill files the project runs
- docs/retro/     — live retrospective workflow (carries project tokens)
- warehouse_robot/ — the generic-owned warehouse engine (SAW-44). Carries NO per-project tokens (per-instance identity lives in the project's `warehouse.config.json`), so it is a plain source copy, not a placeholder re-instantiation. Copy set = tracked source only (`git ls-files warehouse_robot/`): the package + its own `docs/`, `fixtures/`, `tests/`. NEVER the generated/derived artifacts (`index.sqlite*`, `__pycache__/`, `*.pyc`, `.pytest_cache/`). Propagation only copies the robot, never runs it.

generic-only (the upgrade machinery + the generic's own work record — never propagates)
- docs/upgrade/   — upgrade master + propagation agent + upgrade skills (this machinery stays generic; the propagation agent does not propagate itself)
- docs/spqr_self/ — the generic's own run records and templates

init-only (consumed once at first instantiation; NOT propagated on ongoing updates — the project already holds live instantiated copies)
- CLAUDE.md.template
- docs/CONFIGURE.md
- docs/LESSONS.md
- docs/UPGRADE.md
- spqr.config.template

project-owned (target-side; propagation never overwrites or deletes)
- warehouse content and data — the project's ingested nodes (`nodes/`), flags (`flags/`), the derived SQLite index, and per-instance `warehouse.config.json`. The robot ENGINE (`warehouse_robot/`) propagates as CORE; the warehouse DATA it operates on does not — propagation copies the engine and never runs it, so it cannot write or delete a single node, flag, or config.
- flat documentation in the consuming project
- instantiated config values (the project's filled spqr.config)
- any project-owned extension area outside the core surface

OUT-OF-BAND (not propagated by this mechanism — distributed separately)
- .claude/rules/ (AGENT_LAWS) — machine-level constitution. Its real home is the central machine-level Claude config (~/.claude/rules/), not the project repo. For a fresh clone / CI / N consumers it is simply absent, so its distribution is an explicit out-of-band setup step, named here, not an unstated assumption.

SUPERSEDED
- warehouse_robot/ — the SAW-38 deferred "out-of-band" note (updated only when the robot needs a fix, propagation decided at the warehouse stage) is SUPERSEDED by SAW-44: warehouse_robot/ is now a `propagate` (CORE) line above and flows with every bring-current snapshot. Recorded here so the reversal is explicit, not silent.
