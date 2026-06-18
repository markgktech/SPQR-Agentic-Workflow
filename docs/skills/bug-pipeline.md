---
name: bug-pipeline
description: CORRECTIO — the lean bug-type flow. Routing axes, the default 2-session shape (Praetor investigate-first → HITL cause-note gate → fix; Probator verify+close), escalation, the decision-triggered Censura, and the reused veto/revision path. Orchestration doc — the bug-mode branches live in the agent mandates; this file is the single coherent model they point at.
---

CORRECTIO — the bug-type pipeline. Distinct from OPUS (feature) and EXPLORACIO (spike): right-sized, not full feature ceremony. Reuses existing primitives (Praetor, Probator, conditional Senate/Tribunus/Curator) at owner-set effort. Bug tickets are owner-initiated only (`Ticket type = Bug`, see ticket-slicing.md). Hops are owner-launched and handover-driven — the owner moves the Notion ticket through stages and starts each session; agents read the ticket, never write Notion properties (D20).

LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text) + `<TICKET-ID>_handover.md` + `<TICKET-ID>_output.md` if they already exist
4. This file (bug-pipeline.md) — the CORRECTIO model
5. The active agent's stage skill (praetor-input.md / probator-input.md …) — the bug-mode branch in the agent mandate points here
6. In the veto/revision path only: collegium-veto.md + praetor-revision.md (reused, not redefined — D26)

ROUTING — two axes (both already on the hub identity block)
Axis 1 — entry: wild | dev-linked.
  dev-linked — cause near a known recent change (`spawned_by` set) → light triage folds into Praetor.
  wild — unknown origin → may need a dedicated investigation stage before Praetor (see ESCALATION).
Axis 2 — severity: HIGH | MED | LOW (existing hub vocabulary — never sev1/2/3, D9). Drives owner model/effort choice + conditional re-entry.

DEFAULT FLOW — 2 sessions (D2)
owner files bug → Praetor (investigate-first → HITL cause-note gate → fix) → Probator (verify + close).
Leanest shape that still preserves one independent check (Probator). Triage folds into Praetor as a structural investigate-first gate (D3) — no standing separate triage/Tribunus stage. Consilium, Tribunus code-review, and Curator are cut from the default (D5) and re-enter only on the triggers below.

BUG handover-chain (D23): `[investigator →] Praetor → [→ Tribunus-review] Probator [→ Curator] [→ Censura iff decision]`.

