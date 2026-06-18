TRIGGER
Wrap-up begins after the owner confirms all execution groups are complete. Master runs this checklist before closing the upgrade session.

CHECKLIST

Run container
- [ ] Changes Made filled (the "_(pending execution)_" sentinel replaced) in every group sub-md
- [ ] MAIN folder-note Implementation Groups section reflects all groups (done, stalled, descoped)
- [ ] Stalled and descoped items listed in a Stalled/Deferred section in the MAIN folder-note
- [ ] MAIN folder-note status set to done (or partial if any groups did not finish)

Open items
- [ ] Every stalled item has a corresponding new SAW ticket — the owner creates it; Notion auto-assigns the ID
- [ ] Every unresolvable item from Phase 3 has a corresponding new SAW ticket (if Phase 3 ran)
- [ ] No open item left without a ticket or explicit descope decision

Decisions
- [ ] All decisions from this upgrade recorded in the run's PoC (poc/ lane) with rationale; the run container's MAIN links the PoC (poc: frontmatter)
- [ ] Cross-run, durable decisions tagged (e.g. #decision) so they stay findable in the vault — not duplicated

Traceability
- [ ] Each processed SAW ticket has a comment linking the run container (MAIN folder-note path)

Pending owner actions
- [ ] Any proposed CLAUDE.md text flagged for the owner — master does not apply, owner does
- [ ] Owner is aware of any proposed-but-not-applied actions flagged in execution agent output summaries

Repos
- [ ] All repo file changes (run container + workflow files) committed and pushed — owner's task; master confirms this is pending, does not execute
- [ ] SPQR sync grep check passed (if sync group ran)

Owner confirmation
- [ ] Owner explicitly confirms wrap-up complete before session closes
Confirmation is calibrated to communication style — a short "go" or "oké" is a valid gate signal. Master reads intent, not formality.

POST WRAP-UP
Session closes. Any follow-on work (new SAW tickets) is handled in the next upgrade cycle — not appended to this session.

NEVER
- Close session without owner confirmation
- Apply CLAUDE.md changes directly
- Run git commit or git push — the owner commits and pushes
- Create tickets or assign ticket numbers — the owner creates the SAW ticket; Notion auto-assigns the ID
- Append follow-on work to the current upgrade session
