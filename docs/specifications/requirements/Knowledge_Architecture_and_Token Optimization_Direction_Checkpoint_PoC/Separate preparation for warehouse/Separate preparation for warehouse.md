---

---
MY OWN WAREHOUSE (graphRAG) - preparations

Milyen modellel fusson a warehouse?
Javaslat 1 (BM25 + Dense + RRF + graph lookup / similarity fallback):
Hibrid modell - Sparse + dense retrieval note: sparce a pontos kereséshez, dense a paraphasinghez amikor pontatlan a megfogalmazás
Sparce: BM25 - vektoros keresés / gráf keresés determinisztikusan
Use combo: hybrid query for anchoring (bm25 + semantic) then graph query (Recursive CTE)
A combo esetén a számokkal lehet jétszani mennyi eredmény az optimális outputnak (inkább kevesebb mint több)
Dense retrieval - embedding with agent - vector search with (normalized) cosine similarity
Adattárolás: A nodeok tartalmazzanak gráf alapú metadatat részt, lehetőleg kellően vastagot - a nodeok rendelkeznek majd vektorinfókkal is a szemantikus kereséshez
Javaslat 2 (graph lookup / similarity fallback) ONLY
Search nélkül, graphokat keressünk csak

Hogy határozzam meg a nodeokat és hogy fogjam keretek közé?
Legyen atomic
Legyen append only
Legyen supersede funkció
Ha lehet ne támaszkodjunk a latest onlyra mert a fejlesztéseknél ez nem abszolút igazság
Ne legyen minden egy döntésre húzva, a rendszerben több döntés is lehessen: A metaadatok jelezzék hogy milyen területre vonatkozik a döntés

Hogyan képezzem le a gáfok tárolását db-ben? Egy nagy vödör vagy több? (Knowledge Graph Architecture)
Javaslat 1 (Ontology)
Multi-Layered Ontology / Heterogén Gráf - layerek bevezetése
A mostani struktúra alapján egy nagy vödörbe megy mindne de LAYEReket lehetne hozzáadni (lesosns, conventions architecture)
Do laying on the right way: A node is an Atomic Assertion
Nincs különbőző fajta node, minden node ugyanaz a fajta objektum!!

Kell-e auditor a warehousehoz?
Lehet kell mert:
Contradictionök flaggelése és eldöntése
Rosszul ingestelt adatok
Önnellentmondó döntések - melyik a jó döntés? - nem fekete fehér
Nem analizált contradictionök
Auditor kell azért is hogy a kpaocolsatok hálóját karbantartsa? (graph szemszögből)
Vagy mindig csak az új nodeokat kapcosljuk régebbiekhez? - Javaslat: CSAK az új nodeok
Az auditor NEM tart karban, csak jelez ha gondot lát (árva nodeok figyelése és contradiction jelzése)
Jelzésre fontos - valami el van baszódva akkor lássa
Javaslat jelenleg: Hasnzis de flaggeljen de ne tudjon direktbe változtatni
Flag maintenance process kellni fog mert ha túl sok akkor okozhat gondot később
Ki? Mikor hogyan kezeli a flaeket? Lehetne akár retro téma.

Milyen workerek kellenek?
Ingestion workerek?
Query workerek?
Hogy legyen a karbantartásuk? Mérni kell melyik mennyire jó vagy roszz? Hogy méred?
Funciton call / natív tool use - itt csatlakozik az LLM a warehousera
Megvizsgálni kész libraryket: Ragas vagy TruLens
Context Relevance - Jó adatot hozott-e a robot?
Groundedness - A válasz a warehouseból származik vagy hallucináció van? /Mark: Gondolom amikor már flekapta az adatot)
Answer Relevance - megválaszolja a kérdést?

Hogy fogja az SPQR a gyakorlatban ezt használni?
Two phase commit javaslat
A kisebb agentek NEM ingestelnek: quaestor, praetor, tribunus, probator, curator
CSAK javaslatokat adhatnak (warehouse előszobájában a proposed: Run ID / Session ID hez kötve - a javslatok láthatók)
A drága agentek (senate) értékelnek és ingestelnek
Lekérdezik a proposed ötleteket a warehouse előszobájából
Megkapják a végső javaslatot az adott témához
A szekvencia során lévő kis agentek lássák a propose előszobában mi van
Amikor queryznek akkor megkapják MIT javasolt az előttük lévő agent
Mielőtt továbbadják és van hiba ők is hozzáadnak valamit vagy módosítást kérnek
A drága agentek lássák a javaslatokat de ne keveredjenek bele ha vetok voltak és változtak a dolgok
Akár deltát kapjanak a warehouse előszobájából - opcionális aggregationt adjon a robot

Hogy legyen a migráció?
Az eddigi projektudás összekaparása és egy nagy sessionben atomikusra kell bontani mindet de úgy hogy az élek meglegyenek
Mi lesz ha túl sok node jön ki? LLM limitbe nem fog ütközni?
HATALMAS sesison lehet - lehet részletekre szét kell bontani
Javaslat: Divide and Conquer
doksit szétvágása: max 2-3 oldalnyi szövegekre
Kis szövegek feldolgozása egyesével
pontos és szigú promt: mit akarunk outputnak
JSON (Structured Output) - ami majd a data ingestion alapja is lesz - itt már a normál ingestion folyamata fog élni

Hogy legyen a data ingestion migráció után?
Legyen egy előzetes lekérdezés mielőtt ingestelsz?
Honnan tudod, hogy mihez kapcoslódik?
Mi van ha egy meglévő nodenál egy újabb kapcoslat ban ami kimaradt? - kell ide audit?

Postgres vagy in-hous built db
KB 10k notera számítok első körben
In-house: Db building - run with something like docker
Half baked: Postgres pgvector ha kevesebb mint 10k nodes
Neo4j: Felesleges overcompliation + beépülő rendszer risk - nem ajánlott elsőnek

Hogy queryzen al LLM segítségével?
Ne kérjen le túl sok adatot
Legyen megszabva központilag egy lekérdezéssel mennyi node és milyen formában jöhet le
Ne naiv RAG legyen 1 lekérdezéssel
Legyen lekérdezési chain
De legyen keretek közé szorítva hogy ne égesse őrülten a tokenjeimet az LLM
Legyne lehtőség mélyre túrni és magasságokba is maradni - mindkettő másfajta adatlekérdezést igényel

[[Lookup guides]]