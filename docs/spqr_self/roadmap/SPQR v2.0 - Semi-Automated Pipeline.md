---

---
## Metadata

| Mező | Érték |
| --- | --- |
| Létrehozva | 2026-05-28 |
| Létrehozta | Mark + Claude kerekasztal (Gyuri, Laci) |
| Verzió | v1.0 — Big picture draft |
| Státusz | Stratégiai vázlat — részletes kerekasztal szükséges |

---

## Executive Summary

v2.0 az emberi orchestrátor fokozatos visszavonulásának első lépése. A pipeline mérhetővé válik, az első automatizált elágazások megjelennek, és az A2A orchestrátor infrastrukturális alapjai lerakódnak. Ez a milestone nem az autonómiáról szól — hanem az autonómia előkészítéséről.

Három fejlődési dimenzió indul el: **Observability** (pipeline health mérése), **Specification Formalism** (AC formalizálás kezdete), és **Resilience** (checkpointing). Két dimenzió előkészítése zajlik: **Autonomy** (DAG + kondicionális elágazás) és **Cross-ticket Intelligence** (hierarchikus memória alap).

---

## As-Is → To-Be

| Dimenzió | As-Is (v1.1 végén) | To-Be (v2.0 végén) |
| --- | --- | --- |
| Orchestráció | Mark manuálisan triggerel minden lépést | Kondicionális automatizmus; Mark kivételek esetén avatkozik be |
| Mérhetőség | Nulla telemetria — a pipeline egészsége csak véletlenszerűen derül ki | Verdict + vétó + futásidő logolva; trendek láthatók 10+ ticketen |
| Specifikáció | Prose AC-k; emberi review | AC-k részben gépileg ellenőrizhetők; Senate és Praetor közötti szerződés formalizálva |
| Memória | [LESSONS.md](http://lessons.md/)  • cross-ticket alap (v1.1) | Hierarchikus memória réteg; mintázat-alap lerakva |
| Resilience | Manuális recovery — félbehagyott execution = kézi javítás | Checkpoint-resume; félbehagyott pipeline folytatható |

---

## Items — v2.0

| # | Item | K | Fejlődési irány | Leírás |
| --- | --- | --- | --- | --- |
| 1.1 | DAG-alapú workflow | 4 | Autonomy | Sequential helyett graph-alapú végrehajtás; owner-dependent lépések [CLAUDE.md](http://claude.md/)-be dokumentálva; automation-triggered |
| 1.4 | Partial execution | 3 | Autonomy | Early feedback loop — csak ha pipeline automatizálódik; 1.1 DAG után releváns |
| 1.5 | Checkpointing / Resilience | 3 | Resilience | Pipeline resume capability; félbehagyott execution folytatható; 1.1 DAG prerequisite |
| 1.7 | Kondicionális pipeline elágazás | 2 | Autonomy | Vétó után automatikus Quaestor spike indítás; előbb manuálisan tapasztald meg a fájdalmat |
| 2.1 | Hierarchikus memória | 3 | Cross-ticket Intelligence | Short/mid/long term memória formalizálás; [LESSONS.md](http://lessons.md/) fölötti réteg; cross-ticket tapasztalati bázis |
| 3.5 | Adversarial agent | 3 | Specification Formalism | Probator second pass; bounded scope: top 3 törési pont per ticket; sycophancy ellen |
| 3.6 | iOS Simulator MCP | 3 | Tooling | Probator valódi végponttesztelést végez Simulator-on; v2.0 vége |
| 4.1 | Automated eval harness | 3 | Specification Formalism | tool-szint: 3.6b-be feloldódik; semantic szint: 4.3-ba feloldódik; ha mindkettő kész, 4.1 zárható |
| 4.3 | Spec-to-code validation | 4 | Specification Formalism | AC format stabilizálása prerequisite; gépileg verifikálható szerződés Senate és Praetor között |
| 5.4 | Multi-model routing | 3 | Autonomy | Minden agent Sonnet ma; routing csak ha sub-agent hierarchia megvan; v2.0-ban architektúra döntés |
| 6.1 | Context compression | 3 | Observability | 1.1 DAG kötelező companion item — együtt tervezendő; orchestrator layer számára szükséges |
| — | Observability layer | 2 | Observability | Verdict + vétó + futásidő + megközelítés-eltérés logolása per agent-futás; trend detektálás 10+ ticketen; pipeline health láthatóvá válik |

---

## Függőségi sorrend

A v2.0 items kritikus útja:

1. **Observability layer** — bármely más v2.0 item előtt; adatgyűjtés nélkül vak fejlesztés
2. **4.3 Spec-to-code** (AC format stabilizálása) → ezután **4.1 Automated eval harness** feloldódik
3. **3.6 iOS Simulator MCP** → ezután **4.1 tool-szint** feloldódik
4. **1.1 DAG** + **1.5 Checkpointing** + **6.1 Context compression** — kötelező companion hármas, együtt tervezendő
5. **1.7 Kondicionális elágazás** — 1.1 DAG után, manuális tapasztalat alapján

---

## Deferred to v3.0

- **6.3 Automatic relevance filtering** — orchestrator szeme; 1.1 DAG + observability prerequisite
- **2.5 Project brain** — 2.1 hierarchikus memória alap után
- **Cross-ticket intelligence (full)** — observability data kell hozzá (20-30 ticket minimum)
- **4.5 Agent CI/CD** — 4.1 + 4.3 + 3.6 iOS Simulator MCP mind stabil prerequisite

---

## Fejlesztési figyelmeztetések — Gap analízisből (ChatGPT + Gemini + web)

Ismert problémák amiket v2.0 tervezésekor elő kell venni. Nem megoldások — jelzések.

**G1 — Reasoning trace / decision provenance**

- Az observability layer (verdict + vétó + futásidő) megmondja *hogy* romlott a minőség, de nem *miért*
- Hiányzik: agent elmagyarázza a döntését, nem csak kimondja — "Tribunus vétózott mert X"
- Az observability layer definiálásakor kötelező elem, nem opcionális kiegészítés

**G2 — Failure taxonomy**

- A vétók ma kategorizálatlanok — a cross-ticket intelligence vakon tanul ha nincs struktúra
- Javasolt irány: Tribunus/Probator vétó outputba kötelező failure type mező (scope creep / arch violation / missing test / edge case)
- Nélküle a v3.0 cross-ticket intelligence nem tud mintázatot felismerni

**G3 — Confidence-aware handoff**

- Az agensek ma bináris outputot adnak: pass/fail
- Hiányzik: agent jelezze a bizonytalanságát — "átengedi de nem biztos" más mint "egyértelműen PASS"
- Mark tudná mikor kell beavatkozni és mikor nem — kevesebb felesleges review

**G4 — AC diffability**

- Az AC-k formátuma nincs definiálva úgy hogy diff-elhetők legyenek ticketek között
- Ha nem diff-elhető, nem lehet mérni hogy az AC minőség javul-e idővel
- Összefügg a W2 AC format döntéssel

**G5 — Execution economics tracking**

- Token költség per agent-futás nincs a tervezett observability layerben
- Egyetlen fejlesztőnek is fontos: melyik agent fogyaszt aránytalanul sokat a hozzáadott értékéhez képest
- Az observability layer definiálásakor opcionálisan hozzáadható

**W1 — Observability layer scope figyelmeztetés**

- A jelenlegi v2.0 tervben: verdict + vétó + futásidő — ez szükséges de nem elégséges
- G1 (reasoning trace) és G2 (failure taxonomy) nélkül az observability fél megoldás
- Tervezéskor ezeket egyszerre kell definiálni, nem utólag hozzáadni

---

## Glue Architecture — Mechanizmus döntések (2026-05-29)

Kerekasztal: Mark + Claude (Gyuri, Laci). Ez a szekció a v2.0 1.1 DAG tervezéséhez szükséges alapelveket rögzíti — mielőtt a DAG részletezése elkezdődik, ezeket kell inputként kezelni.

### Az architektúra

```javascript
Agents
   ↓
Typed handoffs          ← JSON payload, nem prose komment
   ↓
Append-only events      ← Notion komment már ez, csak formalizálni kell
   ↓
[State reducer]         ← KIHAGYVA — szekvenciális pipeline-hoz nem kell
   ↓
Canonical snapshot      ← egyszerű JSON / Notion DB property
   ↓
Notion visualization    ← Notion = view, nem source of truth
```

### Három architekturális alapelv

**1. Typed handoff JSON schema** — minden agent outputja strukturált JSON payload, nem prose-ba ágyazott mezők. A Notion komment tartalmaz egy gépolvasható JSON blokkot ÉS egy emberi összefoglalót. Az orchestrator a JSON blokkot olvassa, az owner a prose-t. Ez az 1.1 DAG prerequisite-je — explicit itemként kezelendő, nem implicit feltételezésként.

**2. Notion = visualization layer, nem source of truth** — a Notion komment az audit trail és a human interface, nem a pipeline tényleges state-je. A canonical snapshot egy külön, gépileg queryelhető record (Notion DB property vagy egyszerű JSON fájl). Ez az alapelv az egész v2.0 tervezési döntéseit érinti.

**3. State reducer kihagyása** — a tervezett stack (agents → typed handoffs → append-only events → state reducer → canonical snapshot → Notion) state reducert tartalmazott. Ez sequential pipeline-hoz overengineering: nincsenek párhuzamos agentek, nincs out-of-order event. Az orchestrator közvetlenül a typed handoff-ból írja a canonical snapshot-ot. Ha v3.0-ban párhuzamos futás jön (1.3 Tribunus + Probator), a reducer betolható visszafelé-kompatibilisan.

### Az orchestrator karaktere

Nem LangGraph — az Python-native, SPQR Claude Code session-ökben fut. Nem kell megépíteni amit a LangGraph ad. A valódi szükséglet egy **vékony routing script**:

6. Olvassa az utolsó Notion komment JSON blokkját
7. Parse-olja a `routing` mezőt
8. Összerakja a következő agent session starter-jét
9. Meghívja a következő Claude Code agentet
10. Visszaírja a canonical snapshot-ot

Ez ~50-100 sor — nem framework. LangGraph inspiráció forrás az architektúrához, de nem a runtime.

### Owner control — nem változik

Az automatizálás a közbülső mechanikára vonatkozik. A discussion fázisok (Consilium deliberáció, Praetor approach block) és a MANDATORY CHECKPOINTS ([CLAUDE.md](http://claude.md/) update, Curator Needs Work, Censura RED) owner-controlled maradnak. Az orchestrator ezeknél megáll és explicit "go"-t vár. A cél nem vibecoding platform — hanem augmentált workflow ahol az owner figyelmét a valódi döntési pontokra koncentrálja.

### Kapcsolódó items ebben a dokumentumban

- **1.1 DAG** — ez a szekció az 1.1 tervezési inputja; typed handoff schema külön prerequisite itemként kezelendő
- **6.1 Context compression** — a context filtering (agent csak a saját input schema-ját kapja, nem az összes kommentet) a typed handoff schema után következik
- **4.3 Spec-to-code validation** — a typed handoff javítja a mechanikus réteget; a szemantikus réteghez (expected_outputs pontossága) külön munka kell