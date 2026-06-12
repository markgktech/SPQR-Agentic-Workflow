---
id: demo-n9
kind: decision
status: active
title: Keep CLI output plain and parseable
scope: tooling
origin: decided
timestamp: 2026-06-02T11:30:00Z
ticket: DEMO-2
agent: Quaestor
schema_version: 1
edges:
  - type: relates-to
    target: demo-n8
---

Tool output stays line-oriented plain text so scripts can consume it. The
relates-to edge is the deliberately weak second-class link (S3): both
nodes touch user-facing surface conventions, nothing stronger.
