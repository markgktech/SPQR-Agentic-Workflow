---

---
## Metadata

| Mező | Érték |
| --- | --- |
| Létrehozva | 2026-05-27 |
| Létrehozta | Mark + Claude kerekasztal (Gyuri, Laci) |
| Verzió | v1.0 — Quick wins |
| Státusz | Draft — nagyobb témák következnek |

---

## Executive Summary

A SPQR v1.1 sequential agentic workflow fejlesztési roadmapjának első kerekasztal-feldolgozása. Az ülés célja: 57 aktív roadmap item priorizálása, az irreleváns vagy premature itemek kiszűrése, és a v1.1 quick win lista meghatározása — egyetlen fejlesztő + Claude Code + Notion MCP kontextusban.

A kerekasztal két szűrési szempontot alkalmazott: **technológiai relevancia** (Swift/iOS specifikus) és **skála** (single developer). Az eredmény: 11 item OOS, 3 item milestoneban tolva, 7 quick win döntés v1.1-re.

---

## As-Is — Jelenlegi állapot

- Stateless, szekvenciális multi-agent pipeline Claude Code + Notion MCP felett
- Két pipeline: **OPUS** (Senate → Praetor → Tribunus → Probator → Curator → Senate) és **EXPLORACIO** (Senate → Quaestor → Senate)
- State-átadás: Notion ticket comment-ek (külső igazság)
- Négy törvény: Stay in Character / Anti-Meeseeks / Don't be Dory / Be like Spock
- Fix szerepkörök: Senate (3 persona: Tomi/Cicero, Zsombi/Caesar, Peti/Cato), Praetor, Tribunus, Probator, Curator, Quaestor
- Egyetlen fejlesztő — nincs enterprise skála, nincs multi-dev

---

## To-Be — Nagy kép (placeholder)

*Ez a szekció a nagyobb témák ("Tervezd meg" csoport) kerekasztal-tárgyalása után kerül kitöltésre.*

Témák amik ide kerülnek majd: DAG orchestration, memory architektúra evolúciója, evaluation layer, agent architektúra fejlődése.

---

## Quick Wins — v1.1 döntések

