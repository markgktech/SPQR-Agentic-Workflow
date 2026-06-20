---
kind: decision
status: active
title: Adopt append-only proposal content
scope: write-gate
origin: decided
ticket: SAW-30
agent: Praetor
edges:
  - type: derived-from
    target: demo-n1
---

Proposal content files are append-only; a revision is a new file. The mutable
lifecycle lives only in the sidecar, so the antechamber stays a clean queue.
