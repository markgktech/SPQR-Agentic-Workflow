# CONFIGURE.md — SPQR v1.2 Setup Guide

This file explains every placeholder in the SPQR skill and agent files, and how to replace them before running the workflow on a new project.

---

## Section 1 — Variable Catalogue

| Placeholder | File(s) | What to fill in |
|---|---|---|
| `[Name 1]` | `README.md`, `docs/agents/senate.md`, `docs/skills/consilium-discussion.md`, `docs/skills/censura-discussion.md`, `docs/agents/session-starters.md` | First name of your first Senate persona |
| `[Name 2]` | `README.md`, `docs/agents/senate.md`, `docs/skills/consilium-discussion.md`, `docs/skills/censura-discussion.md`, `docs/agents/session-starters.md` | First name of your second Senate persona |
| `[Name 3]` | `README.md`, `docs/agents/senate.md`, `docs/skills/consilium-discussion.md`, `docs/skills/censura-discussion.md`, `docs/agents/session-starters.md` | First name of your third Senate persona |
| `[Name 4]` | `README.md`, `docs/agents/quaestor.md`, `docs/agents/session-starters.md` | First name of your Quaestor persona |
| `[PROJECT_PATH]` | `docs/agents/session-starters.md` | Absolute path to your project root directory (e.g. `/Users/you/Projects/myapp`) |
| `[PROJECT_BOUNDARIES]` | `docs/skills/ticket-slicing.md` | Project-specific ticket slicing rules — layer and entity boundaries. **Silent failure risk if left empty** — the agent will not slice tickets correctly without this. |
| `[SPIKE_TEMPLATE_ID]` | `docs/skills/censura-ticketing-input.md` | Notion page ID of your Spike ticket template |
| `[FEATURE_TEMPLATE_ID]` | `docs/skills/censura-ticketing-input.md` | Notion page ID of your Feature ticket template |
| `[BUG_TEMPLATE_ID]` | `docs/skills/censura-ticketing-input.md` | Notion page ID of your Bug ticket template |
| `[DOC_TEMPLATE_ID]` | `docs/skills/censura-ticketing-input.md` | Notion page ID of your Doc ticket template |
| `[SPIKE_DOCUMENT_TEMPLATE_ID]` | `docs/skills/censura-ticketing-input.md`, `docs/skills/spike-document.md` | Notion page ID of your Spike Document template |
| `[SPIKE_DOC_PARENT_PAGE_ID]` | `docs/skills/quaestor-relatio-output.md`, `docs/skills/censura-ticketing-input.md` | Notion page ID of the parent page where spike docs are created as sub-pages |
| `[SPQR_REPO_PATH]` | `docs/upgrade/session-starter.md` | Absolute path to your SPQR template repo on disk (e.g. `/Users/you/Projects/Marks-agentic-workflow-SPQR`). Needed for sync group briefs during upgrades. |
| `[Master Persona 1]` | `docs/upgrade/session-starter.md`, `docs/upgrade/roundtable.md` | First name of your Dev Process Architect persona for workflow upgrade roundtable |
| `[Master Persona 2]` | `docs/upgrade/session-starter.md`, `docs/upgrade/roundtable.md` | First name of your Agentic Trends Expert persona for workflow upgrade roundtable |

**Senate personas** (`[Name 1]`–`[Name 3]`) appear together in each file. Each persona covers a fixed review angle: premise validity, delivery scope, and production risk. Choose names that are meaningful to your team — real names, fictional characters, or industry figures all work.

---

## Section 2 — Notion Setup

**Finding a page ID from a Notion URL**

The page ID is the last 32 hex characters in any Notion URL, with or without hyphens:

```
https://www.notion.so/My-Page-37168d5de1e881a1ac72c47d42a4e537
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                  this is the page ID
```

You can use the full string with hyphens (`37168d5d-e1e8-81a1-ac72-c47d42a4e537`) or without — Notion accepts both.

**Ticket templates**

Create one template page per ticket type: Spike, Feature, Bug, Doc. The structure is yours to define — the agent fetches the template live and replicates the existing section structure when creating new tickets. Minimal templates (title + a few section headers) are enough.

**Spike doc parent page**

Create a dedicated Notion page (e.g. "Spiking" or "Research") as the parent. Every spike research document the agent creates becomes a sub-page under it. Keep this page stable — changing the ID after setup requires updating `quaestor-relatio-output.md` and `censura-ticketing-input.md`.

---

## Section 3 — Non-Notion Alternatives

**Ticket tracker alternatives (Linear, GitHub Issues, Jira)**

Any system works as long as it supports linkable tickets and comment writing. When using a non-Notion tracker:

- Replace the four `*_TEMPLATE_ID` placeholder values in `censura-ticketing-input.md` with your ticket IDs or URLs — but also replace the Notion template-fetch calls in that file with the corresponding create/clone calls for your tracker. Changing the placeholder value alone is not sufficient; the skill file logic must change too.
- Replace all other Notion MCP tool calls in the relevant skill files with the appropriate API calls or CLI commands for your tracker.
- The Notion MCP sections in agent session-starters can be skipped or swapped for your tool's authentication step.

**Spike document alternatives (if not using Notion)**

Law 3 (Don't be Dory) requires the agent to write spike research to an external record — session memory is not sufficient. `[SPIKE_DOC_PARENT_PAGE_ID]` must always be filled with something; it cannot be left as a placeholder.

Alternatives in order of simplicity:

- **Markdown file committed to the repo** — simplest option. Set `[SPIKE_DOC_PARENT_PAGE_ID]` to the directory path (e.g. `docs/spikes/`) and update both `quaestor-relatio-output.md` and `censura-ticketing-input.md` to write a `.md` file instead of making a Notion page creation call.
- **Google Doc** — replace the Notion page creation call with a Google Drive API call; set the placeholder to the folder ID.
- **Confluence** — replace with a Confluence page creation call; set the placeholder to the parent page ID.

The placeholder value itself is always required. What varies is which tool call reads it.
