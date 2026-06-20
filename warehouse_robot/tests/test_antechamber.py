"""B4 — antechamber dir (truth) vs SQLite mirror: reconcile + divergence.

The mirror is excluded from the A8 logical digest and is not derivable from
warehouse markdown (proposals live outside the warehouse, G6/A3). Without a
dir-driven reconcile a corrupt or lost mirror would be invisible (L4/R3);
these tests prove the dir is the recoverable truth.
"""

import json
import tempfile
import unittest
from pathlib import Path

from warehouse_robot import fold, schema, write_gate as wg

from ._write_helpers import build_instance, make_proposal, mirror_rows

TS = "2026-06-20T10:00:00Z"


def _decision(**kw):
    base = dict(kind="decision", scope="ledger", ticket="SAW-30", agent="Praetor")
    base.update(kw)
    return make_proposal(**base)


def _seed(w, a):
    """Two proposals in different states: one pending, one ingested."""
    p1 = wg.propose(w, a, _decision(title="Pending one"), "SAW-30", "Praetor", now=TS)
    p2 = wg.propose(w, a, _decision(title="Ingested one"), "SAW-30", "Praetor", now=TS)
    wg.resolve(w, a, p2["proposal_key"], "ingested", now=TS)
    return p1["proposal_key"], p2["proposal_key"]


class Sidecars(unittest.TestCase):
    def test_content_is_append_only_state_lives_in_sidecar(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            key, _ = _seed(w, a)
            self.assertTrue((a / f"{key}.md").exists())
            sidecar = json.loads((a / f"{key}{wg.SIDECAR_SUFFIX}").read_text())
            self.assertEqual(sidecar["state"], "pending-senate")
            self.assertEqual(sidecar["round"], 1)


class Reconcile(unittest.TestCase):
    def test_reconcile_rederives_the_mirror_from_the_dir(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            _seed(w, a)
            before = {r["proposal_key"]: r["state"] for r in mirror_rows(w)}
            # wipe the mirror, then re-derive it from the dir
            conn = schema.connect(w / schema.INDEX_FILENAME)
            with conn:
                conn.execute("DELETE FROM antechamber")
            conn.close()
            self.assertEqual(mirror_rows(w), [])
            n = wg.reconcile_antechamber(w, a)
            self.assertEqual(n, 2)
            after = {r["proposal_key"]: r["state"] for r in mirror_rows(w)}
            self.assertEqual(before, after)
            self.assertTrue(wg.check_antechamber(w, a).clean)

    def test_mirror_survives_a_total_index_loss(self):
        # The index is disposable (S7). A full loss must rebuild BOTH the node
        # index (B2 reconcile) and the antechamber mirror (B4) from truth.
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            keys = _seed(w, a)
            (w / schema.INDEX_FILENAME).unlink()
            fold.rebuild(w, fresh=True)            # nodes back from markdown
            wg.reconcile_antechamber(w, a)         # mirror back from the antechamber dir
            states = {r["proposal_key"]: r["state"] for r in mirror_rows(w)}
            self.assertEqual(states[keys[0]], "pending-senate")
            self.assertEqual(states[keys[1]], "ingested")
            self.assertTrue(wg.check_antechamber(w, a).clean)


class Divergence(unittest.TestCase):
    def test_clean_when_in_sync(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            _seed(w, a)
            self.assertTrue(wg.check_antechamber(w, a).clean)

    def test_state_mismatch_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            key, _ = _seed(w, a)
            conn = schema.connect(w / schema.INDEX_FILENAME)
            with conn:
                conn.execute("UPDATE antechamber SET state='rejected' WHERE proposal_key=?", (key,))
            conn.close()
            report = wg.check_antechamber(w, a)
            self.assertFalse(report.clean)
            self.assertEqual(report.state_mismatch, [(key, "pending-senate", "rejected")])

    def test_missing_in_dir_and_mirror(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            key, _ = _seed(w, a)
            # delete the sidecar -> mirror row has no dir backing
            (a / f"{key}{wg.SIDECAR_SUFFIX}").unlink()
            report = wg.check_antechamber(w, a)
            self.assertIn(key, report.missing_in_dir)

    def test_hash_mismatch_when_content_tampered(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            key, _ = _seed(w, a)
            # tamper the mirror's stored hash (simulating drift)
            conn = schema.connect(w / schema.INDEX_FILENAME)
            with conn:
                conn.execute("UPDATE antechamber SET content_hash='deadbeef' WHERE proposal_key=?",
                             (key,))
            conn.close()
            self.assertIn(key, wg.check_antechamber(w, a).hash_mismatch)

    def test_index_missing_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            _seed(w, a)
            (w / schema.INDEX_FILENAME).unlink()
            self.assertTrue(wg.check_antechamber(w, a).index_missing)


if __name__ == "__main__":
    unittest.main()
