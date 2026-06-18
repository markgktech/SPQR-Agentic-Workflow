# SPQR v1.3: Sequential Agentic Workflow

A structured, sequential multi-agent development workflow built on Claude Code. Every task has a ticket. Every agent runs in a stateless session. The work record lives as files in the project repo — the external record is truth.

---

## What is SPQR

SPQR is a development pipeline where each stage of the software delivery cycle is handled by a dedicated Claude Code agent. Agents do not share session memory; they pass state through structured handoff files kept in the project repo — a per-ticket hub, an output document, and an append-only handover log. This makes the pipeline auditable, resumable, and contamination-free between stages.

Three pipelines:

**EXPLORATIO**: research / spike:
```
Senate: Consilium  →  Quaestor  →  Senate: Censura
  (scope)             (research)     (verdict)
```

**OPUS**: feature development:
```
Senate: Consilium  →  Praetor  →  Tribunus  →  Probator  →  Curator  →  Senate: Censura
  (design)            (build)     (review)      (QA)         (ops)        (verdict)
```

**RETROACTIO**: cross-run retrospective:
```
Retrospector
  (process-health review across runs — single agent, owner-initiated, no handoff chain)
```

---

## Agents

| Agent | IT Equivalent | Role | Pipeline |
|-------|---------------|------|----------|
| Senate: Consilium | Tech Lead / Solution Architect | Design authority. Three deliberation personas in one session. | Both |
| Senate: Censura | Engineering Manager | Post-execution review authority. Verdict only. | Both |
| Praetor | Software Engineer | Implements the feature ticket on its own short-lived branch. Never writes code before the owner approves approach. | OPUS |
| Tribunus | Senior Engineer (code reviewer) | Independent code reviewer. Runs the project linter independently. One veto per pipeline run. | OPUS |
| Probator | QA Engineer | Independent QA verifier. Runs the test suite. One veto per pipeline run. | OPUS |
| Curator | DevOps / SRE | Operational steward: build, lint, CLAUDE.md compliance, scope boundary, localization, dead code, operational risk. Verdict only, no veto. | OPUS |
| Quaestor | Technical Analyst / Research Engineer | Spike researcher. Produces a structured decision document. Never writes code. | EXPLORATIO |
| Retrospector | Agile Coach / Process Lead | Cross-run process-health reviewer. Single agent, single session, no handoff chain. Produces a retrospective document; flags candidates only, no code, no tickets. | RETROACTIO |

**Deliberation personas**

**Senate deliberation model:** The Senate runs as three distinct personas in a single session: [Name 1], [Name 2], and [Name 3]. Each arrives with an independent position, challenges the others, and synthesizes toward a decision. One persona acts as Devil's Advocate per Consilium session. Persona names are customizable in `session-starters.md`, not in the agent files, keeping them project-specific without forking the core workflow.

| Agent | Customize as | Roman inspiration | IT inspiration | IT Role | Focus |
|-------|-------------|-------------------|----------------|---------|-------|
| Senate Member 1 | [Name 1] | Cicero | Rich Hickey | Principal Engineer | First-principles, anti-complexity. Questions the premise before accepting any solution. |
| Senate Member 2 | [Name 2] | Caesar | Kelsey Hightower | Engineering Manager | Pragmatic and delivery-focused. Shortest path to working and shipped. |
| Senate Member 3 | [Name 3] | Cato | Charity Majors | SRE / Maintenance | Stability-first, skeptical of hype. Thinks about what breaks in production before it's built. |
| Quaestor | [Name 4] | — | Julia Evans | Staff Engineer | Systematic and evidence-driven. Decomposes every unknown into chunks before drawing conclusions. Researches wide, explains simply, documents precisely. |
| Other agents | — | — | — | — | No personalization: role is execution-focused and fully defined by agent file; no deliberation persona required. |

---

## Four Laws

Every agent operates under the same four laws, in priority order:

1. **Stay in Character**: no stage skipping; challenge through proper channels only
2. **Anti Meeseeks**: complete pre-flight before acting; owner must explicitly close discussion
3. **Don't be Dory**: record the handoff at every major checkpoint; the external record is truth
4. **Be like Spock**: independent view required; no sycophancy; suppress no finding

---

## Ticket system

Every unit of work maps to one of four ticket types:

| Type | Purpose |
|------|---------|
| **Spike** | Research and exploration — produces a structured decision document |
| **Feature** | New functionality — runs the full OPUS pipeline |
| **Bug** | Defect captured during QA — fed back into OPUS |
| **Doc** | Workflow documentation maintenance — handled by Quaestor |

**Ticket creation is automated, owner-gated.** After every spike, Quaestor proposes follow-up tickets. Censura validates them in a dedicated ticketing phase. No ticket is created in your ticket system until the owner explicitly approves:

```
Quaestor proposes  →  Censura validates  →  Owner approves  →  Tickets created
```

