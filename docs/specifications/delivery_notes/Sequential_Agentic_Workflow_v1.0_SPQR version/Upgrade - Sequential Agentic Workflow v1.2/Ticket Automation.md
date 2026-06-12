---

---
## Affected Files

- `docs/skills/ticket-slicing.md` — NEW
- `docs/skills/censura-ticketing-input.md` — NEW
- `docs/skills/censura-ticketing-discussion.md` — NEW
- `docs/skills/censura-ticketing-output.md` — NEW
- `docs/skills/quaestor-relatio-output.md` — UPDATE
- `docs/skills/censura-input.md` — UPDATE
- `docs/skills/censura-output.md` — UPDATE
- `docs/agents/senate.md` — UPDATE ⚠️ **shared with Group 3 — write once, covers both groups**
- `CLAUDE.md` — UPDATE (owner applies manually)

---

## Item #9 — [ticket-slicing.md](http://ticket-slicing.md/)

**What:** New shared skill file, two invocation modes. Quaestor “propose” mode: produces Ticket Proposals table (title, scope-in, scope-out, priority, dependency). Censura “validate + create” mode: validates each proposal against slicing criteria, PASS/REVISE/REJECT verdict per proposal, creates tickets in Notion on owner approval.

**Slicing criteria:** deliverable fits in one sentence · executor needs max 3–4 reference files · verifiable in isolation · no “and also” · no foundation + feature in same ticket · vertical over horizontal · independence rule.

**Priority logic:** Critical = blocks deployment or another ticket · Major = required for feature/pipeline · Minor = improvement or cleanup.

**REJECT flow:** Censura sends specific finding back to Quaestor session. Quaestor revises that proposal only — not a full spike rerun.

**Template behavior:** Template-first, not template-only. Agent fetches Notion template live by page ID. Can add sections if template has gaps; never delete or reorder existing sections; must flag any deviation.

**Where:** `docs/skills/ticket-slicing.md` — new file; prerequisite for #5, #6, #7, #10

**Implementation note:** `[PROJECT_BOUNDARIES]` placeholder in generic SPQR repo; Foodoire version replaces with iOS/SwiftData layer boundaries.

---

## Item #10 — Naming Convention Rule

**What:** Agents never invent ticket prefixes or numbers (SPIKE-XXX, DOC-XXX, or any other). Descriptive working title only during proposal. Owner assigns final prefix and number after creation.

**Where:**

- `CLAUDE.md` → Agent Workflow section — proposed text: *“Ticket naming: agents never invent ticket prefixes or numbers (SPIKE-XXX, DOC-XXX, or any other). Use descriptive working titles only. Owner assigns final prefix and number after creation.”* Owner applies manually.
- `docs/skills/ticket-slicing.md` → NEVER section — covered by #9

**Depends on:** #9

---

## Item #5 — [quaestor-relatio-output.md](http://quaestor-relatio-output.md/) Ticket Proposals Section

**What:** Add formal TICKET PROPOSALS output section. Quaestor proposes only — does not create. Output: table with title (descriptive working title), scope-in, scope-out, priority, dependency.

**Where:** `docs/skills/quaestor-relatio-output.md` — new TICKET PROPOSALS section; format per [ticket-slicing.md](http://ticket-slicing.md/)

**Depends on:** #9

---

## Item #6 — [censura-input.md](http://censura-input.md/) VERIFY Pass Extension

**What:** Add Quaestor ticket proposals as a VERIFY pass evaluation item. Censura checks proposals against [ticket-slicing.md](http://ticket-slicing.md/) criteria during the existing VERIFY pass — not a separate phase.

**Where:** `docs/skills/censura-input.md` — add to VERIFY pass items; reference [ticket-slicing.md](http://ticket-slicing.md/) for criteria

**Depends on:** #9

---

## Item #7 — [censura-output.md](http://censura-output.md/) Ticketing Phase Trigger

**What:** Add conditional ticketing phase trigger. Condition: GREEN verdict + spike requests tickets + owner approval. On trigger: context carries over to [censura-ticketing-input.md](http://censura-ticketing-input.md/); no new input loading. [censura-output.md](http://censura-output.md/) only contains the conditional trigger — ticketing phase content lives in the separate censura-ticketing-* files.

**Where:** `docs/skills/censura-output.md` — conditional trigger block; references [censura-ticketing-input.md](http://censura-ticketing-input.md/)

**Depends on:** #9

---

## Item #8 — [senate.md](http://senate.md/) Two-Phase Censura

**What:** Update CENSURA section: VERIFY (evaluation) → TICKETING (conditional, GREEN + owner approval). Context carry-over explicit — no new input loading between phases.

**Where:** `docs/agents/senate.md` — CENSURA section update

**Depends on:** #7

---

## New Files — censura-ticketing-input / discussion / output

**What:** Three new skill files for the Censura ticketing phase.

- `censura-ticketing-input.md` — loads [ticket-slicing.md](http://ticket-slicing.md/), Notion template IDs, evaluation setup
- `censura-ticketing-discussion.md` — per-proposal verdict deliberation (PASS / REVISE / REJECT)
- `censura-ticketing-output.md` — owner approval gate, Notion ticket creation, URL reporting

**Notion template IDs (inline in **[**censura-ticketing-input.md**](http://censura-ticketing-input.md/)**):**

- Spike: `36368d5de1e881d99814c8bcd8ab7e2d`
- Feature: `36368d5de1e88123b07cea3c40ea2cdf`
- Bug: `36368d5de1e881d4abccee5665a2ae80`
- Doc: `36868d5de1e8819dad83ed28239ea27e`
- Spike document template: `36c68d5de1e8819a824fdfdbb2afff1b`
- Spike doc parent (Exploracio/Spiking): `36c68d5de1e880368560e60a35097ee1`

**Where:** `docs/skills/` — 3 new files

**Depends on:** #9

---

## Changes Made

- `docs/skills/ticket-slicing.md` — NEW: two-mode slicing skill (QUAESTOR PROPOSE + CENSURA VALIDATE+CREATE), Foodoire PROJECT_BOUNDARIES, self-check, NEVER section
- `docs/skills/censura-ticketing-input.md` — NEW: ticketing phase entry, Notion template IDs inline, context carry-over rule, load order
- `docs/skills/censura-ticketing-discussion.md` — NEW: PASS/REVISE/REJECT verdict per proposal, verdict list before proceeding
- `docs/skills/censura-ticketing-output.md` — NEW: owner approval gate, Notion creation, reject protocol, bug ticket exception
- `docs/skills/quaestor-relatio-output.md` — UPDATE: TICKET PROPOSALS section added after spike doc creation; NEVER rule updated (propose only, never create in Notion)
- `docs/skills/censura-input.md` — UPDATE: [ticket-slicing.md](http://ticket-slicing.md/) added to LOAD ORDER (#6); ticket proposals check added to PRE-CHECK
- `docs/skills/censura-output.md` — UPDATE: TICKETING PHASE TRIGGER added (GREEN + proposals + owner approval); old TICKET CREATION replaced with EMERGENT GAPS
- `docs/agents/senate.md` — UPDATE: CENSURA two-phase model (VERIFY/TICKETING) in MODES; STAGE SKILLS and PIPELINE line updated
- `CLAUDE.md` — PENDING: naming convention rule proposed, owner applies manually