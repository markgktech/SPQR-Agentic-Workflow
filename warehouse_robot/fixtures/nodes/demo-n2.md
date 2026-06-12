---
id: demo-n2
kind: decision
status: active
title: Errors propagate as typed envelopes
scope: error-handling
origin: decided
timestamp: 2026-06-01T09:05:00Z
ticket: DEMO-1
agent: Senate
schema_version: 1
---

Services return a typed error envelope instead of throwing raw errors
across layer boundaries. This node is later superseded by demo-n7; the
supersede relation lives on the incoming edge, never as a stored status.
