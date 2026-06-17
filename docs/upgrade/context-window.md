MASTER SESSION
Save at natural stopping points: after each roundtable, after each decision cluster, after each group closes. Frequency is judgment-based, not scheduled — goal is no work re-derivable from scratch if session ends unexpectedly.
The recording target is the run container (the work record under docs/spqr_self/upgrades/<version>/), not central memory.
Before compacting: verify that the run container captures all open decisions.
Use /clear between groups when no carry-over state is needed.
Headroom check before each new group: estimate group size (file count × average change scope) vs free headroom. Percentage alone is not sufficient.
The run container is the external record — the master session can be reconstructed from it if context is lost.

EXECUTION SESSION
Each execution session starts fresh from the brief. No session memory carried from previous groups.
If a group is large enough to risk context exhaustion mid-execution, split it before launching.
Before hitting the context limit: write a partial Changes Made entry in the group sub-md and a status note so the session can be resumed.

COMPACT PROTOCOL
1. Record any unsaved decisions in the run container first.
2. Ensure the run container reflects current state.
3. Run /compact [what we are doing and what remains] — the note is the continuity anchor; not optional.
4. Next session loads the run container to reconstruct context — does not re-derive documented state.

NEVER
- Compact without recording decisions in the run container first
- Compact without a context note in /compact args
- Re-derive decisions already documented in the run container
- Start a new group when headroom is insufficient for it
