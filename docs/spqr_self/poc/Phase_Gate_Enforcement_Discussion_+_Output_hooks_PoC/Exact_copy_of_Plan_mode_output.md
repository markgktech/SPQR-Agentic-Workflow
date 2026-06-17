---

---
***SPQR Phase Gate Enforcement — Skill Fix + Hook***

**Context**

DOC-015 dokumentált egy szisztematikus hibát: Censura SPIKE-007 sessionban egyetlen turn alatt futott végig VERIFY → DISCOVER → CONVERGENCE → OUTPUT — az agent átracionalizálta a stop feltételt mert a

skill file definiálta a triggert, de NEM definiálta a stop-branch outputot.

Két probléma van egymás mellett:

1. **Skill** **file** **gap** — censura-discussion.md CONVERGENCE-ben és quaestor-relatio.md STOP-ban hiányzik a "mit csinálsz ha megállsz" formátum

2. **Mechanikus** **enforcement** **hiánya** — az agent a skill file utasítás ellenére is tud output phase-be lépni egyetlen turn alatt, az owner közbeavatkozása nélkül

**A** **hook** **célja:** az output phase-be lépés (= az output skill file olvasása) owner jóváhagyáshoz kötve. Ha az agent megpróbálja olvasni bármely output skill file-t, a hook blokkolja amíg az owner feloldja.

---

**Hogyan** **működik**

**Két** **gate,** **egy** **mechanizmus,** **két** **token.**

Input phase (auto) → STOP → owner: ! spqr-gate-discussion.sh → Discussion (valós párbeszéd) → STOP → owner: ! spqr-gate-output.sh → Output

**Miért** **az** **Input→Discussion** **gate** **az** **elsődleges:**

Ha az agent bemegy a discussionbe owner jóváhagyás nélkül, 20-30k tokent éget autonóm következtetésekkel — utólag nézel kárra, nem tudod megelőzni. Ha megáll az input után, a discussiont te indítod és

irányítod tempóban és irányban.

**A** **mechanizmus:**

A skill file-okban gate: marker él a frontmatterben. A PreToolUse hook a Read tool meghívása ELŐTT fut — maga olvassa a fájl első sorait (head), és ha markert talál → blokkolja az olvasást, amíg nincs

owner-token.

**Miért** **content** **marker** **és** **nem** **fájlnév:**

Ha a hook *-discussion.md fájlnév alapján szűr, fájlátnevezéskor elromlik. A gate: marker a fájlban marad átnevezésen át — a hook és a gate-definíció együtt mozog a skill fájlokkal.

**Token** **mechanizmus:**

- Discussion gate: owner futtatja ! spqr-gate-discussion.sh → /tmp/spqr_gate_discussion.token (single-use, törlődik olvasás után)

- Output gate: owner futtatja ! spqr-gate-output.sh → /tmp/spqr_gate_output.token (single-use)

- Stop hook: session végén törli mindkét tokent ha maradt

**Session** **starter** **érintetlen** **marad.** A hook a .claude/settings.json-ban él a repóban, automatikusan érvényes minden sessionban.

---

**Réteg** **1:** **Skill** **File** **Változások**

**1a.** **Discussion** **skill** **file-ok** **—** **gate:** **discussion marker** **(elsődleges** **gate)**

Érintett fájlok:

- docs/skills/censura-discussion.md

- docs/skills/consilium-discussion.md

- docs/skills/praetor-discussion.md

- docs/skills/tribunus-output.md ← Tribunusnál nincs külön discussion.md; az output.md-ben van a HITL — itt gate: discussion kerül, nem gate: output

- docs/skills/probator-output.md ← ugyanígy

Frontmatter kiegészítés:

---

name: [meglévő]

description: [meglévő]

gate: discussion

---

**1b.** **Input** **skill** **file-ok** **—** **záró** **stop** **instrukció**

Minden input.md fájl végére kerül (NEVER szekció elé vagy után, ahol logikus):

STOP AFTER INPUT

After all LOAD ORDER items are complete: stop here. Do not open [agent]-discussion.md.

Output: "Input complete — [N items loaded: ticket, Consilium comment, spike doc, etc.]. Ready to begin discussion when you are."

Wait for owner signal before continuing.

Érintett fájlok: censura-input.md, consilium-input.md, praetor-input.md, tribunus-input.md, probator-input.md, curator-input.md, quaestor-relatio.md

**1c.** **Output** **skill** **file-ok** **—** **gate:** **output marker** **(másodlagos** **gate)**

Érintett fájlok:

- docs/skills/censura-output.md

- docs/skills/censura-ticketing-output.md

- docs/skills/consilium-output.md

- docs/skills/praetor-output.md

- docs/skills/curator-output.md

- docs/skills/quaestor-relatio-output.md

Frontmatter kiegészítés:

---

name: [meglévő]

description: [meglévő]

gate: output

---

**1b.** **docs/skills/censura-discussion.md —** **CONVERGENCE** **stop-branch** **(DOC-015** **Item** **1)**

A CONVERGENCE szekcióban, közvetlenül a trigger feltétel után, co-lokálva:

CONVERGENCE

Personas compare findings and resolve disagreements.

Owner check-in required if: personas disagree on a FAIL, or significant emergent gap found.

