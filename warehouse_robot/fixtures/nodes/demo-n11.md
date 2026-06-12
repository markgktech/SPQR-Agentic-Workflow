---
id: demo-n11
kind: decision
status: active
title: Cache entries expire after thirty days
scope: data-layer
origin: decided
timestamp: 2026-06-07T10:00:00Z
ticket: DEMO-6
agent: Senate
schema_version: 1
---

Local cache entries are evicted after thirty days without access. This
fixture node deliberately carries no edges: it is the orphan-watch test
subject for the B5 tripwires, flagged by demo-f1.