| # | Item | Döntés | Implementáció |
| --- | --- | --- | --- |
| 2.7a | Parent Ticket relation | ✅ v1.1 | Notion Dev Tickets DB-be self-referential relation property + Consilium pre-flight: töltse be a szülő ticketet ha van |
| 2.3 | ADR javaslat (Decision memory) | ✅ v1.1 | Censura GREEN output kötelező szekciója — discussion fázisban NEM jelenik meg |
| 3.7 | DA (Devil's Advocate role) | ✅ v1.1 | Senate Opener process lépés — Tomi topic alapján jelöl ki DA-t a három persona közül per session; DA blokk először, autentikus nézet utána; nem 4. persona |
| 6.6 | [CLAUDE.md](http://claude.md/) frissítési javaslat | ✅ v1.1 | Curator-output kötelező szekciója — javasol exact szöveggel, owner dönt és ír; agent SOHA nem ír [CLAUDE.md](http://claude.md/)-be |
| 7.6 | Retrospektív session | ✅ v1.1 | Manual trigger — te vezeted és rakod össze; metodológia a tapasztalatból érlelődik |
| 9.2 | Standalone Debugging Tribunus | ✅ v1.1 | Új session starter — pipeline context nélkül, bármilyen kódra futtatható |
| 8.4 | Sensitive operation fallback | ✅ v1.1 | Anti-Meeseeks kiegészítés: bármilyen külső állapotot módosító művelet előtt explicit owner confirm — még ha az owner kérte is |
| 3.6a | Context7 MCP integráció | ✅ v1.1 | Context7 MCP szerver becsatolás Claude Code settings-be + Praetor prompt kiegészítés: azonosítsd a releváns framework-öket a ticketből, töltsd be a Context7 doksit mielőtt implementálsz. Senate ad-hoc használhatja technikai döntésnél. |
| 3.6b | Tribunus + Probator Bash tool mandátum | ✅ v1.1 | Praetor, Tribunus és Probator kötelezően futtat build+lint+test toolokat: xcodebuild, swiftlint, xctest — Bash permission + prompt mandátum minden érintett agent skill fájlban |
| [LESSONS.md](http://lessons.md/) | Curator per-ticket tanulságok | ✅ v1.1 | Curator minden pipeline futás végén 1-2 bullet tanulságot ír [LESSONS.md](http://lessons.md/)-be; Senate olvassa induláskor; 7.6 retrospektív agent alapja |

---

## Deferred Items

| # | Item | Új milestone | Ok |
| --- | --- | --- | --- |
| 1.7 | Kondicionális pipeline elágazás | v2.0 | Először manuálisan tapasztalj — automation csak ha fáj a mikromenedzsment |
| 5.7 | Model routing (Haiku/Sonnet/Opus) | v3.0 | Horizontális routing sub-agent architektúrát igényel (3.1/3.2); vertikális Sonnet > Opus a tapasztalat alapján |
| 2.7b | Agent ticket creation skill | TBD | Teszteletlen — hogyan működik a gyakorlatban? Tapasztalat kell |
| 7.6b | Retro metodológia formalizálás | TBD | Az első 5-10 ticket után lesz érdemi input rá |
| 5.4 | Multi-model routing | v2.0 | Minden agent egységesen Sonnet — differenciálás csak ha sub-agent hierarchia megvan; horizontális routing előfeltétele |
| 6.1 | Context compression pipeline | v2.0+ | 1.1 DAG kötelező companion item — együtt tervezendő; orchestrator agent prerequisite; orchestrator nélkül premature |
| 6.3 | Automatic relevance filtering | v3.0 | Az orchestrator szeme — dinamikus kontextus döntés agent-hívásokhoz; 1.1 DAG + observability prerequisite |

---

## Cross-Cutting Rules

A kerekasztal vitájából crystallizálódott szabályok amelyek minden agentre és minden jövőbeli döntésre érvényesek:

- **Agents SOHA nem írnak **[**CLAUDE.md**](http://claude.md/)**-be** — csak javasolnak exact szöveggel (ticket comment vagy Censura output). Az írás az owner kizárólagos joga.
- **Sensitive operations fallback** — bármilyen külső állapot módosítása (fájl, Notion, git) előtt explicit confirm szükséges, Anti-Meeseeks alá beépítve.
- **DA (Devil's Advocate role) = process lépés, nem persona** — Senate Opener szintjén rotál; a három existing persona közül kerül ki per session.
- **Agent ticket creation = HITL** — agent javasol részletekkel, owner jóváhagyja, agent hoz létre (Notion MCP). Soha nem autonóm.

---

## OOS — Out of Scope

### Technológiai OOS (Swift/iOS irreleváns)

| # | Item | Ok |
| --- | --- | --- |
| 4.7 | OpenAPI / Prisma / TypeScript spec-driven | Web/backend stack — nem Swift |
| 5.1 | Docker / ephemeral containers | iOS build = Xcode/macOS, nem container |
| 5.5 | Deterministic replay environments | Distributed systems koncepció |
| 5.6 | Playwright / headless browser | Web UI testing — iOS-en XCUITest |

### Skála OOS (single developer)

| # | Item | Ok |
| --- | --- | --- |
| 1.6 | Distributed agent orchestration | Multi-machine infrastruktúra — single dev nem igényli |
| 9.1 | Multi-human + multi-agent hybrid teams | Single developer |
| 9.3 | Parallel developer-agent streams | Single developer |
| 9.4 | Shared project memory graph | "Shared" = multi-dev |
| 9.5 | Asynchronous collaboration layers | Multi-developer |

### Premature OOS (revisit later)

| # | Item | Ok |
| --- | --- | --- |
| 6.4 | Context budgeting (token allocation) | Premature — revisit ha a projekt skálázódik |
| 8.2 | Audit trail immutability | Notion natívan kezeli; teljességi rést 2.3/2.7 zárja be |

---

## Fejlesztési figyelmeztetés — Gap analízisből (ChatGPT + Gemini + web)

Ez a szekció nem megoldásokat tartalmaz — csak jelzi hogy ezek ismert problémák amiket fejlesztésnél elő kell venni.

**W2 — AC format döntés (BLOCKER a v2.0 spec-to-code validationhöz)**

- A spec-to-code validation (4.3) nem tud elindulni amíg az AC formátum nincs definiálva
- Kérdés: XCTest-based, Gherkin-szerű, vagy Notion property-k?
- Ez v1.1 implementáció közben döntendő — ne halaszd v2.0-ra

**G6 / W3 — Architectural coherence (Senate szintű, hamarabb mint v3.0)**

- AI-generált kód lokálisan helyes, globálisan csendben ronthatja az architektúrát
- Az AST/dependency tool (xcgrapher) single-target projekten is futtatható ma
- Javasolt megoldás irány: Senate-be egy rövid architectural invariant lista minden ticketnél — ez nem igényel modularizációt