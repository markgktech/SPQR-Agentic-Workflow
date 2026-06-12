---

---
## Affected Files

- `censura-output.md` — new file (`docs/skills/`)
- `senate.md` — new file (`docs/agents/`) ⚠️ **shared with Quality & Safety — write once, covers both groups**
- `session-starters.md` — update (existing)

> Note: earlier drafts assigned [LESSONS.md](http://lessons.md/) writing to Curator. Roundtable decision (2026-05-28): **Censura writes**, not Curator — Censura has the full picture (verdict + all review findings) and is the only agent that can contextualize a lesson correctly.

---

## Item [LESSONS.md](http://lessons.md/) — Per-ticket Learning

**What:** After every pipeline run, Censura writes 1-2 bullet lessons to `LESSONS.md`. Senate reads the file at startup on every session. This is the feedback loop that makes the pipeline learn from itself over time — foundation for v2.0/v3.0 cross-ticket intelligence.

**Who writes:** Censura (Senate — Tomi/Zsombi/Peti). Not Curator. Censura has the final verdict and full pipeline context; a lesson written before the verdict would be misleading on RED tickets.

**Validation before writing:** Censura drafts the lesson internally, Senate personas agree or refine, then it's written. Not a separate step — part of Censura's closing deliberation.

**Where:**

- `censura-output.md` → mandatory closing section: draft lesson → Senate internal validate → write 1-2 bullets to `LESSONS.md`; applies on GREEN, YELLOW, and RED
- `senate.md` → context loading / pre-flight: load `LESSONS.md` before session opens; silent skip if file doesn't exist yet

**Retrospective trigger:** After each retrospective run, Censura appends a `---` divider with date to `LESSONS.md`. On every subsequent run, Censura counts entries since the last divider. When count reaches 10, Censura adds "Retrospective recommended" to its output. No separate counter — `LESSONS.md` is the state.

**Implementation note:** Senate reads the full file, no summarization. The divider approach makes retrospective cycles visible in the file itself.

---

## Item 2.3 — ADR Proposal

**What:** Every time Censura issues a GREEN verdict, it includes a mandatory ADR (Architecture Decision Record) proposal section — one entry per significant decision made during the ticket. Proposed with exact text; owner decides whether to commit it to `docs/decisions/`.

**Who writes:** Censura. Both ADR proposal and [LESSONS.md](http://lessons.md/) write are Censura output sections — different layers (architectural decision vs. process lesson), not overlap.

**Where:** `censura-output.md` → GREEN verdict block, mandatory ADR proposal section

**Implementation note:** ADR proposal appears only on GREEN — not on YELLOW or RED. [LESSONS.md](http://lessons.md/) write appears on all verdicts.

---

## Item 7.6 — Retrospective Session

**What:** A manually triggered session starter that reviews accumulated [LESSONS.md](http://lessons.md/) entries since the last `---` divider, surfaces patterns, and proposes process improvements. Owner runs it when Censura recommends it (every ~10 tickets). Methodology matures from experience — no rigid format enforced now.

**Where:** `session-starters.md` → new entry: Retrospective session

**Implementation note:** This session reads [LESSONS.md](http://lessons.md/) as its primary input, focusing on entries since the last divider. Senate-only deliberation — no pipeline execution agents involved.