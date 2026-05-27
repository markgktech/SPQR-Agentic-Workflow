LOAD ORDER
1. AGENT_LAWS.md
2. CLAUDE.md
3. Ticket (full text + all Notion comments)
4. Spike doc Decision Table (if spike doc exists for this ticket)
5. [WRITE INDEPENDENT APPROACH BLOCK — before loading item 6]
6. Consilium output comment (if exists)
7. praetor-discussion.md

HALT RULE
If no Consilium comment AND no spike doc found on ticket:
Signal owner: "No Consilium output or spike doc found. Cannot proceed without mandate context."
Do not open praetor-discussion.md. Wait for owner response.
If owner overrides: note in approach_before_consilium — "No Consilium input available; proceeding on owner instruction."
Never silently skip the halt check.

INDEPENDENT APPROACH BLOCK
After loading items 1–4, before loading item 6:
Write 3–5 bullets stating your independent implementation approach.
This block is visible in the conversation — owner sees it.
Summary of this block goes into the ticket comment approach_before_consilium field.
Do not read Consilium output before this block is written.

RECONCILIATION
After loading item 6, compare own approach to Consilium decisions.
Surface any drift, gaps, or contradictions explicitly.
If Consilium mandates a different approach: adopt it unless it conflicts with CLAUDE.md invariants.
If conflict with CLAUDE.md: flag to owner before proceeding — do not silently override.

CONSTRAINTS
Never start discussion before all LOAD ORDER items are read
Never load Consilium output before independent approach block is written
Never skip halt check — not even on small or familiar tickets
Never carry state from a prior session — start cold (Law 3)
Never proceed if ticket scope is ambiguous — clarify with owner first
