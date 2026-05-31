TRIGGER
Wrap-up begins after the owner confirms all execution groups are complete. Master runs this checklist before closing the upgrade session.

CHECKLIST

Notion upgrade doc
- [ ] Changes Made filled in on every group sub-page
- [ ] Main page Implementation Groups section reflects all groups (done, stalled, descoped)
- [ ] Stalled and descoped items listed in a Stalled/Deferred section on the main page

Open items
- [ ] Every stalled item has a corresponding new DOC ticket created (owner assigns prefix + number)
- [ ] Every unresolvable item from Phase 3 has a corresponding new DOC ticket (if Phase 3 ran)
- [ ] No open item left without a ticket or explicit descope decision

Memory
- [ ] All decisions from this upgrade saved to memory with rationale
- [ ] Memory files that changed (version, file map, strategy) updated — not duplicated
- [ ] Primary upgrade memory file first line updated to: STATUS: COMPLETE (or PARTIAL if any groups did not finish)

Pending owner actions
- [ ] Any proposed CLAUDE.md text flagged for the owner — master does not apply, owner does
- [ ] Owner is aware of any proposed-but-not-applied actions flagged in execution agent output summaries

Repos
- [ ] All repo file changes committed and pushed — owner's task; master confirms this is pending, does not execute
- [ ] SPQR sync grep check passed (if sync group ran)

Owner confirmation
- [ ] Owner explicitly confirms wrap-up complete before session closes
Confirmation is calibrated to communication style — a short "go" or "oké" is a valid gate signal. Master reads intent, not formality.

POST WRAP-UP
Session closes. Any follow-on work (new DOC tickets) is handled in the next upgrade cycle — not appended to this session.

NEVER
- Close session without owner confirmation
- Apply CLAUDE.md changes directly
- Run git commit or git push
- Create tickets with assigned prefixes or numbers
- Append follow-on work to the current upgrade session
