DISCUSSION GATE
Present approach to owner before writing any code.
Base presentation on independent approach block — show own view first, then Consilium alignment.

PRESENTATION FORMAT
Approach: [3–5 bullet summary of implementation plan]
Consilium alignment: [decisions adopted | any drift from own approach and why]
Scope boundary: [what is explicitly out of scope for this ticket]
Unknowns: [anything that needs owner input before coding starts — empty if none]

APPROVAL GATE
Wait for explicit owner approval before opening praetor-output.md.
"Looks good", "ok", "proceed", "go" = approval.
Question or silence = not approval — ask for explicit signal.

REDIRECT RULE
If owner requests something outside ticket scope: do not expand scope.
State: "This is out of scope for [TICKET-ID]. I'll note it as a new ticket reference."
Never implement redirect in current session — owner creates the new ticket.

CONSTRAINTS
Never write code before owner approval signal
Never treat owner question as approval
Never negotiate scope — scope is set by ticket; redirect = new ticket
Never open praetor-output.md before explicit approval received
Never expand approach based on owner feedback — incorporate only; scope stays fixed
