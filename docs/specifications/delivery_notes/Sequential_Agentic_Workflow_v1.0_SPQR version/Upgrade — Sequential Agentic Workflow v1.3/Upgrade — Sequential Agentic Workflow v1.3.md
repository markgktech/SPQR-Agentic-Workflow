---

---
## Summary

- **v1.1:** feedback loop + agent hardening foundation
- **v1.2:** ticket creation automated, agent hygiene hardened, SPQR repo decoupled — *within* the existing pipeline
- **v1.3:** extends the pipeline (retrospective back end), lowers its running cost, and closes two trust gaps. First new agent (Retrospector) since the core pipeline; the Intake agent is **deferred** (depends on the ticket-convention work — SAW-2 / SAW-8).

---

## Why now

- **Ideas get lost** — ad-hoc mid-session ideas have no low-friction capture path → deferred or forgotten *(DOC-12 — itself deferred to a later batch; depends on SAW-2 / SAW-8)*
- **Learning isn't systematized** — the retro works but lives *outside* SPQR; not reproducible or in-repo *(DOC-18)*
- **Running cost grew materially v1.1→v1.2** — doc growth, more ADRs, the new skills layer, two-phase Censura; no fetch discipline anywhere *(DOC-14)*
- **Two trust gaps surfaced in SPIKE-007** — Censura didn't stop for owner check-in despite a triggering gap *(DOC-15)*; Quaestor inherited an unverified external claim as fact *(DOC-16)*
- **Sessions aren't resumable** — no record of which CLI session produced a checkpoint comment *(DOC-17)*

---

## Scope — 3 categories

1. **Pipeline Extensions** — RETROACTIO retro back end *(DOC-18)*  ·  *(DOC-12 idea intake deferred — depends on SAW-2 + SAW-8; rides a later batch)*
2. **Reliability / Trust Hardening** — Censura stop-branch *(DOC-15)* · Quaestor claim verification *(DOC-16)*
3. **Operational Quality** — fetch strategy / token cost *(DOC-14)* · session_id resumability *(DOC-17)*

---

## Execution note

Every v1.3 change lands in **Foodoire first, then syncs** to the generic SPQR repo — no SPQR-only items. Each ticket's *approach* is decided per-topic before implementation; this page frames problems and value, not solutions.

[[1. Pipeline Extensions]]

[[2. Reliability - Trust Hardening]]

[[3. Operational Quality]]

[[4. SPQR Repo Sync]]

---

## Status — v1.3 execution complete

All execution groups done (Foodoire-first → SPQR sync):

- **Group 1 — RETROACTIO** (DOC-18) ✅ — 5 `docs/retro/*` files; folder-pipeline session-starter
- **Group 2 — Reliability / Trust Hardening** (DOC-15 stop-branch · DOC-16 verify) ✅
- **Group 3 — Operational Quality** (DOC-14 fetch hygiene · DOC-17 session_id) ✅
- **Group 4 — SPQR Repo Sync** ✅ — generic copies + placeholders; grep verified (zero hardcoded names / Notion IDs)

Per-group file-by-file changes live on each sub-page; all 5 tickets checkpoint-commented (session_id, routing → OWNER). **Repo changes in both repos are uncommitted — owner-only commit pending.**

## Deferred / spun off

- **DOC-12 (Intake)** — **deferred** out of v1.3; its create-step depends on SAW-2 (routing) + SAW-8 (templates/naming). Decided direction preserved; rides a later batch.
- **Spun-off SAWs (roadmap):** residue-pruning · gate audit & gate semantics · scalable knowledge representation (SAW-13) · self-building governance (north-star) · parking (sorting agent + A2A orchestrator) · README iOS-tooling residue.
- **Remaining wrap edits (owner / quick exec):** README v1.3 version-history entry + `AGENT_LAWS.md` SCOPE `v1.2 → v1.3` (both repos) — not yet applied.

[[5. Branch Strategy]]