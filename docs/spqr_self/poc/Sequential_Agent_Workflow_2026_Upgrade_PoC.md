---

---
# Overview

2026 state-of-the-art upgrade for the current sequential, ticket-comment-based workflow in `markgktech/sequental-agent-workflow-template`. The full backlog has 17 items; this document covers the **S+A+B tier (13 items)** in implementation order. C-tier (14-17) comes later, only if the S+A+B foundation is in place and the current form genuinely feels limiting.

Prioritization is based on **effort/value ratio**, viewed from a **personal use / learning** perspective. Each item stands on its own; dependencies are flagged explicitly.

## Implementation roadmap

- **Day 1 (~1.5 hours):** S-tier (1-3) + start of A-tier (4-6) → noticeably better workflow already
- **One weekend (~3-4 hours):** rest of A-tier (7-9) → execution layer in place
- **Next free afternoon (~2-3 hours):** start of B-tier (10-11) → independent validation in place
- **When **[**CLAUDE.md**](http://claude.md/)** starts to feel heavy (~3 months):** rest of B-tier (12-13)

---

# S-tier — do this immediately

*Effort: minutes. Value: extremely high. No dependencies.*

## 1. Goal alignment `still_solving:` block

**Effort:** 5 minutes per agent prompt

**Value:** catches drift early

Add to every agent's system prompt: "End your output with a one-sentence `still_solving:` block stating the original ticket goal."

**Why:** the silent killer of sequential workflows is goal drift — every agent does its own job correctly, yet the final result diverges from the original ticket. One sentence makes this visible.

**Example output from Dev Engineer:**

```javascript
[implementation]

still_solving: Display the user's last 5 orders on the user profile page.
```

If step 3 reads "API endpoint optimization" instead → drift, intervention needed.

---

## 2. Severity-tagged findings (Impact × Effort + What/Why/How)

**Effort:** 15 minutes (prompt template swap in Peer Reviewer + QA + Judge)

**Value:** dramatically more readable output, easier to prioritize

Every finding in structured format:

```javascript
[HIGH/MED/LOW Impact, HIGH/MED/LOW Effort] Title
- What: Brief description of the issue
- Why: Why it matters
- How: Concrete suggestion to fix
```

**Why:** the LLM is forced to think structurally instead of just listing things. The 2D matrix (Impact × Effort) beats a 1-10 scale because it's decision-oriented.

---

## 3. Strict tool permissions per agent role

**Effort:** 10 minutes (`session-starters.md` update)

**Value:** structural guarantee — a lock, not a request

`allowed_tools:` list per role:

- **Master Architect:** Read, Grep, Glob (read-only)
- **Dev Engineer:** Read, Write, Edit, Bash, Grep, Glob
- **Peer Reviewer:** Read, Grep, Glob (read-only!)
- **QA Specialist:** Read, Write, Edit, Bash (writes tests)
- **DevOps:** Read, Bash, Grep

**Why:** if the Peer Reviewer can't use Edit, it won't "slightly rewrite" anything. Framework-level enforcement instead of prompt-level pleading.

---

# A-tier — doable over a weekend

*Effort: 30 min – 1 hr per item. Value: high.*

## 4. Master Architect structured PLAN output

**Effort:** 10 minutes (prompt fix)

**Value:** trackable, checkpointable planning

Master Architect's mandatory output format:

```javascript
PLAN:
- [ ] step 1: <concrete action>
- [ ] step 2: <concrete action>
- [ ] step 3: <concrete action>

expected_outputs:
- <what Dev Engineer must deliver>
```

**Why:** the planning layer already exists (Master Architect whiteboarding), but free text → hard to tell what Dev Engineer skipped. Turning it into a checklist makes it traceable.

---

## 5. Explicit handoff contracts (`expected_outputs` / `addressed`)

**Effort:** 30 minutes (two new fields at the end of every agent prompt)

**Value:** foundation of cascading-error defense

Every agent comment ends with:

```javascript
expected_outputs (for the next agent):
- <point 1>
- <point 2>
```

The next agent must respond with:

```javascript
addressed:
- point 1: ✓ <how I handled it>
- point 2: ✓ <how I handled it>
```

**Why:** today the Dev Engineer can silently skip the 5th architectural point — nobody knows it ever existed. The `addressed:` checklist makes this visible.

**Pairs with:** item 4 (the PLAN becomes the source of `expected_outputs`).

---

## 6. 3-level Verdict aggregation (Ready / Needs Attention / Needs Work)

**Effort:** 20 minutes (new block at the end of Judge / DevOps agent)

**Value:** explicit go/no-go decision

Judge agent (or final step) scores per-dimension on a 1-10 scale (correctness, completeness, alignment), then aggregates by an explicit rule:

- **Ready to Merge:** all dimensions ≥ 8
- **Needs Attention:** all ≥ 5, but not all ≥ 8
- **Needs Work:** any dimension < 5

**Why 3 levels and not 1-10:** you yourself won't make finer-grained decisions. The action space is 3-level (proceed / small fix / send back to Dev), so the verdict should be too.

---

## 7. Execution Agent (Bash-only: lint+test+build)

**Effort:** 1 hour (new role file + testing on your own project)

**Value:** token savings + deterministic quality gate BEFORE the LLM Reviewer

New agent role, deliberately lean:

- **Allowed tools:** Bash only
- **System prompt:** "Run the project's lint/test/typecheck/build commands. Return structured output: tool name, exit code, error count, first 20 errors with file:line:message. Do not interpret, do not fix."

**Workflow change:**

```javascript
Dev Engineer → Execution Agent → Peer Reviewer → QA → DevOps
```

**Why:** syntax checks, type checks, unused-import detection are not LLM tasks — deterministic tools exist (ruff, eslint, tsc, mypy). Free, fast, never hallucinate. The Peer Reviewer can then focus on semantic/architectural concerns.

---

## 8. Execution feedback loop

**Effort:** 30 minutes (Execution Agent prompt + DevOps logic update)

**Value:** the "build broken" case resolves without human involvement

If the Execution Agent finds an error (exit code ≠ 0), it auto-routes back to the Dev Engineer instead of forwarding to the Peer Reviewer. You don't decide in between.

```javascript
Dev → Execution (ERROR) → Dev (fix) → Execution (PASS) → Peer Reviewer
```

**Why:** broken-build bugs are evident, no human review needed. The Peer Reviewer only gets code that at least technically runs.

**Depends on:** item 7.

---

## 9. Strategic interrupt levels (mandatory vs. optional checkpoints)

**Effort:** 30 minutes (convention + per-agent flag)

**Value:** prevents review fatigue

Mandatory human checkpoints only in these cases:

- Architectural change ([CLAUDE.md](http://claude.md/) update)
- Public API change
- Security touch (auth, crypto, permissions)
- Verdict = "Needs Work"

In every other case → **auto-proceed**, if every agent's confidence is high and Verdict ≥ Needs Attention.

**Why:** if you have to review after every agent, you stop reviewing carefully after two weeks. Strategic placement = more real attention on what matters.

---

# B-tier — worth doing, but can wait 2-3 weeks

*Effort: 30 min – 2 hrs per item. Value: medium-high; becomes fully valuable only after S+A is in place.*

## 10. Independent Judge Agent

**Effort:** 1-2 hours (new role, isolated prompt)

**Value:** cascading-error detection

New agent role that **only** sees the original ticket description and the final code/PR — nothing from the Master Architect's plan, the Peer Reviewer's comments, or the QA findings. Goal alignment check, nothing else.

**Difference from Peer Reviewer:**

- Peer Reviewer: style, correctness, codebase fit
- Judge: "is this what we would have built given the ticket?"

Evaluation output: 3 dimensions (correctness, completeness, alignment), 1-10 scoring, justification. Verdict aggregation per item 6.

**Why:** the Peer Reviewer works with the same architectural assumptions as the Dev (shared ticket, shared context). If Dev misread the ticket, Reviewer will too.

---

## 11. Cross-Model Redundancy (Judge with an alternative model)

**Effort:** 30 minutes (Gemini API key + bash wrapper inside the Judge agent)

**Value:** eliminates model-specific blind spots

The Judge agent uses a **different model family** — if every other agent is Claude, the Judge should be Gemini (or vice versa).

**Free setup:**

1. `aistudio.google.com` → Get API key (free, no credit card)
2. Bash wrapper inside the Judge agent role file: `gemini-cli` or a direct API call via curl
3. Judge agent prompt makes it explicit: "Use the gemini CLI tool with this prompt: {prompt}"

**Why:** Claude tends to be an agreeable reviewer of Claude-written code. A cross-model independent perspective genuinely catches things a Claude-judge would miss.

**Depends on:** item 10.

---

## 12. Tiered context ([CLAUDE.md](http://claude.md/) / [DECISIONS.md](http://decisions.md/) / [RECENT.md](http://recent.md/) split)

**Effort:** 1-2 hours one-time ([CLAUDE.md](http://claude.md/) split + agent prompt updates)

**Value:** prevention; without it, month 6 becomes painful

**Today:** monolithic [CLAUDE.md](http://claude.md/) grows continuously.

**New structure:**

- `**CLAUDE.md**` — only active conventions + architecture core (max ~2k tokens)
- `**DECISIONS.md**` — decision archive, agents read it **only on demand** (RAG-style lookup)
- `**RECENT.md**` — last 10 tickets' lessons learned, auto-rotating

Agent prompt update: "Read [CLAUDE.md](http://claude.md/) always. Read [DECISIONS.md](http://decisions.md/) only if you need historical context for the current task. [RECENT.md](http://recent.md/) provides recent lessons learned."

**Why:** monolithic [CLAUDE.md](http://claude.md/) → 50k+ tokens after a year, every agent reads everything on every ticket. Fragmented retrieval is dramatically cheaper and more accurate.

---

## 13. Subagent memory (Claude Code only)

**Effort:** 5 minutes per agent (YAML frontmatter flag)

**Value:** cross-ticket learning, per-agent

Claude Code supports per-subagent memory directories. To enable:

```yaml
---
name: code-reviewer
description: Reviews code for quality
memory: project
---
```

The subagent automatically updates its own [MEMORY.md](http://memory.md/) with patterns, conventions, and recurring issues it discovers. By the next ticket, it already knows them.

**Why:** directly solves the [CLAUDE.md](http://claude.md/) staleness problem — the Peer Reviewer agent builds its own [MEMORY.md](http://memory.md/) from its own experience instead of reading global [CLAUDE.md](http://claude.md/).

**Depends on:** Claude Code; otherwise zero value.

---

# C-tier (later, not now)

The following 4 items are **not part** of this PoC, but belong to the full backlog. Worth adding only if S+A+B is in place and the current form genuinely feels limiting.

- **State Save + checkpoint recovery** (Pydantic schema)
- **Self-Evolving Conventions** (monthly Retrospective Agent)
- **Artifact-centric workflow** (`.claude/reports/` filesystem)
- **Time-travel rewind** (snapshot IDs)

---

# References

- Original repo: [https://github.com/markgktech/sequental-agent-workflow-template](https://github.com/markgktech/sequental-agent-workflow-template)
- Context Amnesia protocol: [https://medium.com/@ilyas.ibrahim/the-4-step-protocol-that-fixes-claude-codes-context-amnesia-c3937385561c](https://medium.com/@ilyas.ibrahim/the-4-step-protocol-that-fixes-claude-codes-context-amnesia-c3937385561c)
- 9 parallel agent code review: [https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents](https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents)
- Awesome Claude Code Subagents: [https://github.com/VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- Linear ticket workflow: [https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/)