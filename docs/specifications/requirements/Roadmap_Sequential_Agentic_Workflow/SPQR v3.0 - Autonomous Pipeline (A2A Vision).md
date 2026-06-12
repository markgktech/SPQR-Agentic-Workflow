---

---
## Metadata

| Mező | Érték |
| --- | --- |
| Létrehozva | 2026-05-28 |
| Létrehozta | Mark + Claude kerekasztal (Gyuri, Laci) |
| Verzió | v1.0 — Vision |
| Státusz | Stratégiai vízió — v2.0 lezárása után részletezendő |

---

## Executive Summary

v3.0 az SPQR state of the art célállapota. Az A2A orchestration megérkezik: egy master agent Mark mellett koordinálja a teljes pipeline-t. Mark az L4 szinten dolgozik — csak kivételek esetén avatkozik be. A pipeline önjavít observability adatok alapján, a specifikációk gépileg verifikálhatók, és a cross-ticket intelligence mintázatokat ismer fel és előre jelez.

**Prerequisite:** v2.0 teljes lezárása — DAG orchestration, observability layer, spec-to-code validation mind stabil kell legyen mielőtt v3.0 tervezés elkezdődik.

---

## Az 5 fejlődési irány — v3.0-ban teljesül

| Fejlődési irány | v3.0-ban |
| --- | --- |
| Autonomy | Master agent koordinál; Mark L4 szint (csak kivételek); párhuzamos agent futás |
| Observability | Self-optimizing pipeline; adatok alapján önjavít; 6.3 relevance filtering aktív |
| Specification Formalism | Teljesen verifikálható AC-k; Agent CI/CD pipeline; pass/fail automatikusan |
| Cross-ticket Intelligence | Mintázat-felismerés; előrejelzés; projekt brain; "ilyen ticket 40%-ban vétóba fut" |
| Resilience | Teljes failure recovery; circuit breaker; self-healing orchestration |

---

## As-Is → To-Be

| Dimenzió | As-Is (v2.0 végén) | To-Be (v3.0 végén) |
| --- | --- | --- |
| Orchestráció | Kondicionális automatizmus; Mark aktívan figyeli | Master agent koordinál; Mark L4 — csak kivételek esetén avatkozik be |
| Mérhetőség | Trendek láthatók; manuális értékelés | Pipeline önjavít observability adatok alapján; self-optimizing |
| Specifikáció | Részben gépileg ellenőrzött | Teljesen verifikálható; AC — tool-checked pass/fail |
| Memória | Hierarchikus réteg; mintázat-alap | Cross-ticket intelligence; mintázat-felismerés; projekt brain; előrejelzés |
| Resilience | Checkpoint-resume | Teljes failure recovery; circuit breaker; self-healing |

---

## Items — v3.0

| # | Item | K | Fejlődési irány | Leírás |
| --- | --- | --- | --- | --- |
| — | A2A Orchestration (master agent) | 5 | Autonomy | Master agent koordinál Mark mellett; 1.1 + 4.1 + 4.3 + observability layer mind prerequisite; L4 szint |
| 1.3 | Async párhuzamos futás | 5 | Autonomy | Tribunus + Probator párhuzamosan futhat; orchestrator layer prerequisite; ma sequential marad |
| 2.5 | Project brain | 5 | Cross-ticket Intelligence | Persistent knowledge graph; projekt-szintű memória; 2.1 hierarchikus memória prerequisite |
| 2.6 | AST dependency graph | 3 | Cross-ticket Intelligence | Csak ha a projekt modulárissá válik; xcgrapher/XcodeTargetGraphGen; ma single-target Foodoire — premature |
| 4.5 | Agent CI/CD pipeline | 5 | Specification Formalism | 1.1 + 4.1 + 4.3 konvergenciája; Probator + hook alapú; teljesen automatizált quality gate |
| 5.7 | Model routing (sub-agent) | 2 | Autonomy | Horizontális routing ha sub-agent hierarchia létezik; vertikális: Sonnet  Opus tapasztalat alapján |
| 6.3 | Automatic relevance filtering | 3 | Observability | Orchestrator szeme — dinamikus kontextus döntés per agent-hívás; 1.1 DAG + observability prerequisite |
| — | Cross-ticket intelligence (full) | 4 | Cross-ticket Intelligence | Mintázat-felismerés; előrejelzés; observability data prerequisite (minimum 20-30 ticket) |
| 7.1 | Self-optimizing workflows | 5 | Observability | Pipeline meta-learning; adat nélkül vak; cross-ticket intelligence + A2A orchestration prerequisite; v4.0 határán |

---

## Prerequisite térkép

v3.0 nem indulhat v2.0 nélkül. Kritikus függőségek:

- **A2A master agent:** 1.1 DAG + 4.3 spec + 4.5 CI/CD + observability layer mind stabil
- **Cross-ticket intelligence (full):** 2.1 hierarchikus memória + observability data (legalább 20-30 ticket)
- **Self-optimizing:** cross-ticket intelligence + A2A orchestration
- **4.5 Agent CI/CD:** 4.1 + 4.3 + 3.6 iOS Simulator MCP mind kész
- **6.3 Relevance filtering:** 1.1 DAG + observability layer aktív