---
cover: "[[Agent Delivery.png]]"
---
This section contains the system prompts and operating logic for each AI agent used in the **Foodoire** development workflow.

## Agent Overview

| Agent | Role | Input | Output | Key behaviour |
| --- | --- | --- | --- | --- |
| 🛠️ Dev Engineer | Writes production Swift code | Task description + spec | Files, code, assumptions, handoff note | Confirms scope before coding; hard stops on uncovered architectural decisions |
| 🔍 Peer Reviewer | Reviews code, challenges decisions | Dev output | Structured report (P0/P1/P2 + challenged decisions) | Devil's advocate — considers alternatives before criticising |
| 🧪 QA Specialist | Writes tests, files bug tickets | Approved code | Unit tests + bug tickets | Source of truth for issue tracking |
| ⚙️ DevOps | Commits, manages branches, verifies build | QA-approved code | Commit + build verification | Never commits without explicit instruction |
| 🏛️ Master Architect | Cross-cutting technical decisions | Escalations from any agent | Decision + rationale + [CLAUDE.md](http://claude.md/) update | Invoked only when agents cannot resolve ambiguity |

All agents operate on the same codebase and read the same `CLAUDE.md` from the repo root. Each agent has a specific role, scope, and output format. The workflow is **sequential** — you coordinate between agents and decide when to advance to the next stage.

---

## Workflow Overview

```javascript
You (task description)
    ↓
1. Dev Engineer — understands architecture, writes the code
    ↓
You (review output, decide: send to Peer Reviewer or revise)
    ↓
2. Peer Reviewer — architectural + code style review, surfaces issues clearly
    ↓
You (decide: revert to Dev Engineer with notes, or advance to QA)
    ↓
3. QA Specialist — writes unit tests, identifies bugs, documents issues as tickets
    ↓
You (decide: send bugs back to Dev Engineer, or advance to DevOps)
    ↓
4. Dev Engineer (bugfix loop) — fixes flagged issues
    ↓
5. DevOps — commit, branch management, build verification
    ↓
You (final approval)
```

---

## Skills

Skill files live in `docs/skills/` in the repo. Load them by adding one line to the agent session prompt.

| Skill file | For agent | Load with |
| --- | --- | --- |
| `swift-patterns.md` | Dev Engineer | `Read docs/skills/swift-patterns.md before starting.` |
| `swiftdata-patterns.md` | Dev Engineer | `Read docs/skills/swiftdata-patterns.md before starting.` |
| `ios-testing.md` | QA Specialist | `Read docs/skills/ios-testing.md before starting.` |
| `code-review-checklist.md` | Peer Reviewer | `Read docs/skills/code-review-checklist.md before starting.` |
| `whiteboarding.md` | Master Architect | `Read docs/skills/whiteboarding.md before starting.` |

Skills are optional per session — load only what is relevant to the task. For most tasks, load both Dev Engineer skills together.

---

## Debug Agent

🟡 **Planned for Phase 2.** A dedicated Debug agent will be added before Phase 2 development begins. It handles active bug diagnosis (predict → log → run → resolve) for issues found in a running app, distinct from QA’s pre-release testing role.

---

## Session Management

- Every agent = a new Warp terminal session
- Sessions are stateless — the Notion ticket comments are the memory between sessions
- After a session ends, the agent posts a comment on the ticket addressed to the next agent — no manual copy-paste needed
- For bugfix loops: open a new Dev Engineer session with the same TICKET_URL — it reads the QA bug tickets from the comments automatically
- Name each Warp tab: `JEGY-XXX — Agent Name` to avoid confusion
- Sessions can be closed after the agent has posted its comment on the ticket

## Warp Starter Prompts

All 7 agent prompts are configured in Warp under the Starter prompts folder. If they are ever lost, the exact prompt text for each agent can be found in `docs/session-starters.md` in the repo.

Prompt structure:

- **Title:** `Foodoire — [Agent name]`
- **Arguments:** `TICKET_URL` for every agent + `TASK` (Dev Engineer), `FEATURE` (Whiteboarding), `REASON` (Master Architect Review)
- **Prompt:** reads `CLAUDE.md`, the relevant `docs/agents/` file, and the relevant `docs/skills/` files

Note: the Handoff Note and branch name do NOT need to be copied manually — the agent reads them directly from the Notion ticket comments.

| Agent | Warp title | Arguments |
| --- | --- | --- |
| Master Architect (Whiteboarding) | `Foodoire — Master Architect (Whiteboarding)` | FEATURE, TICKET_URL |
| Dev Engineer | `Foodoire — Dev Engineer` | TASK, TICKET_URL |
| Peer Reviewer | `Foodoire — Peer Reviewer` | TICKET_URL |
| QA Specialist | `Foodoire — QA Specialist` | TICKET_URL |
| Dev Engineer (Bugfix) | `Foodoire — Dev Engineer (Bugfix)` | TICKET_URL |
| DevOps | `Foodoire — DevOps` | TICKET_URL |
| Master Architect (Review) | `Foodoire — Master Architect (Review)` | TICKET_URL, REASON |

## Agents

See subpages below for each agent's system prompt and operating logic.

---

## Notes

- **git commit and git push: NEVER** — Only the project owner commits and pushes. No agent, no Claude Code session may run `git commit` or `git push` under any circumstances. This rule is absolute and has no exceptions.
- All agents read `CLAUDE.md` at the repo root before starting any task
- Agents never navigate outside their defined scope
- You are the decision maker at every stage — agents surface information, you decide
- Bug tickets generated by QA are the source of truth for issue tracking

[[1. Dev Engineer]]

[[2. Peer Reviewer]]

[[3. QA Specialist]]

[[4. DevOps]]

[[5. Master Architect]]