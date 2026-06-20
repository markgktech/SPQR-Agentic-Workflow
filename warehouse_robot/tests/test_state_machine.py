"""B4 — the proposal state machine + the ID-allocation monopoly."""

import tempfile
import unittest
from pathlib import Path

from warehouse_robot import schema, store, write_gate as wg
from warehouse_robot.errors import AntechamberError, RevisionLimitReached

from ._write_helpers import build_instance, make_proposal, mirror_state

TS = "2026-06-20T10:00:00Z"


def _decision(**kw):
    base = dict(kind="decision", scope="ledger", ticket="SAW-30", agent="Praetor",
                edges=[("derived-from", "demo-n1")])
    base.update(kw)
    return make_proposal(**base)


class HappyPath(unittest.TestCase):
    def test_propose_then_ingest(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            r = wg.propose(w, a, _decision(), "SAW-30", "Praetor", now=TS)
            self.assertEqual(r["state"], "pending-senate")
            self.assertEqual(r["connection_report"]["missing_targets"], [])
            self.assertIn("escalation_packet", r)
            key = r["proposal_key"]
            self.assertEqual(mirror_state(w, key), "pending-senate")

            res = wg.resolve(w, a, key, "ingested", now=TS)
            self.assertEqual(res["state"], "ingested")
            self.assertEqual(res["node_id"], "demo-n13")
            self.assertEqual(mirror_state(w, key), "ingested")
            # the node markdown was appended + folded
            self.assertTrue((w / "nodes" / "demo-n13.md").exists())
            node = store.read_node_file(w / "nodes" / "demo-n13.md")
            self.assertEqual(node.timestamp, TS)
            self.assertEqual(node.schema_version, 1)

    def test_reject(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            r = wg.propose(w, a, _decision(), "SAW-30", "Praetor", now=TS)
            res = wg.resolve(w, a, r["proposal_key"], "rejected", now=TS)
            self.assertEqual(res["state"], "rejected")
            self.assertEqual(mirror_state(w, r["proposal_key"]), "rejected")
            # nothing was minted
            self.assertFalse((w / "nodes" / "demo-n13.md").exists())

    def test_validated_is_a_reachable_state(self):
        # The escalation predicate runs while the proposal rests at 'validated',
        # so the state is exercised — not a dead DDL enum value.
        observed = []

        def spy(draft):
            observed.append(mirror_state(self.w, self.key))
            return False

        with tempfile.TemporaryDirectory() as d:
            self.w, self.a = build_instance(d)
            # capture the key the gate will allocate
            self.key = "demo-p1"
            wg.propose(self.w, self.a, _decision(), "SAW-30", "Praetor",
                       now=TS, auto_ingest=spy)
            self.assertEqual(observed, ["validated"])


class RejectedMalformed(unittest.TestCase):
    def test_missing_per_kind_field_is_persisted_not_raised(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            bad = make_proposal(kind="decision", ticket="SAW-30", agent="Praetor")  # no scope
            r = wg.propose(w, a, bad, "SAW-30", "Praetor", now=TS)
            self.assertEqual(r["state"], "rejected-malformed")
            self.assertIn("scope", r["reason"])
            self.assertEqual(mirror_state(w, r["proposal_key"]), "rejected-malformed")
            # rejected-malformed cannot be resolved
            with self.assertRaises(AntechamberError):
                wg.resolve(w, a, r["proposal_key"], "ingested", now=TS)


class AutoIngest(unittest.TestCase):
    def test_promoted_class_skips_the_senate(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            r = wg.propose(w, a, _decision(), "SAW-30", "Praetor", now=TS,
                           auto_ingest=lambda draft: True)
            self.assertEqual(r["state"], "auto-ingested")
            self.assertEqual(r["node_id"], "demo-n13")
            self.assertEqual(mirror_state(w, r["proposal_key"]), "auto-ingested")


class ReviseLoop(unittest.TestCase):
    def test_revise_reenters_at_proposed_then_ingests(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            r = wg.propose(w, a, _decision(), "SAW-30", "Praetor", now=TS)
            key = r["proposal_key"]
            back = wg.resolve(w, a, key, "revise", now=TS)
            self.assertEqual(back["state"], "proposed")
            # the agent resubmits revised content -> new round, new append-only file
            r2 = wg.revise(w, a, key, _decision(title="Adopt event sourcing v2"), now=TS)
            self.assertEqual(r2["state"], "pending-senate")
            self.assertEqual(r2["round"], 2)
            self.assertTrue((a / f"{key}.r2.md").exists())
            self.assertTrue((a / f"{key}.md").exists())  # round-1 content kept
            res = wg.resolve(w, a, key, "ingested", now=TS)
            self.assertEqual(res["state"], "ingested")
            node = store.read_node_file(w / "nodes" / (res["node_id"] + ".md"))
            self.assertEqual(node.title, "Adopt event sourcing v2")

    def test_revise_only_applies_to_a_sent_back_proposal(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            r = wg.propose(w, a, _decision(), "SAW-30", "Praetor", now=TS)
            with self.assertRaises(AntechamberError):  # still pending-senate
                wg.revise(w, a, r["proposal_key"], _decision(), now=TS)

    def test_revise_loop_is_bounded(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            r = wg.propose(w, a, _decision(), "SAW-30", "Praetor", now=TS)
            key = r["proposal_key"]
            # limit=2: round1 revise ok -> round2; round2 revise -> escalate
            wg.resolve(w, a, key, "revise", now=TS, revise_limit=2)
            wg.revise(w, a, key, _decision(), now=TS)  # round 2, back to pending
            with self.assertRaises(RevisionLimitReached) as ctx:
                wg.resolve(w, a, key, "revise", now=TS, revise_limit=2)
            self.assertEqual(ctx.exception.packet["round"], 2)
            self.assertEqual(mirror_state(w, key), "pending-senate")  # unchanged


class IdMonopoly(unittest.TestCase):
    def test_ingest_allocates_from_counter_not_markdown_max(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            # fixtures occupy demo-n1..n12 -> counter at 13
            counter = schema.connect(w / schema.INDEX_FILENAME).execute(
                "SELECT next_value FROM id_counter WHERE plane='n'").fetchone()[0]
            self.assertEqual(counter, 13)
            ids = []
            for _ in range(3):
                r = wg.propose(w, a, _decision(), "SAW-30", "Praetor", now=TS)
                ids.append(wg.resolve(w, a, r["proposal_key"], "ingested", now=TS)["node_id"])
            self.assertEqual(ids, ["demo-n13", "demo-n14", "demo-n15"])

    def test_crash_skipped_id_is_a_gap_not_a_collision(self):
        # Simulate a crash after the id burn but before the markdown write by
        # advancing the counter out of band; the next ingest must NOT reuse it.
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            conn = schema.connect(w / schema.INDEX_FILENAME)
            with conn:
                conn.execute("UPDATE id_counter SET next_value = 14 WHERE plane='n'")
            conn.close()
            r = wg.propose(w, a, _decision(), "SAW-30", "Praetor", now=TS)
            res = wg.resolve(w, a, r["proposal_key"], "ingested", now=TS)
            self.assertEqual(res["node_id"], "demo-n14")  # 13 skipped, never reused

    def test_flag_proposal_allocates_on_the_audit_plane(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            flag = make_proposal(kind="flag", flag_type="orphan", origin="observed",
                                 title="Orphan: demo-n11", edges=[("flags", "demo-n11")])
            r = wg.propose(w, a, flag, "SAW-30", "Curator", now=TS)
            res = wg.resolve(w, a, r["proposal_key"], "ingested", now=TS)
            self.assertEqual(res["node_id"], "demo-f3")  # f1,f2 fixtures -> f3
            self.assertTrue((w / "flags" / "demo-f3.md").exists())


if __name__ == "__main__":
    unittest.main()
