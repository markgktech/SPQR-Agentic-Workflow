"""L1 — the completed automated vertical slice (A17).

B5 is the last warehouse surface, so the full scenario now runs end to end:

    fold (B2) -> query (B3) -> propose -> gate -> ingest (B4) -> AUDIT (B5)
    -> reconcile (B2)

asserting every hop plus the two B5 contract points the brief names: the audit
LEG flags a deliberately broken case, AND a clean graph stays flag-free (no
false positives). The emitted flag — canonical f-plane markdown — must survive
a reconcile rebuild with the projection still deterministic (A8).

This is also the cross-B integration seam the master re-tests (A10): a gate-
allocated id (B4) is seen by the fold (B2), read by a query (B3), and a broken
case is flagged by the audit (B5), all on one disposable instance.
"""

import tempfile
import unittest

from warehouse_robot import audit, fold, query, schema, write_gate as wg

from ._write_helpers import build_instance, make_proposal

TS = "2026-06-20T12:00:00Z"


class VerticalSlice(unittest.TestCase):
    def test_full_slice_fold_query_propose_gate_ingest_audit_reconcile(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)  # fold (B2): the 14 demo nodes are indexed

            # --- B4: propose a decision that supersedes demo-n1, then ingest ---
            text = make_proposal(kind="decision", scope="local-first",
                                 title="Supersede the local-first decision",
                                 ticket="SAW-30", agent="Praetor",
                                 edges=[("supersedes", "demo-n1")])
            r = wg.propose(w, a, text, "SAW-30", "Praetor", now=TS)
            self.assertEqual(r["state"], "pending-senate")
            self.assertEqual(r["connection_report"]["edges"][0]["present"], True)
            res = wg.resolve(w, a, r["proposal_key"], "ingested", now=TS)
            new_id = res["node_id"]
            self.assertEqual(new_id, "demo-n13")

            # --- B2: the fold saw it; divergence is clean ---
            conn = schema.connect(w / schema.INDEX_FILENAME)
            try:
                row = conn.execute("SELECT title FROM nodes WHERE id=?", (new_id,)).fetchone()
                self.assertEqual(row[0], "Supersede the local-first decision")
            finally:
                conn.close()
            self.assertTrue(fold.check(w).clean)

            # --- B3: the query reads it, and demo-n1 is now derived-superseded ---
            fetched = query.fetch(w, "execute", "s-new", "slice", [new_id])
            self.assertEqual(fetched["nodes"][0]["id"], new_id)
            n1 = query.fetch(w, "execute", "s-n1", "slice", ["demo-n1"])
            self.assertEqual(n1["nodes"][0]["status"], "superseded")

            # --- B5: a clean graph stays flag-free. demo-n13 is connected, the
            # superseded demo-n1 drops out of the live graph, and the only
            # standing orphan (demo-n11) is already flagged → nothing new. ---
            clean = audit.audit(w, now=TS)
            self.assertEqual(clean["emitted"], [])
            self.assertEqual(clean["skipped_existing"],
                             [{"target": "demo-n11", "flag_type": "orphan"}])

            # --- B4 again: ingest a deliberately broken node (a decision with
            # no edges) through the real gate → an orphan enters the graph. ---
            orphan_text = make_proposal(kind="decision", scope="dead-end",
                                        title="An orphan ingested via the gate",
                                        ticket="SAW-30", agent="Praetor")
            ro = wg.resolve(w, a,
                            wg.propose(w, a, orphan_text, "SAW-30", "Praetor",
                                       now=TS)["proposal_key"],
                            "ingested", now=TS)
            orphan_id = ro["node_id"]
            self.assertEqual(orphan_id, "demo-n14")

            # --- B5: the audit LEG flags the broken case (and only it) ---
            flagged = audit.audit(w, now=TS)
            self.assertEqual(
                flagged["emitted"],
                [{"flag_id": "demo-f3", "target": orphan_id, "flag_type": "orphan"}],
            )
            self.assertEqual(flagged["open_flag_count"], 2)  # demo-f1 + demo-f3

            # idempotent: a re-run mints no duplicate
            self.assertEqual(audit.audit(w, now=TS)["emitted"], [])

            # --- B2: the emitted flag is canonical markdown — it survives a
            # reconcile rebuild, and the live index already equals a fresh one
            # (A8 part 2). Both the knowledge node and the audit flag are part
            # of the deterministic projection; both projections stay clean. ---
            live = fold.logical_digest_of(w / schema.INDEX_FILENAME)
            fold.rebuild(w)
            self.assertEqual(fold.logical_digest_of(w / schema.INDEX_FILENAME), live)
            self.assertTrue(fold.check(w).clean)
            wg.reconcile_antechamber(w, a)
            self.assertTrue(wg.check_antechamber(w, a).clean)
            # the flag is still open against its target after the rebuild
            self.assertEqual(audit.audit(w, now=TS)["open_flag_count"], 2)


if __name__ == "__main__":
    unittest.main()
