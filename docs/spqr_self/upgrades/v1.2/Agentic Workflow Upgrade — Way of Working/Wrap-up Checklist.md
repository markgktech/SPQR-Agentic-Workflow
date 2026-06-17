---

---
## When wrap-up starts

Wrap-up begins after the owner confirms all execution groups are complete. The master runs through this checklist before closing the upgrade.

---

## Checklist

**Notion upgrade doc**

- [ ] All group sub-pages have Changes Made filled in
- [ ] Main page Implementation Groups section reflects all groups (done, stalled, descoped)
- [ ] Stalled and descoped items listed in a Stalled/Deferred section on the main page

**Open items**

- [ ] Every stalled item has a corresponding new DOC ticket created (owner assigns prefix + number)
- [ ] Every unresolvable item from Phase 3 has a corresponding new DOC ticket (if Phase 3 ran)
- [ ] No open item is left without a ticket or explicit descope decision

**Pending owner actions**

- [ ] Any [CLAUDE.md](http://claude.md/) text proposed by the master during the upgrade has been flagged for the owner — master does not apply these, owner does
- [ ] Owner is aware of any other proposed-but-not-applied actions from execution agents

**Memory**

- [ ] All decisions from this upgrade saved to memory with rationale
- [ ] Any memory files that changed (version, file map, strategy) are updated — not duplicated
- [ ] The primary upgrade memory file first line updated to: `STATUS: COMPLETE` (or PARTIAL if any groups did not finish)

**Repos**

- [ ] All repo file changes committed and pushed (owner’s task — master confirms this is pending, does not execute)
- [ ] SPQR sync grep check passed (if sync group ran)

**Owner confirmation**

- [ ] Owner explicitly confirms wrap-up complete before the master session closes

Confirmation is calibrated to communication style — a short “go” or “oké” is a valid gate signal. The master reads intent, not formality. Asking for formal written confirmation when the owner communicates concisely is friction, not rigour.

---

## After wrap-up

The master session closes. Any follow-on work (new DOC tickets) is handled in the next upgrade cycle — it is not appended to this session.