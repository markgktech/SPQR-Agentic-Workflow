# SPQR v1.0 — Sequential Agentic Workflow

A structured, sequential multi-agent development workflow built on Claude Code and Notion. Every task has a ticket. Every agent runs in a stateless session. The external record is truth.

---

## What is SPQR

SPQR is a development pipeline where each stage of the software delivery cycle is handled by a dedicated Claude Code agent. Agents do not share session memory — they pass state through structured Notion ticket comments. This makes the pipeline auditable, resumable, and contamination-free between stages.

Two pipelines:

**OPUS** — feature development:
```
Senate: Consilium  →  Praetor  →  Tribunus  →  Probator  →  Curator  →  Senate: Censura
  (design)            (build)     (review)      (QA)         (ops)        (verdict)
```

**EXPLORACIO** — research / spike:
```
Senate: Consilium  →  Quaestor  →  Senate: Censura
  (scope)             (research)     (verdict)
```

---

## Agents

| Agent | Role | Pipeline |
|-------|------|----------|
| Senate | Design authority (Consilium) and post-execution review authority (Censura). Three deliberation personas in one session. | Both |
| Praetor | Implements the feature ticket in a worktree-isolated session. Never writes code before the owner approves approach. | OPUS |
| Tribunus | Independent code reviewer. Read-only. One veto per pipeline run. | OPUS |
| Probator | Independent QA verifier. Runs the test suite. One veto per pipeline run. | OPUS |
| Curator | Operational steward — build, lint, CLAUDE.md compliance, scope boundary, localization, dead code, operational risk. Verdict only, no veto. | OPUS |
| Quaestor | Spike researcher. Produces a structured decision document. Never writes code. | EXPLORACIO |

---

## Four Laws

Every agent operates under the same four laws, in priority order:

1. **Stay in Character** — no stage skipping; challenge through proper channels only
2. **Anti Meeseeks** — complete pre-flight before acting; owner must explicitly close discussion
3. **Don't be Dory** — write a ticket comment at every major checkpoint; the external record is truth
4. **Be like Spock** — independent view required; no sycophancy; suppress no finding

---

## How to adopt

1. **Fill in CLAUDE.md** — copy `CLAUDE.md.template`, fill every `[PLACEHOLDER]` with your project's rules, stack, and phase boundaries. This is the single most important step — every agent loads it.

2. **Provide project skill files** — the workflow references `[project-skill-files]` and `[project-testing-guidelines]` in several places. Replace these with your actual domain skill files (e.g. language patterns, framework conventions, testing scope rules).

3. **Fill in code-review-checklist.md** — the `PROJECT CRITICAL RULES` section contains a placeholder. Populate it from your CLAUDE.md Critical Rules.

4. **Set up Notion** — each ticket needs a Notion page. Agents read the ticket and post structured comments as checkpoints.

5. **Update session-starters.md** — replace `[PROJECT_PATH]` with your actual project path.

---

## Dependencies

- **Claude Code** (claude.ai/code or CLI)
- **Notion MCP** — agents read tickets and post comments via Notion MCP
- **git worktree** — Praetor runs in an isolated worktree per ticket

---

## File structure

```
.claude/
└── rules/
    └── AGENT_LAWS.md          — four laws, auto-loaded every session
docs/
├── agents/
│   ├── senate.md
│   ├── praetor.md
│   ├── tribunus.md
│   ├── probator.md
│   ├── curator.md
│   ├── quaestor.md
│   └── session-starters.md
└── skills/
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
    └── code-review-checklist.md
CLAUDE.md.template             — fill this in for your project
```

---

## License

MIT
