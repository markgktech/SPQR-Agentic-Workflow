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
- warehouse content and data
- flat documentation in the consuming project
- instantiated config values (the project's filled spqr.config)
- any project-owned extension area outside the core surface

OUT-OF-BAND (not propagated by this mechanism — distributed separately)
- .claude/rules/ (AGENT_LAWS) — machine-level constitution. Its real home is the central machine-level Claude config (~/.claude/rules/), not the project repo. For a fresh clone / CI / N consumers it is simply absent, so its distribution is an explicit out-of-band setup step, named here, not an unstated assumption.

DEFERRED
- warehouse_robot/ — descoped (SAW-38 owner decision). Pulled in at first instantiation; thereafter updates only when the robot itself needs a fix. How warehouse-robot propagation works is decided at the warehouse stage, not here. Flagged only; not yet a manifest line.
