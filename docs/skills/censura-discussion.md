---
name: censura-discussion
description: Senate Censura deliberation — two-pass review structure, finding format, and persona constraints
---

TWO-PASS STRUCTURE

VERIFY PASS (parallel, autonomous)
Each persona independently checks executor output against Consilium decisions.
Finding format: [PASS|FAIL|RISK|NOTE] [area] [HIGH|MED|LOW Impact] [HIGH|MED|LOW Effort] — [one sentence]
PASS: requirement met
FAIL: requirement not met — triggers RED verdict
RISK: met but fragile or operationally concerning
NOTE: observation worth recording; not blocking

DISCOVER PASS (open-ended)
Each persona looks for emergent gaps not visible at Consilium time.
Emergent findings become candidate new SPIKE sub-tickets or DEV tickets — owner decides in output phase.

CONVERGENCE
Personas compare findings and resolve disagreements.
Owner check-in required if: personas disagree on a FAIL, or significant emergent gap found.
Censura closes autonomously after verdict if no owner check-in is needed.

MANDATORY PER PERSONA
[Name 1]: did executor solve the right problem? (premise check)
[Name 2]: did executor stay in scope and deliver what was planned? (delivery check)
[Name 3]: does executor output break anything in production? (operational impact check)

NEVER
Never issue silent clean pass — at least one finding or explicit "no findings" (Law 4)
Never suppress a FAIL to preserve pace
Never approve work that violates a Critical Rule from CLAUDE.md
Never carry Consilium session memory into review — load from Notion comment (Law 3)
Never let delivery pressure override a correctness FAIL
