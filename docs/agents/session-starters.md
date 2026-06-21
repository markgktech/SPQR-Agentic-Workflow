SESSION STARTER — SPQR v1.5
One template. Replace [AGENT] and [TICKET_URL] each time.

PASTE PROMPT
Load docs/agents/[AGENT].md
Begin input phase.
Ticket: [TICKET_URL]
Project is located at: [PROJECT_PATH]

AGENT NAMES
senate / quaestor / praetor / tribunus / probator / curator

TICKET ID
`<TICKET-ID>` resolves to the consuming project's ticket id (Foodoire → FDP-N; `DEV-XXX` is a legacy alias). The executor agent (Praetor for DEV, Quaestor for SPIKE/DOC) creates the ticket hub + handover file in the work_documents/ vault at session start if missing.

WARP TAB NAME
<TICKET-ID> — [Agent]

PRAETOR PRE-STEP (before pasting prompt)
Ensure the repo is on main and clean. Praetor auto-opens the ticket branch (feature/<TICKET-ID>-slug) before coding — mechanics in docs/skills/git-workflow.md. If a branch already exists for the ticket, Praetor stops and asks owner.

SENATE PRE-STEP — WAREHOUSE WAKE (before pasting a Senate prompt; owner-operated)
Surface warehouse state so the Senate's INGEST JUDGMENT + heat review have their input (daemon-free — the Senate agent runs `list-pending`/`audit` on session-open and surfaces the result, agent-executed on owner HITL):
- Antechamber pending-check — `python3 -m warehouse_robot list-pending --warehouse-root [WAREHOUSE_ROOT] --state pending-senate` — lists the proposals awaiting Senate judgment (read-only; reads the antechamber sidecars, not the mirror). `check` is a divergence check (dir vs mirror), NOT a pending lister — do not use it for the wake.
- Audit heat — `python3 -m warehouse_robot audit --warehouse-root [WAREHOUSE_ROOT]` — surfaces open structural flags + per-node heat (exit 1 = findings exist).
Paste the output (or "none pending / no open flags") into the session. The Senate judges each pending proposal; the owner then authorizes the privileged `resolve`/`grant` (HITL — the Senate executes on the owner's go).

---

DEBUGGING TRIBUNUS — STANDALONE
Load docs/agents/tribunus.md
Load docs/skills/debugging-tribunus-input.md
MODE: STANDALONE DEBUGGING
Issue: [describe the bug or test failure]
Relevant files: [list suspect or changed files]
Project is located at: [PROJECT_PATH]

WARP TAB NAME
<TICKET-ID> — Tribunus Debug

---

CORRECTIO — BUG FLOW (owner-launched, handover-driven)
The owner moves the Notion bug ticket through stages and launches each hop as a fresh session; context flows via the local handover (D20, D23). Default 2 hops: Praetor (investigate → HITL cause-note gate → fix) → Probator (verify + close). Conditional inserts: [investigator →] before Praetor, [→ Tribunus-review] / [→ Curator] after, [→ Censura iff decision].

PASTE PROMPT — Praetor (bug executor)
Load docs/agents/praetor.md
Load docs/skills/bug-pipeline.md
MODE: CORRECTIO (bug) — investigate-first, STOP at the HITL cause-note gate before any code
Ticket: [TICKET_URL]
Project is located at: [PROJECT_PATH]

PASTE PROMPT — Probator (verify + close)
Load docs/agents/probator.md
Load docs/skills/bug-pipeline.md
MODE: CORRECTIO (bug) — verify repro pre/post, tests, conditional regression test, write close + routine knowledge entry
Ticket: [TICKET_URL]
Project is located at: [PROJECT_PATH]

Escalation hops (conditional): investigator → use the DEBUGGING TRIBUNUS — STANDALONE starter (CORRECTIO investigator mode); Tribunus-review / Curator → their standard OPUS starters on the same fix/ branch.

WARP TAB NAME
<TICKET-ID> — [Agent] (CORRECTIO)

PRAETOR PRE-STEP (CORRECTIO)
Repo on main and clean. Praetor opens the bug branch (fix/<TICKET-ID>-slug) ONLY after the HITL cause-note gate clears — not before. If a branch already exists for the ticket, Praetor stops and asks owner.

---

WAREHOUSE MAINTENANCE — OWNER-DRIVEN STARTERS (D6b — daemon-free, run when the owner authorizes)
Four standalone owner touches, distinct acts (do not conflate): `audit` detects structural conditions → emits flags; the retro harvest reads open flags + heat → trend; the flag-resolution sweep closes a handled flag; the semantic audit is the owner's contradiction review. The robot writes files but never runs git — the owner commits.

AUDIT RUN (structural tripwires)
`python3 -m warehouse_robot audit --warehouse-root [WAREHOUSE_ROOT]`
Exit 0 = clean (no open flags) · 1 = findings exist · 2 = robot error (run `reconcile` first). Re-running over a standing condition is a no-op, never a duplicate.

ANTECHAMBER PENDING-CHECK (what awaits Senate judgment)
`python3 -m warehouse_robot list-pending --warehouse-root [WAREHOUSE_ROOT] --state pending-senate`
Lists the proposals awaiting Senate judgment (read-only, straight from the sidecars); feeds the SENATE PRE-STEP wake above. (`check` reports antechamber dir-vs-mirror divergence only — it is not a pending lister.)

FLAG-RESOLUTION SWEEP (close a handled flag — agent-executes-on-owner-HITL, D3)
After a flag's underlying condition is genuinely handled, the owner authorizes clearing it by ingesting a node carrying a `resolves` edge to the flag (via `docs/skills/warehouse-ingest.md`). The retro SURFACES open flags/heat; it does not write — resolution is a write-path act on explicit owner go. Never sweep a flag whose condition still holds (a recurrence after resolution is a real new finding).

SEMANTIC AUDIT — "REVIEW THIS" (owner-driven contradiction review)
The structural `audit` is graph-shaped only; the semantic / contradiction pass is owner-driven. Paste the candidate scope's nodes into a Senate-style review session and ask: does any active node contradict another? A confirmed contradiction is resolved by a **superseding** decision proposal (append-only — never an in-place edit), routed through the antechamber. Full semantic-audit automation is out of scope (later ticket).

---

PERSONAS
Name 1: [Name 1]
Name 2: [Name 2]
Name 3: [Name 3]
Name 4: [Name 4]

Load this section when invoking a Senate or Quaestor agent.
If no persona-carrying agent is invoked: skip.
