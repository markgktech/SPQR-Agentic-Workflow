---

---
## Preparation

Before invoking the roundtable, the master reads all relevant tickets and forms an initial reading. The roundtable confirms, challenges, or extends that reading — it does not generate from a blank slate. A roundtable called without prior preparation produces shallow output.

---

## What the roundtable is

The roundtable is a structured challenge session run by the master agent before planning and optionally during execution. It is a tool, not a phase — it can be invoked at any point the master judges it necessary.

---

## When to run it

**Mandatory:**

- Phase 2 — before the item list is finalised and Phase 3 begins

**Master's call (no owner approval needed):**

- After any execution group output that contains an out-of-scope finding, a stalled item, or a Changes Made section that deviates from the brief
- When a decision in Phase 3 has significant architectural implications
- When two items appear to conflict

**Not needed:**

- After routine execution group outputs with no surprises
- For minor wording or formatting decisions
- For questions the owner has already explicitly closed — roundtable does not reopen owner decisions

---

## Who participates

| Persona | Role | Focus |
| --- | --- | --- |
| [Master Persona 1] | Dev Process Architect | Mechanical correctness, load order, incomplete specs, missing constraints |
| [Master Persona 2] | Agentic Trends Expert | Naive agentic assumptions, deployment vs spec gaps, 2026 tooling context |

Persona names are set in the session starter PERSONAS section. Roles and focus areas are fixed.

---

## Rules

- Each persona arrives with an independent position — no deference to the other's prior statement
- Both personas can update their position when challenged with new evidence
- Neither persona adjusts conclusions based on the master's apparent preference
- The master synthesises — personas do not reach consensus on behalf of the master
- A roundtable produces findings, not approvals. The master decides what to do with them.

---

## Output

At the end of every roundtable the master produces a short summary:

- Decisions made or confirmed
- Points to update (which phase, which file, which Notion page)
- Open items that need new tickets

This summary is what drives the next action — not the discussion itself.

---

## Clean pass rule

If a persona finds no genuine problem, they state it explicitly — but must justify it: **"CLEAN PASS — checked [specific aspects], no issues found."** An unjustified clean pass is not valid. Law 4 (Be like Spock) applies both ways: suppress nothing real, fabricate nothing.

**Execution protocol — treat as checklist, not prose:**

1. Run first round
2. Apply all modifications found
3. CHECK: did the first round produce any modifications?
    - YES → run second round on modified/new content only, then write summary
    - NO → justified clean pass, write summary
4. Write output summary and close

Skipping step 3 is the failure mode — modifications applied ≠ roundtable complete.

## Agent-actionability test

For every rule in the file under review, ask: *can a stateless execution agent apply this rule without additional context?* If the answer is uncertain — raise it as a finding, do not clean pass. This is the primary lens for roundtable review.

Examples of non-actionable rules that should be flagged:

- Time-based rules an agent cannot measure ("under 10 minutes")
- Conditional logic with no stated condition ("field is always yes")
- Ambiguous variants with no selection criteria ("two formats, no rule for which to use")

---

## What it is not

- Not an approval gate — the master does not need roundtable sign-off to proceed
- Not a blocker — if personas disagree and neither has new evidence, the master decides
- Not a substitute for owner confirmation at the three explicit checkpoints