---

## Configuration

SPQR ships as a generic template — every project-specific detail is a named placeholder. Before running any pipeline, those placeholders need to be filled in: persona names, project path, ticket system IDs. `docs/CONFIGURE.md` is the single inventory: every placeholder, which files contain it, and what to put there.

**Why CONFIGURE.md exists.** Without it, placeholders are scattered across a dozen skill and agent files. CONFIGURE.md means one place to configure, not a grep session across the repo.

**Notion is the reference implementation, but not required.** The ticket system only holds ticket definitions — the work record is files in your repo — so any system with linkable tickets works: Linear, GitHub Issues, Jira, or plain markdown. CONFIGURE.md Section 3 covers the alternatives.

**An agent can perform the configuration.** Provide a project brief, point the agent at `docs/CONFIGURE.md`, and it will substitute all placeholders across the relevant files. Recommended approach for new project setup.

---

## How to adopt

Before filling anything in, open `docs/CONFIGURE.md` — it lists every placeholder in the workflow, which file it lives in, and what to put in it.

1. **Fill in CLAUDE.md**: copy `CLAUDE.md.template`, fill every `[PLACEHOLDER]` with your project's rules, stack, and phase boundaries. This is the single most important step; every agent loads it.

2. **Provide project skill files**: the workflow references `[project-skill-files]` and `[project-testing-guidelines]` in several places. Replace these with your actual domain skill files (e.g. language patterns, framework conventions, testing scope rules).

3. **Fill in code-review-checklist.md**: the `PROJECT CRITICAL RULES` section contains a placeholder. Populate it from your CLAUDE.md Critical Rules.

4. **Set up Notion**: each ticket needs a Notion page that agents read for the ticket definition. The per-ticket work record — hub, output, and handover — is written as files in your project repo, not as comments. Ticket creation requires Notion templates (one per type: Spike, Feature, Bug, Doc) — see `docs/CONFIGURE.md` for the IDs needed.

5. **Update session-starters.md**: fill in `[PROJECT_PATH]` with your project root and the PERSONAS section with your persona names. If you plan to run workflow upgrades, open `docs/upgrade/upgrade-agent.md` and fill in the CONFIG section: persona names, project paths, and memory path. This is the single place for all upgrade configuration.

6. **Set up MCP servers**: register Context7 MCP in your Claude Code settings. Session-starters.md specifies the `--allowedTools` flags per agent; verify these match your setup before first run.

---

## Dependencies

- **Claude Code** (claude.ai/code or CLI)
- **Notion MCP**: agents read ticket definitions and create tickets via Notion MCP; the per-ticket work record is kept as files in the project repo
- **Context7 MCP**: agents load current library documentation on-demand during implementation and review
- **git**: Praetor opens a short-lived feature branch per ticket; the owner commits and merges

---

## File structure

```
.claude/
└── rules/
    └── AGENT_LAWS.md          (four laws, auto-loaded every session)
docs/
├── CONFIGURE.md               (placeholder reference — start here when setting up)
├── LESSONS.md                 (pipeline retrospective log; written by Censura after every run)
├── agents/
│   ├── senate.md
│   ├── praetor.md
│   ├── tribunus.md
│   ├── probator.md
│   ├── curator.md
│   ├── quaestor.md
│   └── session-starters.md
├── skills/
    ├── consilium-input.md
    ├── consilium-discussion.md
    ├── consilium-output.md
    ├── censura-input.md
    ├── censura-discussion.md
    ├── censura-output.md
    ├── praetor-input.md
    ├── praetor-discussion.md
    ├── praetor-output.md
    ├── praetor-revision.md
    ├── praetor-impl-doc.md
    ├── tribunus-input.md
    ├── tribunus-output.md
    ├── probator-input.md
    ├── probator-output.md
    ├── curator-input.md
    ├── curator-output.md
    ├── quaestor-relatio.md
    ├── quaestor-relatio-output.md
    ├── spike-document.md
    ├── collegium-veto.md
    ├── ticket-comment.md
    ├── doc-maintenance.md
    ├── code-review-checklist.md
    ├── debugging-tribunus-input.md
    ├── ticket-slicing.md
    ├── censura-ticketing-input.md
    ├── censura-ticketing-discussion.md
    ├── censura-ticketing-output.md
    └── quaestor-doc-execute.md
├── retro/
│   ├── retrospector.md        (Retrospector agent identity)
│   ├── session-starter.md     (paste prompt — milestone + tickets in scope)
│   ├── input.md               (pre-flight — load order, git boundary)
│   ├── discussion.md          (HITL gate — owner closes with "go")
│   └── output.md              (local retro file, template-exact)
├── upgrade/
│   ├── session-starter.md     (paste prompt — scope + paths)
│   ├── upgrade-agent.md       (master agent definition — identity, config, pipeline, skills)
│   ├── roundtable.md
│   ├── decision-making.md
│   ├── planning.md
│   ├── execution.md
│   ├── context-window.md
│   └── wrap-up.md
CLAUDE.md.template             (fill this in for your project)
```