PHASE BOUNDARIES (each phase a cold-start session — Law 3)
Mirrors OPUS/EXPLORACIO: distinct input → work/HITL → output phases, never collapsed.

  PHASE 1 — Praetor: investigate-first → HITL cause-note gate → fix (D3, D4)
    a. INVESTIGATE (no code): draft `<TICKET-ID>_output.md` from bug_output_template — SYMPTOM/REPRO + ROOT CAUSE; set hub identity (severity, entry, affects); state the proposed FIX direction; size the ticket (D17, informs the owner model/effort call).
    b. HITL CAUSE-NOTE GATE — the canonical phase boundary (modelled on Consilium's owner-closes-discussion gate). Praetor reports the cause-note to the owner and STOPS. No code is written until the owner explicitly signs off. This is the bug flow's single mandatory HITL.
    c. FIX (only after sign-off): open `fix/<TICKET-ID>-slug` (git-workflow.md), implement, update `<TICKET-ID>_output.md` (FIX · VERIFICATION evidence Praetor can give) + append the Praetor handover block.

  PHASE 2 — Probator: verify + close (D6)
    Verify repro pre-fix (must reproduce) + post-fix (must not), evidenced in the handover. Run tests. Add a regression test unless excused (D6b). Write the close + the routine knowledge entry (D8). May raise `decision: yes` at close (D7b).

HITL CAUSE-NOTE GATE (hard gate)
The owner = fresh eyes; this gate is what a separate investigator would otherwise buy (anchoring-bias-free root cause). Never close it without an explicit owner signal (Law 2). The cause-note lives local (D14) — `<TICKET-ID>_output.md` ROOT CAUSE + hub identity — not a Notion comment.

PROBATOR CLOSE (D6, D6b, D8)
- Repro evidence: pre-fix reproduces, post-fix does not — both recorded in `<TICKET-ID>_handover.md`.
- Tests run; results cited per changed path.
- Regression test: REQUIRED unless the owner has tagged the ticket `no-repro-harness` / "untestable because X" (recorded on the hub) — D6b. The trigger is owner-set, not agent-discretionary.
- Routine knowledge entry: always written at close to the project-knowledge sink (D8) — today LESSONS.md; soon the Warehouse (v1.5). The sink is abstract — swapping it is a one-line change; do not hardcode a path beyond "the project-knowledge sink".

DECISION FLAG → conditional Censura (D7, D7b)
decision = a choice a future ticket's agent would behave differently knowing. `decision: yes` is raisable by whoever first sees it — Praetor at the HITL gate, or Probator at close. The owner confirms. On a confirmed `decision: yes`, Censura (Senate) runs ONLY to expand the repo project-knowledge sink — knowledge-base expansion, NOT a quality gate for the fix. Routine lessons never need Censura; they are written at close by Probator. There is no standing bug review gate.

ESCALATION TRIGGERS (mechanical only — D11)
- entry=wild AND Praetor reports "cause not localizable" → + investigator BEFORE Praetor (see INVESTIGATOR SELECTION).
- severity=HIGH OR the fix touches a critical surface → + Tribunus code-review AFTER Praetor.
- Curator → ONLY if the fix touches deploy / config / runtime (D11).
- Censura is never triggered by severity. A bug too big for this flow is re-filed as a feature (it earns ceremony as OPUS) — not escalated in place.

INVESTIGATOR SELECTION (D12)
Default: Tribunus standalone-debug (code-near, existing primitive — debugging-tribunus-input.md), producing a structured fix-spec (repro · root-cause file:symbol · proposed change · blast radius).
Mechanical escalation: if Tribunus returns "root cause not localizable to a file/subsystem" → the owner files a normal EXPLORACIO spike ticket (genuine research); Quaestor runs the standard spike flow. There is NO in-CORRECTIO quaestor mode — quaestor.md is unchanged.

VETO / REVISION PATH (D26 — reused, not new)
When Probator's verification fails (repro persists post-fix / tests fail): Probator raises intercessio → praetor-revision → re-verify. This REUSES the OPUS veto/revision mechanic — load collegium-veto.md (format) + praetor-revision.md (fix scope, delta doc `<TICKET-ID>_output_revN.md`). No new mechanic. One veto per run, single issue, MED/HIGH HITL before posting — all per the reused skills.

EDGE / TERMINAL STATES (D16)
- not-a-bug → triage re-routes to OPUS/EXPLORACIO, or closes invalid.
- can't-reproduce → owner-close terminal state + reopen affordance.
- reopened-after-close → spawn a NEW linked ticket (`spawned_by` the original) for trace integrity — never a re-run of the closed ticket.
- bug found mid-feature work → always a separate owner-initiated bug ticket (entry=dev-linked, spawned_by the parent); Praetor never fixes a pre-existing bug inline (D15).

DOC LAYOUT (D18, D19)
Bug folder: `dev_logs/correctio_outputs/<FDP-N>_<Title>/`. Praetor creates the hub (`<TICKET-ID>_<title>.md`, uncomment the BUG identity block) + `<TICKET-ID>_output.md` (from bug_output_template) + `<TICKET-ID>_handover.md`. Probator appends its handover block. Censura (if triggered) appends + writes the knowledge entry. Reviewer notes live in `_handover.md` only — never in the output doc.

MODEL / EFFORT (D10 — descoped, dimension only)
Model and effort are owner-selected per bug at runtime, guided by severity / entry. No tiers are pinned here. Non-binding heuristic only: diagnosis-heavier on wild / HIGH bugs. Reopenable as a later SAW if fixed routing is wanted.

NEVER / CONSTRAINTS
Never write code before the owner signs off the cause-note at the HITL gate (Law 2)
Never close the HITL cause-note gate without an explicit owner signal — "let's move on" is not sign-off (Law 2)
Never carry state across phases — each phase is a cold-start session driven by the handover (Law 3)
Never skip the handover block at phase completion (Law 3)
Never collapse investigate and fix into one step — the cause-note gate is structural, not optional (Law 1)
Never escalate via severity into Censura — too-big re-files as a feature; Censura is decision-triggered only
Never run an in-CORRECTIO quaestor mode — non-localizable cause exits to a normal EXPLORACIO spike ticket (D12)
Never invent a new veto mechanic — reuse collegium-veto.md + praetor-revision.md (D26)
Never write Notion properties — agents read the ticket; the owner moves it through stages (D20)
Never fix a pre-existing bug inline during feature work — file a separate bug ticket (D15)
Never issue a silent clean pass at any stage — declare findings or an explicit "no findings" (Law 4)
