---
kind: lesson
status: active
title: Burn the id before writing markdown
verdict: GREEN
origin: observed
ticket: SAW-30
agent: Probator
edges:
  - type: about
    target: demo-n1
---

Allocating the id in its own committed transaction makes a crash skip an id
rather than reuse one — unique, not gapless (S7).