STOP BRANCH — if either condition is met:

Do not write CONVERGENCE summary. Do not open censura-output.md.

List each gap or disagreement: [RISK|NOTE] [area] — [one sentence]

Output exactly: "Owner check-in required — [gap list]. Waiting for explicit closure before proceeding to output."

Wait for owner to explicitly close before continuing.

Censura closes autonomously after verdict if no owner check-in is needed.

**1c.** **docs/skills/quaestor-relatio.md —** **STOP** **feltétel** **várakozási** **output**

STOP — do not proceed to quaestor-relatio-output.md until owner explicitly closes discussion.

Output when stopping: "Research complete. Open items: [list]. Waiting for owner to explicitly close discussion."

If no open items: "Research complete — no unresolved items. Waiting for owner closure to proceed to spike document."

---

**Réteg** **2:** **Hook**

**Új** **fájlok**

**.claude/hooks/spqr-gate.sh** — PreToolUse hook (egy script, mindkét gate)

#!/bin/bash

FILE_PATH=$(python3 -c "

import sys, json

d = json.load(sys.stdin)

print(d.get('tool_input', {}).get('file_path', ''))

" 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

HEADER=$(head -10 "$FILE_PATH" 2>/dev/null)

if echo "$HEADER" | grep -q "^gate: discussion"; then

TOKEN="/tmp/spqr_gate_discussion.token"

if [ ! -f "$TOKEN" ]; then

echo "⛔ SPQR GATE [DISCUSSION]: Input phase lezárult. Discussion phase zárva."

echo "   Owner futtatja amikor kész: ! spqr-gate-discussion.sh"

exit 1

fi

rm -f "$TOKEN"

fi

if echo "$HEADER" | grep -q "^gate: output"; then

TOKEN="/tmp/spqr_gate_output.token"

if [ ! -f "$TOKEN" ]; then

echo "⛔ SPQR GATE [OUTPUT]: Discussion phase lezárult. Output phase zárva."

echo "   Owner futtatja amikor kész: ! spqr-gate-output.sh"

exit 1

fi

rm -f "$TOKEN"

fi

**.claude/hooks/spqr-gate-discussion.sh** — Owner futtatja discussion indításához

#!/bin/bash

touch /tmp/spqr_gate_discussion.token

echo "✅ SPQR GATE: Discussion phase feloldva."

**.claude/hooks/spqr-gate-output.sh** — Owner futtatja output indításához

#!/bin/bash

touch /tmp/spqr_gate_output.token

echo "✅ SPQR GATE: Output phase feloldva."

**.claude/settings.json**

{

"hooks": {

"PreToolUse": [

{

"matcher": "Read",

"hooks": [

{

"type": "command",

"command": "bash /Users/kovacsmark/Documents/GitHub/Marks-agentic-workflow-SPQR/.claude/hooks/spqr-gate.sh"

}

]

}

],

"Stop": [

{

"hooks": [

{

"type": "command",

"command": "rm -f /tmp/spqr_gate_discussion.token /tmp/spqr_gate_output.token"

{

"hooks": [

{

"type": "command",

"command": "rm -f /tmp/spqr_gate_discussion.token /tmp/spqr_gate_output.token"

}

]

}

]

}

}

**Megjegyzés** **a** **Foodoire** **repóhoz:** Ugyanez a .claude/settings.json kell a Foodoire projektbe is — a script path abszolút, mindkét helyen ugyanazt hívja.

---

**Amit** **NEM** **változtatunk**

- praetor-discussion.md — approval gate konkrét szólistával + "silence ≠ approval"

- tribunus-output.md / probator-output.md — 3-opciós HITL menü explicit, erős

- Session starter fájlok — nem érintett

- Agent.md fájlok — nem érintett

---

**Amit** **NEM** **változtatunk**

- Discussion fázison belüli lépések — nincs hook, owner steeri konverzációval

- Session starter fájlok — érintetlen

- Agent.md fájlok — érintetlen

- collegium-veto.md, ticket-comment.md — érintetlen

**Végrehajtási** **sorrend**

1. Discussion skill fájlok frontmatterébe gate: discussion (5 fájl)

2. Output skill fájlok frontmatterébe gate: output (6 fájl)

3. Input skill fájlok végére STOP AFTER INPUT instrukció (7 fájl)

4. censura-discussion.md — CONVERGENCE stop-branch (DOC-015)

5. quaestor-relatio.md — STOP várakozási output

6. .claude/hooks/ könyvtár + spqr-gate.sh + spqr-gate-discussion.sh + spqr-gate-output.sh

7. .claude/settings.json létrehozása

8. Foodoire .claude/settings.json — ugyanaz a hook bejegyzés

**Ellenőrzés**

- Manuális teszt discussion gate: echo '{"tool_input":{"file_path":"...censura-discussion.md"}}' | bash spqr-gate.sh → blokk

- ! spqr-gate-discussion.sh után ugyanez → olvasás engedélyezett, token törlődik

- Manuális teszt output gate: ugyanez censura-output.md-vel

- Frontmatter ellenőrzés: head -10 censura-discussion.md | grep "gate: discussion" → megtalálja

- Átnevezési robusztusság: marker bent marad fájlátnevezésnél → hook stabil