---

## Version History

### v1.3 (2026-06)
- RETROACTIO pipeline: new Retrospector agent — single-agent, single-session cross-run process-health review; new `docs/retro/` folder (5 files: agent, input, discussion HITL gate, output, session-starter). Triggers: owner milestone + LESSONS.md 10-entry counter (signals, no auto-trigger). Includes a rule-rot pass; flags candidates only — no code, no tickets (DOC-18)
- Censura CONVERGENCE stop-branch: co-located gate evaluated before verdict commitment; owner check-in required on a significant emergent gap, resume only on explicit owner closure (DOC-15)
- Quaestor external-claim verification: decision-bearing external claims must be verified against a primary source during research, never inherited — ACCEPTED / REFUTED / UNKNOWN (DOC-16)
- Fetch strategy / token hygiene: `quaestor-relatio.md` FETCH STRATEGY — skip re-fetch on routine writes (verify after format-sensitive ones); WebFetch external URLs only (DOC-14)
- session_id resumability: `ticket-comment.md` now carries session_id on every checkpoint comment; never omitted (DOC-17)
- Branch strategy: branch granularity follows the deliverable, not per-ticket; Consilium decides scope and sets the ticket Branch property, Praetor consumes it; worktree teardown gate (commit or stash before removal)
- CONFIGURE.md: three new retro placeholders (`[RETRO_PARENT_ID]`, `[RETRO_TEMPLATE_ID]`, `[RETRO_SESSION_STARTER_ID]`)
- Generic-template hygiene: genericized residual iOS tooling references (swiftlint / xcodebuild) in the README (SAW-16)

### v1.2.1 (2026-05)
- Upgrade Way of Working: new `docs/upgrade/` folder with master orchestrator session starter and six skill files covering roundtable, decision making, planning, execution order, context window management, and wrap-up
- README: Ticket system, Configuration, and Upgrading SPQR sections added
- CONFIGURE.md: `[Master Persona 1]` and `[Master Persona 2]` placeholders added for upgrade roundtable personas

### v1.2 (2026-05)
- Ticket creation automated: Quaestor proposes → Censura validates → owner approves → Notion tickets created; shared ticket-slicing.md skill (two modes)
- Censura two-phase model: VERIFY (existing) + TICKETING phase (3 new skill files)
- Agent hygiene: 8 fixes from SPIKE-004 — handoff accuracy, date validation, context alerts, spike doc location, discussion depth calibration
- DOC process: new quaestor-doc-execute.md for DOC-type ticket handling with per-fix re-verification
- SPQR repo public-ready: all project-specific data replaced with named placeholders; CONFIGURE.md setup guide added

### v1.1 (2026-05)
- LESSONS.md retrospective log: Censura writes one entry per pipeline run; suggests retrospective at 10 entries
- Devil's Advocate role: one persona designated as DA per Consilium session; argument captured in output
- Granular Bash permissions: Tribunus (linter only), Probator (build + test + git diff)
- Context7 MCP: Praetor and Tribunus load current library docs on-demand
- Sensitive op HITL: Praetor confirms before Notion delete or file delete outside worktree
- Parent ticket tracing: Censura sets parent_ticket when creating follow-up tickets (requires Notion DB self-referential relation)
- ADR proposal field: Censura surfaces ADR candidates at ticket close
- Standalone Debugging Tribunus: dedicated session starter and skill file for non-pipeline debugging
- senate.md Notion MCP write declared (was assumed, not specified in v1.0)

### v1.0 (2025)
- Initial release

---

## Upgrading SPQR

SPQR is designed to evolve. When gaps surface — through Censura retrospectives, spike findings, or operational experience — the upgrade process turns them into versioned improvements applied consistently across all files.

**Why a structured process?**
- Workflow changes touch many files at once; ad hoc edits cause inconsistencies
- Each upgrade is recorded in the repo (a run container under `docs/spqr_self/upgrades/<version>/`) before and during execution — reviewable and traceable; ticketing stays in Notion (SAW tickets)
- Changes apply to your project repo first, then sync to the generic template _(propagation direction under review)_

**How it works:**
1. Open SAW tickets for each identified gap or improvement
2. Load the master orchestrator session from `docs/upgrade/session-starter.md`
3. Master agent runs a roundtable → builds a decision log → groups changes into execution sets
4. Each group runs in a separate agent session driven by a written brief
5. Results reviewed; open items become new tickets

**When to run an upgrade:**
- After Censura surfaces recurring friction in the retrospective log
- When a spike reveals a gap in the current workflow
- When syncing your project fork back to the generic template

---

## License

MIT
