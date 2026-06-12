---
id: demo-n8
kind: decision
status: active
title: Confirmation dialogs use the standard destructive style
scope: ux-pattern
origin: decided
timestamp: 2026-06-02T11:00:00Z
ticket: DEMO-2
agent: Praetor
schema_version: 1
edges:
  - type: derived-from
    target: demo-n3
---

Concrete project rule derived from the inherited confirmation constraint:
all destructive confirmations use the platform's destructive button role,
no custom dialogs.
