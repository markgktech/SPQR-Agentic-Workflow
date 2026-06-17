---

---
## Affected Files

- `AGENT_LAWS.md` — new file (`.claude/rules/`)
- `senate.md` — new file (`docs/agents/`) ⚠️ **shared with Memory & Learning — write once, covers both groups** | also: ALLOWED TOOLS fix — Notion MCP write (see Fix S1 below)
- `praetor-input.md` — update (existing)
- `tribunus-input.md` — update (existing)
- `probator-input.md` — update (existing)
- `session-starters.md` — update (existing)
- `.claude/settings.json` — update (Context7 MCP server)
- `praetor-impl-doc.md` — update (new mandatory fields)

---

## Item 3.6b — Bash Tool Mandate

**What:** Every execution and review agent independently verifies the codebase using domain-specific tools. No agent trusts the previous agent’s reported results — each runs its own checks. Granular Bash permissions enforced technically via `--allowedTools`, not just prompt instruction.

**Distribution:**

- **Praetor:** `Bash(xcodebuild *)` + `Bash(swiftlint *)` + `Bash(xctest *)` — full suite after implementation
- **Tribunus:** `Bash(swiftlint *)` only — independent lint run; cannot modify files, cannot run git
- **Probator:** `Bash(xcodebuild *)` + `Bash(xctest *)` + `Bash(git diff *)` — independent test run + delta visibility; cannot modify files, cannot commit

**Enforcement:** `session-starters.md` documents the exact `--allowedTools` invocation per agent. Technical enforcement — not prompt-level.

**Impl doc mandatory fields** (pointer pattern — no code copied):

- `changed_files:` — list of file paths touched by Praetor
- `lint_violations:` — raw swiftlint output (compact: `file:line:error`)
- `test_results:` — PASS/FAIL summary + counts

Tribus reads `changed_files` and loads those files directly via Read tool. Reads `lint_violations` and forms independent judgment. Probator runs `git diff` to see the precise delta independently.

**Why independent, not domain-split trust:** Research (2026): agents sharing the same training distribution fail to catch each other’s errors downstream. Independent verification is the minimum adversarial diversity.

---

## Item 8.4 — Sensitive Operation Fallback

**What:** Narrow extension to Law 2 (Anti-Meeseeks). Explicit owner confirmation required before irreversible, high-blast-radius operations — even if the owner originally requested them.

**Triggers confirm:**

- Notion page delete or content overwrite
- File delete outside the git worktree

**Does NOT trigger confirm:**

- Routine file create/edit inside the worktree (Praetor’s normal work)
- Ticket comment writing
- Notion page creation
- Any additive operation

**Where:** `AGENT_LAWS.md` → Law 2 block, added as a narrow destructive-op rule

**Why narrow, not broad:** Full implementation (confirm every external state change) creates dozens of confirms per ticket and defeats pipeline automation. The value is in catching the rare but catastrophic case, not slowing routine work.

---

## Item 3.7 — Devil’s Advocate Role

**What:** Rotating Senate Opener step. At the start of each session, Tomi designates one of the 3 personas (Cicero / Caesar / Cato) as Devil’s Advocate (DA) based on the ticket topic. Owner is informed immediately at the start of the discussion — who the DA is and why. DA speaks first with the strongest counterargument. Senate then decides normally. No separate report.

**Flow:**

1. Senate Opener: Tomi names the DA + reason — visible to owner at session start
2. DA delivers the strongest counterargument first
3. Senate discusses and decides normally — DA argument is one input among others, not a veto
4. Consilium ticket comment captures the DA, the argument, and the final decision

**Where:** `senate.md` → Senate Opener section, mandatory step before discussion opens

**Implementation note:** DA designation logic — Tomi picks the persona whose domain is most at risk. Infrastructure-heavy ticket → Peti/Cato. Architecture decision → Zsombi/Caesar. Scope/process concern → Tomi/Cicero as DA.

---

## Item 3.6a — Context7 MCP Integration

**What:** Praetor identifies the relevant frameworks from the ticket before implementing, loads the current official documentation via Context7 MCP, and uses it to inform implementation decisions. Senate can use Context7 ad-hoc for technical decisions during Consilium.

**Where:**

- `.claude/settings.json` → Context7 MCP server added
- `praetor-input.md` → pre-implementation step: identify frameworks from ticket scope, load Context7 docs

**Implementation note:** If Context7 does not have documentation for a specific framework, Praetor continues without it — silent skip, no block.

---

## Fix S1 — [senate.md](http://senate.md/) Allowed Tools: Notion MCP Write

**What:** `senate.md` ALLOWED TOOLS currently lists only `Read` and `WebSearch`. Censura posts ticket comments and (via 2.7a) creates follow-up tickets in Notion. Without Notion MCP write explicitly declared, agents cannot confirm the permission is available — silent skip or halt risk.

**Where:** `senate.md` → ALLOWED TOOLS — add `Notion MCP (post ticket comment; create follow-up tickets on owner approval)`

**Linked to:** Item 2.7a (Traceability sub-page) — parent ticket creation by Censura requires Notion write to function.

**Why it wasn't caught earlier:** [senate.md](http://senate.md/) v1.0 never declared Notion MCP in ALLOWED TOOLS because comment posting was assumed, not specified. 2.7a makes the write path explicit and surfaces the gap.

**Risk if left out:** 2.7a is a dead implementation — Censura won't create parent-linked follow-up tickets without declared permission.