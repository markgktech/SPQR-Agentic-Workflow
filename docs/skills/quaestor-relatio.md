---
name: quaestor-relatio
description: Quaestor research and presentation skill — pre-flight, chunk research, self-reflection, and owner discussion in one session
---

PRE-FLIGHT
Load in order:
1. AGENT_LAWS.md
2. CLAUDE.md
3. DECISIONS.md
4. Ticket (full text)
5. Consilium comment — scope only: still_solving; read expected_outputs from ticket body Handoff section, not from comment
   Do NOT read Consilium decisions section yet.
6. if ticket prefix is DOC-XXX: load quaestor-doc-execute.md
Stop if anything missing — halt and request from owner.

FETCH STRATEGY
Verification skip: Notion create/write returns success + URL → confirmed; do not re-fetch to verify a routine write. BUT do verify after a structurally complex / format-sensitive write (multi-section content, code blocks).
WebFetch no-go: external URLs only; skip Notion-internal links, private/auth-gated repos, and other vendor-gated URLs — 403 expected.

CHUNK DECOMPOSITION
Break mandate into chunks: one chunk = one researchable question with a concrete, independently verifiable finding.
Map dependencies before starting — block dependent chunks until prerequisites complete.
Scope drift = new SPIKE ticket, never expand current mandate.

RESEARCH
Before any web search: verify today's date; orient all queries to current date.
Investigate each chunk independently: web, docs, codebase, Notion — cite every source.
Verify external claims — never inherit. Consilium claims about external facts (API behaviour, bug fixes, platform release outcomes, library/framework guarantees) must be independently verified during research, not accepted as given. Scope: decision-bearing external claims only — a claim a recommendation/decision rests on; skip incidental mentions. Search for a primary source (release notes / official spec or standards proposal / vendor session or documentation) and tag the outcome:
  ACCEPTED — primary source found and cited.
  REFUTED — primary source contradicts the claim → flag as a finding; the Consilium claim is wrong, not merely unverified.
  UNKNOWN — no source either way → escalate; never silently inherit.
After all chunks: load Consilium decisions section → compare against own findings.
Surface drift, gaps, and contradictions between own findings and Senate conclusions.

SELF-REFLECTION
Goal: find what has NOT been examined yet — not a pass/fail gate.
Check: logical fallacies in own reasoning; uncovered edge cases; conclusions without sufficient evidence.
Quaestor owns the spike decisions — actively surface Senate errors if well-founded.
Come with everything: findings, questions, contradictions, decisions that seem wrong, spike errors.
No pre-filtering.

DISCUSSION
Present to owner after self-reflection — same session, do not close.
Present high-level first: what is documented, what is excluded, why.
Per finding: tag irreversibility, blast radius, confidence.
Bring everything openly — no filtering before the owner sees it.
If owner states a decision that contradicts a HIGH impact finding: state the contradiction explicitly once, then defer.
Escalate only genuine uncertainty. Show reasoning, not conclusions.
If open gaps >2: alert owner — spike may not close fully.
If position changes on the same topic more than once: flag explicitly to owner — "I have revised this answer [X] times — topic may require a dedicated spike." Do not produce a third answer without this flag.
HIGH impact or HARD TO REVERSE topics: do not close unilaterally. Must offer alternative, surface uncertainty, or request explicit owner confirmation before the owner closes discussion.

NEVER
Never reach 100% context without alerting owner at 80% — no exceptions

STOP — do not proceed to quaestor-relatio-output.md until owner explicitly closes discussion.
