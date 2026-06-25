---
type: poc
title: "SAW-54/55/56 — Session Close-Out & Write-Gate Hardening"
decides: "How three additive close-out mandates compose in the shared handover protocol + Censura, without collision"
status: done
date: 2026-06-25
tags: [poc, decision]
---

# SAW-54/55/56 — Session Close-Out & Write-Gate Hardening — PoC

## Context / question
Three FDP-56-triggered process-hardening tickets land together, all generic-side:

- **SAW-54** — Require Warehouse Delta Close-Out (every session declares warehouse-relevant knowledge change; `none` allowed with rationale; no auto-ingest; Censura validates).
- **SAW-55** — Clean Warehouse Write Gates (pre/post-write `check`, non-fresh `reconcile` recovery, `--fresh` owner-only, write-gate receipts; Censura can YELLOW a missing receipt).
- **SAW-56** — Require Hub Session Close-Out (deterministic hub session/status row, cost placeholders, hub=navigation / handover=evidence; Censura validates hub/handover agreement).

Each ticket carries its own exact text/diff, so there is **no open design question** — roundtable (Phase 2) and the decision-making session (Phase 3) are **dropped per owner**. The ONE thing the tickets do not individually settle is **cross-ticket composition**: all three add (a) a required element to the session close-out and (b) a Censura checklist item, landing in the same small set of shared files. This PoC records only those reconcile decisions, so the composition is not lost (Law 3).

## Findings — shared-target map
Tier-0 (all three tickets write here): `docs/skills/ticket-comment.md` (canonical HANDOVER protocol), `docs/agents/senate.md` (Censura), `docs/skills/censura-output.md` (Censura checklist).
Tier-1 overlap: `docs/skills/warehouse-ingest.md` — SAW-54 (owner-approval-before-ingest) **and** SAW-55 (write-gate discipline).
Tier-1 exclusive: SAW-55 → `docs/skills/warehouse-usage.md`. SAW-56 → hub `## Session / cost` row contract.

Architecture precedent: **SAW-26 receipt rule** already established the pattern — a close-out rule is *defined ONCE* in `ticket-comment.md`, and producer/enforcer skills *reference* it (DRY, D2). The existing handover block already carries `receipt:` and `warehouse_trace:` fields and the hub already has a `## Session / cost` table. So these three are extensions to an existing structure, not new scaffolding.

## Recommendation / decision

**D1 — Canonicalize, don't scatter.** Each mandate is defined ONCE in `ticket-comment.md` (the shared handover protocol), mirroring SAW-26. Per-agent `*-output.md` skills are NOT each rewritten; at most a one-line pointer is added where an agent would otherwise not act. No full-rule restatement (DRY).

**D2 — Composition: distinct homes, no mega-block.** SAW-56 is explicit that the hub is navigational and evidence lives in the handover. Therefore:
- **Hub (`## Session / cost` row)** ← SAW-56: status, session_id, role, verdict, artifact links, routing, cost placeholder (`owner-fill`).
- **Handover block / output close-out** ← SAW-54 Warehouse Delta + SAW-55 write-gate receipt (both are evidence).
- The full `## Warehouse Delta` section lives in the **output doc** close-out; the handover block carries a terse one-line `warehouse_delta:` pointer (mirrors the existing `warehouse_trace:` pattern), keeping the block a terse routing record.
- The write-gate receipt **extends the existing `receipt:` discipline** (SAW-55 fields: command, exit code, final `check` result, reconcile-needed, no-`--fresh` confirmation) — it is not a separate block.

**D3 — Censura checklist: three separate, single-purpose items in a stable order.** No shared line. Fixed order so agents do not contend:
1. `C-56` — hub session/status row exists, references correct handover/output artifacts, matches routing/verdict.
2. `C-54` — Warehouse Delta present + credible; `none` only with rationale; candidates dispositioned (no auto-ingest).
3. `C-55` — write-gate receipt present for any warehouse-mutating session; YELLOW/FAIL if missing.

**D4 — Execution = serialized, section-owned (per owner).** Order **56 → 54 → 55**; later agent rebases on the prior agent's applied edits. Rationale for order: 56 hardens the hub/close-out skeleton first; 54 adds the Warehouse Delta section to the close-out; 55 extends the receipt discipline last. Each agent owns ONLY its labeled section/field/checklist-item and never edits another ticket's. `warehouse-ingest.md` (54∩55 overlap): SAW-54 adds the owner-approval-before-ingest note; SAW-55 adds the write-gate discipline — distinct anchors, serialized.

**D5 — No auto-ingest, no `--fresh`, no Foodoire.** Generic-side only; Foodoire reference-only. No automatic warehouse ingest (54). `--fresh` stays owner-authorized only (55). Owner commits.

**D6 — Acceptance stays per-ticket.** Each group sub-doc maps to its own ticket's Acceptance Criteria; not merged.

---

## Owner amendments (2026-06-25, pre-execution)

**D2b — Warehouse Delta location fallback (refines D2; ARTIFACT-based, owner-clarified 2026-06-25).** The full `## Warehouse Delta` section's home depends on whether THIS session actually produces a separate output document — never on agent role:
- Session DOES produce an output doc → full section in the output doc close-out; handover carries only the terse `warehouse_delta:` pointer.
- Session does NOT produce a separate output doc → the full Warehouse Delta section MUST live in the handover block itself, regardless of role. No session may omit the full delta just because it wrote no output doc.
The rule keys on the artifact, never the role — do NOT assume any role always has an output doc. If the session produces a separate output doc, the full delta lives there. If the session does not produce a separate output doc, the full delta lives in the handover block. Rationale: otherwise a session whose close-out is the handover (the surface most likely to carry a durable lesson) could drop the delta.

**D7 — Reconcile authorization for write gates (refines SAW-55 item 1/2 + resolves the warehouse-usage matrix tension).** The existing matrix marks `reconcile`/`check`/`reconcile-antechamber` as `owner / maintenance | owner-run`. For the write-gate pre/post-cleaning path, **non-fresh `reconcile` + `reconcile-antechamber` is a sanctioned agent-executed maintenance step** when `check` reports index/projection divergence — no owner HITL needed to restore a clean projection. The matrix wording must be reconciled so it no longer reads blanket owner-only for this path. `--fresh` remains explicit owner-authorization only and is NOT covered by this sanction.
