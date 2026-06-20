---
id: demo-n99
kind: decision
status: active
title: Proposer tried to mint an id
scope: write-gate
origin: decided
ticket: SAW-30
agent: Praetor
---

The proposer must not set id — the robot allocates it (A15). This is a
STRUCTURAL violation: not proposal-shaped, so it is raised at the door and
never persisted (CLI exit 2), not transitioned to rejected-malformed.
