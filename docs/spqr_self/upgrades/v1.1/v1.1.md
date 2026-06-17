---

---
## Summary

- **v1.0 foundation:** Sequential multi-agent pipeline (Senate → Collegium → Senate) with formal veto protocol, context isolation, and Notion ticket comments as external truth
- **v1.1 scope:** 10 targeted improvements — no new agents, no architecture changes; polishing reliability, traceability, and the feedback loop that enables cross-ticket learning
- **Why now:** v1.0 operates but leaves gaps in agent behavior consistency, output richness, and the self-improvement loop

---

## What's New — v1.1 vs v1.0

- **Feedback loop activated:** [LESSONS.md](http://lessons.md/) — Curator writes 1-2 bullets per ticket; Senate reads on startup; foundation for v2.0/v3.0 cross-ticket intelligence *(highest-value item in v1.1)*
- **Agent behavior hardened:** Bash tool mandate (domain-specific granular permissions — Praetor: full suite; Tribunus: lint only; Probator: tests + build; technical enforcement via `--allowedTools`), Sensitive operation fallback (Anti-Meeseeks extension: destructive ops only — Notion page delete/overwrite + file delete outside worktree), Devil's Advocate role (rotating Senate Opener step)
- **Output enriched:** ADR proposal (mandatory section in Censura GREEN output), [CLAUDE.md](http://claude.md/) update proposal (mandatory section in Curator output) — both with exact proposed text; owner decides and writes
- **Tooling extended:** Context7 MCP integration (Praetor loads framework docs on-demand), Parent ticket traceability (Notion DB self-referential relation + Consilium pre-flight check)
- **Session starters added:** Standalone Debugging Tribunus (runs without pipeline context), Retrospective session (manual trigger)

---

## Implementation Groups

**1. Memory & Learning**

- Items: [LESSONS.md](http://lessons.md/) · 2.3 ADR proposal · 7.6 Retrospective session
- Affected files: `curator-output.md` (update) · `senate.md` (new) · `censura-output.md` (new) · `session-starters.md` (update)

**2. Quality & Safety**

- Items: 3.7 DA role · 3.6a Context7 MCP · 3.6b Bash tool mandate · 8.4 Sensitive op fallback
- Affected files: `senate.md` (new) · `AGENT_LAWS.md` (new) · `praetor-input.md` · `tribunus-input.md` · `probator-input.md` (update)

**3. Traceability**

- Items: 2.7a Parent ticket · 6.6 [CLAUDE.md](http://claude.md/) update proposal · 9.2 Standalone Debugging Tribunus
- Affected files: `consilium-input.md` (new) · Notion Dev Tickets DB schema · `curator-output.md` (update) · `session-starters.md` (update)

[[Memory & Learning]]

[[Quality & Safety]]

[[Traceability]]