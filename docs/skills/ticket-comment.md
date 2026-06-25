HANDOVER BLOCK — SHARED PROTOCOL
Keep the block terse — a routing/signal record; detail belongs in the output doc, not here (no fixed line count). One block per stage. Append at stage completion — not only at session end.
Transport (D2): append a `---`-delimited block to `<TICKET-ID>_handover.md` in the ticket's work_documents vault — NOT a Notion comment. The work-trace is local. The field contract below is PRESERVED verbatim; only the transport changed.

APPEND MECHANICS
The executor agent creates `<TICKET-ID>_handover.md` if it does not exist: frontmatter `up: "[[<TICKET-ID>]]"` + `tags: [content/handover]`, then a `## <TICKET-ID> Handover Chain` heading and an `*Append-only.*` note. Backfill invariant (D7): any agent that finds the file missing creates it.
To append: locate the last `---` block in the file, add a new `---` delimiter, then the block header `### <Agent> — <verdict> | <date>` followed by the fields below. Never overwrite or edit a prior block — append only (D10).

FORMAT
session_id: [claude_cli_conversation_id]
still_solving: [one sentence — ticket goal]
mode: [PRAETOR | TRIBUNUS | PROBATOR | CURATOR]
approach_before_consilium: [Praetor only — 1-2 sentences, independent approach before Consilium load]
consilium_addressed: [Praetor only — one-line summary; detail in output KEY DECISIONS]
addressed: [confirmation prior expected_outputs were met — empty on first Praetor block]
expected_outputs: [changed file list — detail in output FILES CHANGED]
impl_doc: [Praetor only — local `<TICKET-ID>_output.md` path]
receipt: [producer only — verbatim decisive tool-output `<command> → <decisive stdout line>` per build/test/lint/warehouse-write claim; see FIELD RULES for the scoped definition]
warehouse_trace: [immutable pointer to this stage's warehouse interaction — the query `--session` id / last-round ref, or `n/a` if none; see FIELD RULES]
warehouse_delta: [terse one-line disposition pointer — `none | candidates | proposals | deferred`; the FULL `## Warehouse Delta` section lives in the session's separate output doc when it produces one, otherwise in this block (D2b — see WAREHOUSE DELTA — SHARED); see FIELD RULES]
routing: → [next agent | OWNER]

FIELD RULES
session_id: always present; retrieve own value via `echo $CLAUDE_CODE_SESSION_ID` (Bash) at block-writing time; if the env var is unset, record `unknown` — never drop the field
approach_before_consilium: Praetor only; omit for all other agents
consilium_addressed: Praetor only; one-line summary only — full detail belongs in the output file; omit for others
impl_doc: Praetor only; must be present before routing — reviewers load on-demand; points to the local `<TICKET-ID>_output.md`; omit for others
addressed: empty on first block in a pipeline run; required on all subsequent blocks
receipt: CANONICAL definition — defined ONCE here (D2); the producer/enforcer skills reference this, they do not restate it. A receipt binds every build/test/lint claim to verbatim tool evidence: `<command> → <decisive stdout line>`, copied exact — NOT paraphrased. Scoped to the decisive line, not the full log. Whitelist: build succeeded · tests ran + result · lint zero-warnings (e.g. `BUILD SUCCEEDED`, `Executed 42 tests, 0 failures`, `0 violations`). **Warehouse-write claims extend this discipline (D4):** a `propose`/`revise`/`resolve` claim carries its verbatim CLI verdict line (`<command> → <state + proposal key>`, e.g. `propose … → pending-senate demo-k7`); the `→ <state + proposal key>` is the **decisive `state`+key read from the CLI's JSON output** (the write verbs emit JSON, not plain text — the receipt records that one decisive pair in the same readable `<command> → <result>` convention as the build/test receipts, not raw stdout) — the immutable, within-pipeline proof that the write was attempted and how the gate ruled (verification-on-handoff; the canonical definition also lives in `warehouse-ingest.md` RECEIPT, which references this). Producers: Praetor (build + lint), Probator (test); warehouse-write producers = any agent that runs `propose`/`revise` (Praetor, Quaestor, Censura, Probator-narrow) and the Senate's owner-HITL `resolve`. Senate runs no build/test shell → Censura produces no build/test receipt (enforcer only) but DOES carry a warehouse-write receipt for its lesson proposal. Praetor's verbatim build/lint lines live in `<TICKET-ID>_output.md` VERIFICATION (RECEIPT) and the handover field carries the compact decisive line(s); Probator (no output doc, D14) puts its decisive test line directly in this field. **Write-gate receipt (SAW-55):** a warehouse-MUTATING session (`propose`/`revise`/`resolve`, or a manifest/scope-vocabulary edit) additionally records its clean-gate evidence in this same receipt — (a) command run + (b) exit code, (c) the final `check` result (clean/divergent), (d) pending/proposed count if relevant, (e) whether a non-fresh `reconcile` was needed, and (f) explicit confirmation that no `--fresh` was used. These are part of THIS receipt rule, not a separate block (the clean-gate path is `warehouse-usage.md` §5). Censura validates presence (C-55). Omit only on a block that makes no build/test/lint/warehouse-write claim.
warehouse_trace: immutable within-pipeline POINTER to this stage's warehouse interaction — the query `--session` id and/or last round ref (the trace handle), or `n/a` if the stage touched no warehouse. One line; a pointer, not a transcript — round detail lives in the trace table, the write proof lives in `receipt:`. Do NOT carry mutable antechamber status here: current pending-proposal state is stale-by-construction in an append-only block and lives authoritatively in the antechamber queue (`check` / the session-starter pending-check) — there is deliberately no `antechamber:` status field (D4 LEAN).
warehouse_delta: one-line disposition pointer mirroring `warehouse_trace:`'s terseness — `none | candidates | proposals | deferred`. A pointer, not the delta: the FULL `## Warehouse Delta` section (structure below) lives in the session's separate output doc when it produces one, and IN THIS BLOCK when it does not (D2b — artifact-based, never role-based; see WAREHOUSE DELTA — SHARED). Required on every close-out block; `none` is valid only with the rationale carried in the full section. Omit only when the session writes no close-out.
routing: name next agent explicitly; use OWNER if pipeline ends or HITL checkpoint reached

CONSTRAINTS
Never bloat the block — keep it a terse routing/signal record; push detail to the output doc
Never omit session_id
Never omit expected_outputs
Never omit routing
Never omit a receipt on a build/test/lint/warehouse-write claim to save tokens — it is a quality floor (cost-guard C6), never optional; a missing receipt is bounced at Censura
Never add an `antechamber:` status field — mutable pending state is stale-by-construction here; it lives in the antechamber queue (D4 LEAN)
Never omit impl_doc on Praetor block — the local `<TICKET-ID>_output.md` must exist before the block is appended
Never append mid-implementation — only at stage completion checkpoints
Never carry forward prior agent opinions in your own block fields
Never overwrite or edit a prior block — the handover file is append-only

---

HUB CLOSE-OUT — SHARED (SAW-56)
CANONICAL definition — defined ONCE here (D1, mirrors the SAW-26 `receipt:` precedent); the per-agent `*-output.md` skills reference this, they do not restate it. Every agent session updates the ticket hub before stopping WHEN A HUB EXISTS — the close-out is part of the session contract, not optional. Backfill invariant (D7): if the hub is missing, create it from template before finishing, then write the row.

SESSION ROW — required fields (D2 — the hub `## Session / cost` table)
role: [session role/agent — e.g. Praetor, Senate Censura]
phase: [stage/phase — e.g. OPUS Praetor, EXPLORACIO, Censura VERIFY]
session_id: [own `$CLAUDE_CODE_SESSION_ID`; `—` if the agent runs no shell, e.g. Senate]
verdict: [verdict/status this session closes with — GREEN | YELLOW | RED | routed | done]
artifacts: [links to this session's handover/output artifacts — `<TICKET-ID>_handover.md` block, `_output.md`]
routing: [next routing / owner action — next agent | OWNER]
cost: [cost/token total — or the placeholder per the rule below]

COST PLACEHOLDER RULE (D2)
If exact cost/tokens are unavailable at close, write the explicit placeholder `owner-fill` (pending owner entry) — NEVER omit the session row to avoid the missing number. A missing cost figure is owner-filled later; a missing row is a broken session contract.

HUB = NAVIGATIONAL (D2)
The hub records status, session lineage, routing, and links — it is a navigational index, not an evidence store. Detailed receipts/evidence belong in the handover block / output doc, NOT in the hub. Do not overload the hub row with detail that lives in the handover.

CONSTRAINTS
Never stop a session without updating the hub when a hub exists — the row is part of the session contract
Never omit the session row to avoid a missing cost number — use `owner-fill`
Never overload the hub with detailed evidence — keep it navigational; detail lives in handover/output

---

WAREHOUSE DELTA — SHARED (SAW-54)
CANONICAL definition — defined ONCE here (D1, mirrors the SAW-26 `receipt:` precedent); the per-agent `*-output.md` skills reference this, they do not restate it. Every session close-out MUST declare its warehouse-relevant knowledge change — a missing Warehouse Delta is a close-out defect. The terse `warehouse_delta:` handover field (FORMAT above) is the pointer; the FULL `## Warehouse Delta` section is the declaration.

FULL SECTION STRUCTURE (`## Warehouse Delta`)
- Status: `none | candidates-present | proposals-authored | deferred` — the disposition this close-out reaches.
- Changed knowledge — what durable knowledge this session touched, bucketed: Decisions / Constraints / Lessons / Supersedes. Empty buckets omitted.
- Recommended disposition — what should happen to each candidate (author antechamber proposal / defer to owner / no action), per candidate. Candidates carry a recommendation, NEVER an automatic ingest.
- Owner-facing summary — one or two plain sentences an owner can act on without reading the trace.

EXPLICIT `none` RULE (item 2)
`Status: none` is valid ONLY with a one-line rationale stating why no durable decision/constraint/lesson/supersession was introduced. Missing Warehouse Delta is a close-out defect; bare `none` (no rationale) is the same defect. Censura validates this (C-54).

D2b — LOCATION FALLBACK (artifact-based, NOT role-based)
The home of the FULL `## Warehouse Delta` section depends on whether THIS session actually produces a separate output document — never on agent role:
- Session DOES produce an output doc → the full section lives in the OUTPUT DOC close-out; the handover block carries ONLY the terse `warehouse_delta:` pointer.
- Session does NOT produce a separate output doc → the full `## Warehouse Delta` section MUST live in THIS handover block itself, regardless of agent role. A session may NOT omit the full delta just because it wrote no output doc.
Note: do not infer Warehouse Delta placement from agent role. If the session writes a separate output artifact, the full Warehouse Delta lives there and the handover carries only the `warehouse_delta:` pointer. If the session writes only a handover block, the full Warehouse Delta lives in that handover block.

CONSTRAINTS
Never close a session without a Warehouse Delta — its absence is a close-out defect bounced at Censura
Never write bare `none` — `none` is valid only with a one-line rationale
Never auto-ingest a candidate — a Warehouse Delta records a recommended disposition; ingest requires owner approval (warehouse-ingest.md)
Never let a session that writes no separate output doc drop the full delta — D2b puts it in the handover block
