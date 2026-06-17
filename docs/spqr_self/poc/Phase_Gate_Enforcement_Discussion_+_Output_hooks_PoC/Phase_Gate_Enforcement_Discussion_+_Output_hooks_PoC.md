---

---
|   |   |
| --- | --- |
| **Epic Name** | SPQR v1.2 Agentic Workflow |
| **Component Name** | Phase Gate Enforcement — Discussion + Output hooks |
| **Document status** | To Do |
| **Phase** | PoC |
| **Last updated** | 2026-06-01 |

# Overview

A SPQR pipeline agentjei Input → Discussion → Output fázisokon mennek végig, de ezek a fázishatárok jelenleg csak szövegesen vannak definiálva a skill fájlokban — az agent átugorhatja őket egyetlen turn alatt. Ez a PoC azt vizsgálja, hogy Claude Code PreToolUse hookkal és skill fájl content markerekkel mechanikusan kényszeríthetők-e ezek a határok minimális overhead mellett. Scope: Discussion gate + Output gate; discussion belső lépéseire nem terjed ki.

# Motivation

DOC-015 dokumentálta: Censura SPIKE-007 sessionban a VERIFY → DISCOVER → CONVERGENCE → OUTPUT ciklus egyetlen turn alatt futott le, owner check-in nélkül, ~20-30k token ráfordítással. Az agent a skill fájl stop feltételét átracionalizálta mert a stop-branch output formátum hiányzott. Ha az agent belép a discussion phase-be jóváhagyás nélkül, autonóm következtetésekre jut, és ezek a korai következtetések szennyezik a tényleges discussiont — az owner utólag látja a kárt, nem tudja megelőzni.

# Findings

- A PreToolUse hook a Read tool meghívása ELŐTT fut — maga olvashatja a fájl első sorait (`head`), és tartalom alapján dönthet blokkolásról. Ez fájlnévtől független.
- `gate: discussion` / `gate: output` marker a skill fájl frontmatterébe kerül — ha a fájl átíródik vagy átnevezik, a marker vándorol vele. A hook stabil marad.
- Két token fájl (`/tmp/spqr_gate_discussion.token`, `/tmp/spqr_gate_output.token`) — owner futtatja (`! spqr-gate-discussion.sh` / `! spqr-gate-output.sh`), single-use, Stop hook törli session végén.
- Egy hook script (`spqr-gate.sh`) kezeli mindkét gate-et — nem kell agent-specifikus logika.
- Session starter és [agent.md](http://agent.md/) fájlok érintetlenek — a gate a skill fájlban és a settings.json-ban él.
- Tribunusnál és Probatornál nincs külön [discussion.md](http://discussion.md/) — náluk az [output.md](http://output.md/) tartalmazza a HITL szekciót, így ott `gate: discussion` kerül az [output.md](http://output.md/)-be.

# Breakdown

## Hook mechanizmus

PreToolUse hook a Read toolra. A hook script `head -10`-zel olvassa a megnyitni kívánt fájl elejét, keres `gate: discussion` vagy `gate: output` markert. Ha talál és nincs token → blokk + üzenet az ownernek. Ha van token → token törlés + olvasás engedélyezett (single-use). Stop hook: mindkét token törlése session végén.

```javascript
Input phase (auto) → STOP → owner: ! spqr-gate-discussion.sh → Discussion (valós párbeszéd) → STOP → owner: ! spqr-gate-output.sh → Output
```

## Skill fájl változások

**Discussion gate — frontmatter marker (**`**gate: discussion**`**):**

- `censura-discussion.md`
- `consilium-discussion.md`
- `praetor-discussion.md`
- `tribunus-output.md` ← nincs külön [discussion.md](http://discussion.md/), HITL itt él
- `probator-output.md` ← ugyanígy

**Input fájlok — STOP AFTER INPUT instrukció a load order végére:**

- `censura-input.md`, `consilium-input.md`, `praetor-input.md`, `tribunus-input.md`, `probator-input.md`, `curator-input.md`, `quaestor-relatio.md`

Sablon: *"After all LOAD ORDER items are complete: stop here. Do not open [agent]-*[*discussion.md*](http://discussion.md/)*. Output: 'Input complete — [N items loaded]. Ready to begin discussion when you are.'"*

**Output gate — frontmatter marker (**`**gate: output**`**):**

- `censura-output.md`, `censura-ticketing-output.md`, `consilium-output.md`, `praetor-output.md`, `curator-output.md`, `quaestor-relatio-output.md`

**DOC-015 skill fix (ezzel együtt szállítandó):**

- `censura-discussion.md` CONVERGENCE szekció: stop-branch co-lokálva a trigger feltétel mellé
- `quaestor-relatio.md` STOP: várakozási output formátum hozzáadva

## settings.json

SPQR repóban és Foodoire repóban azonos `.claude/settings.json` — PreToolUse + Stop hook bejegyzés, abszolút script path a SPQR repóra mutatva.

# Recommendations

- **Do now:** Implementálja a két gate-et a SPQR repóban, validálja Censura sessionnal (DOC-015 reprodukálása → blokk ellenőrzése)
- **Do now:** DOC-015 skill fix (`censura-discussion.md` + `quaestor-relatio.md`) a hookkal együtt, nem külön
- **Defer:** Foodoire `.claude/settings.json` frissítése a SPQR validáció után
- **Discard:** Fájlnév alapú hook — fragile, content marker váltja ki

# Descoped

- Discussion fázison belüli lépések gatelése — owner konverzációval irányítja, nincs hook
- Input→Discussion gate belső lépéseinek kényszerítése (pl. load order sorrend ellenőrzése)
- Tribunus/Probator HITL mechanikus blokkolása — 3-opciós menü már explicit a skill fájlban
- Git commit/push blokkoló, protected file write blokkoló — külön concern, nem e PoC scope-ja

# References

- [DOC-015 — Censura CONVERGENCE stop-branch gap](https://www.notion.so/37168d5de1e881b4aba3db4c7629754a)
- [PoC TEMPLATE](https://www.notion.so/36868d5de1e8814386e1fbc33c8f9e39)

[[Exact copy of Plan mode output]]