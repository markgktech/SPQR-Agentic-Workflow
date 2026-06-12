---
cover: "[[Sequential Agentic Workflow v1.0 SPQR version]]"
---
## Summary

- **Old workflow problem:** The Master Architect agent mixed whiteboarding, spike research, and post-dev review into one role. Dev / Reviewer / QA / DevOps agents had no formal veto format, no context isolation between reviewers, and no structured handoff protocol — every session started from scratch.
- **SPQR v1.0 fix:** A formalized pipeline replaces the ad-hoc setup. A **Senate** (3-persona deliberation body) opens and closes every ticket. A **Quaestor** handles spike research exclusively. The **Collegium** (Praetor → Tribunus → Probator → Curator) executes feature tickets with structured veto format, context isolation, and ticket-comment handoffs.
- **Consistency:** Every agent operates under the same 4 Agent Laws. Skill files use progressive disclosure — each stage loads only what it needs, no context bloat.
- **Traceability:** Ticket comments are the memory between sessions. Delta docs are created on revision only. Spike Documents are recorded permanently as Notion child pages on the ticket.

---

## Agentic Workflow — Owner's View

![[Agentic.workflow.v1.1.drawio(2).png]]

### Spike Ticket (large unknowns, new territory)

1. Owner creates a **SPIKE ticket** in Notion with the question to answer
2. **Senate: Consilium** — brainstorm with 3 personas (Cicero / Caesar / Cato); lock decisions, blockers, assumptions
3. **Quaestor** — decomposes mandate into research chunks, investigates, presents findings to owner for approval
4. Owner approves or redirects → Quaestor loops on redirect
5. **Senate: Censura** — reviews Quaestor output; creates **Spike Document** child page on the ticket
6. Spike Document is now available as Decision Table context for future feature Praetors

### Feature Ticket

7. Owner creates a **feature ticket** in Notion
8. **Senate: Consilium** — plan the approach (skippable if a spike doc already covers unknowns)
9. **Praetor** — implements ticket scope only; posts ticket comment when done
10. **Tribunus → Probator → Curator** — sequential review; each loads ticket comments; veto sends back to Praetor-revision
11. **Senate: Censura** — final review; **GREEN / YELLOW / RED** verdict
12. Owner reviews verdict, commits and merges

---

## Agents

- **Senate** (Tomi=Cicero, Zsombi=Caesar, Peti=Cato) — 3-persona deliberation body; runs as Consilium before execution, Censura after
- **Quaestor** (Cornelia Evans / Timi) — spike research executor; chunk decomposition, evidence-driven, delivers Spike Document
- **Praetor** — dev executor; implements scope only, worktree isolation, posts ticket comment on completion
- **Tribunus** — code reviewer; context-isolated (ticket comments only), single-issue veto authority
- **Probator** — QA verifier; runs test suite against changed paths, single-issue veto authority
- **Curator** — DevOps; build + lint + 8-area check, 3-level verdict (Ready to Merge / Needs Attention / Needs Work)

---

## Skills

Each agent loads skill files on demand — one file per stage. Skills define what to load, how to reason, what to output, and what never to do.

- **Shared (Collegium):** `ticket-comment.md` — comment etiquette for all agents; `collegium-veto.md` — single-issue veto format
- **Praetor:** `praetor-input` → `praetor-discussion` → `praetor-output` → `praetor-revision`
- **Senate:** `consilium-input/discussion/output` + `censura-input/discussion/output`
- **Quaestor:** `quaestor-relatio-input/discussion/output` + `spike-document`
- **Review agents:** `tribunus-input/output`, `probator-input/output`, `curator-input/output`
- **Existing skills (carried forward):** `swift-patterns`, `swiftdata-patterns`, `ios-testing`, `code-review-checklist`, `doc-maintenance`

---

[[OG Sequential Agentic Workflow v1.0 SPQR]]

[[Upgrade - Sequential Agentic Workflow v1.1]]

[[Upgrade - Sequential Agentic Workflow v1.2]]

[[Upgrade — Sequential Agentic Workflow v1.3]]