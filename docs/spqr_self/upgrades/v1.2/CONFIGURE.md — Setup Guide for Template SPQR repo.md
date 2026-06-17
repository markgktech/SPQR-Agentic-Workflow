---

---
## What

New file in the public SPQR repo: `docs/CONFIGURE.md`

Every placeholder in the generic repo needs to be explained — what it means, which files contain it, what to put in it. Without this, a new user stares at `[SPIKE_TEMPLATE_ID]` with no guidance.

Format: agent-consumable AND human-readable. An agent can load it during setup; a new user can read it top to bottom.

**Repo:** `/Users/kovacsmark/Documents/GitHub/Marks-agentic-workflow-SPQR/`

---

## Section 1 — Variable Catalogue

Every placeholder, one place:

| Placeholder | Files | What to put in |
| --- | --- | --- |
| [Name 1] / [Name 2] / [Name 3] | [senate.md](http://senate.md/), [consilium-discussion.md](http://consilium-discussion.md/), [censura-discussion.md](http://censura-discussion.md/), [session-starters.md](http://session-starters.md/) | First names of your 3 Senate personas |
| [Name 4] | [quaestor.md](http://quaestor.md/), [session-starters.md](http://session-starters.md/) | First name of your Quaestor persona |
| [PROJECT_PATH] | [session-starters.md](http://session-starters.md/) | Absolute path to your project root |
| [PROJECT_BOUNDARIES] | [ticket-slicing.md](http://ticket-slicing.md/) | Project-specific ticket slicing rules (layer/entity boundaries) — silent failure risk if left empty |
| [SPIKE_TEMPLATE_ID] | [censura-ticketing-input.md](http://censura-ticketing-input.md/) | Notion page ID of your Spike ticket template |
| [FEATURE_TEMPLATE_ID] | [censura-ticketing-input.md](http://censura-ticketing-input.md/) | Notion page ID of your Feature ticket template |
| [BUG_TEMPLATE_ID] | [censura-ticketing-input.md](http://censura-ticketing-input.md/) | Notion page ID of your Bug ticket template |
| [DOC_TEMPLATE_ID] | [censura-ticketing-input.md](http://censura-ticketing-input.md/) | Notion page ID of your Doc ticket template |
| [SPIKE_DOCUMENT_TEMPLATE_ID] | [censura-ticketing-input.md](http://censura-ticketing-input.md/), [spike-document.md](http://spike-document.md/) | Notion page ID of your Spike Document template |
| [SPIKE_DOC_PARENT_PAGE_ID] | [quaestor-relatio-output.md](http://quaestor-relatio-output.md/) | Notion page ID of the parent page where spike docs are created |

---

## Section 2 — Notion Setup

- How to get a page ID: open the page in Notion, copy the URL — the ID is the last 32-character hex string (with or without dashes)
- Ticket templates: create one template page per type (Spike, Feature, Bug, Doc) — structure is up to you; the agent fetches it live and uses the section structure as-is
- Spike doc parent: create a dedicated page (e.g. "Spiking") where all spike research documents will be created as sub-pages

---

## Section 3 — Non-Notion Alternatives

**Ticket tracker alternatives (Linear, GitHub Issues, Jira):**

Any system works if it supports linkable tickets and comment writing. Replace Notion template IDs with ticket URLs. MCP sections in skill files can be skipped or replaced with equivalent tool calls for your tracker.

**Spike doc alternatives (if no Notion):**

Law 3 (Don't be Dory) requires the agent to write to an external record — session memory is not sufficient. Alternatives:

- Markdown file committed to the repo (simplest)
- Google Doc
- Confluence page

The spike doc parent page ID placeholder must still be replaced — point it to wherever your spike docs will live. Do not leave it empty.

---

## Changes Made

- `docs/CONFIGURE.md` → NEW — Section 1: Variable Catalogue (12 placeholder, tábla, explicit fájllisták minden sorban); Section 2: Notion Setup (page ID kinyerés, template struktúra, parent page stabilitás); Section 3: Non-Notion Alternatives (ticket tracker + spike doc alternatívák, skill file Notion fetch logic cserélendő explicit módon jelezve)

**Roundtable-azonosított korrekciók (mind javítva a fájlban):**

- `[Name 2]`, `[Name 3]` sorokból `same as above` eltávolítva → explicit fájllista
- `README.md` hozzáadva `[Name 1–4]` fájllistákhoz
- `censura-ticketing-input.md` hozzáadva a `[SPIKE_DOC_PARENT_PAGE_ID]` fájllistájához (brief-ből hiányzott)
- Section 3 spike-doc alternatíva: mindkét érintett fájl (`quaestor-relatio-output.md` + `censura-ticketing-input.md`) listázva