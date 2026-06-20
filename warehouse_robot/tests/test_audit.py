"""B5 — audit tripwire unit tests (A14/A16).

Deterministic, graph-structural tripwires that ONLY flag, never mutate. Every
test runs against a disposable instance under the system tmp directory (A4/
A12). The library API (`audit.audit`) is exercised here; the CLI surface is in
test_cli_audit, the versioned fixtures in test_audit_fixtures, and the L1/L2
end-to-end legs in test_vertical_slice / test_cli_session.
"""

import tempfile
import unittest
from pathlib import Path

from warehouse_robot import audit, config, fold, schema, store, write_gate
from warehouse_robot.errors import AuditError
from warehouse_robot.store import Edge

from ._audit_helpers import build_broken_instance, build_clean_instance
from ._fold_helpers import fold_fixtures, init_instance, query_all, query_one

TS = "2026-06-20T12:00:00Z"


def append(wroot, *, kind, title, body="Body text.\n", edges=(), now=TS, **fields):
    """Append a knowledge node through the shared allocation primitive (the
    same path the gate uses) so tests can build arbitrary graph shapes."""
    cfg = config.load_config(wroot)
    conn = schema.connect(Path(wroot) / schema.INDEX_FILENAME)
    try:
        node_id, _ = write_gate.append_node(
            conn, wroot, cfg, kind=kind, status=fields.pop("status", "active"),
            title=title, origin=fields.pop("origin", "decided"), body=body,
            now=now, edges=[Edge(t, tgt) for t, tgt in edges], **fields,
        )
    finally:
        conn.close()
    return node_id


def run_audit(wroot):
    return audit.audit(wroot, now=TS)


class CleanGraph(unittest.TestCase):
    def test_clean_fixture_graph_produces_zero_flags(self):
        """A16 no-false-positives control: a well-connected graph flags nothing."""
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            r = run_audit(w)
            self.assertEqual(r["emitted"], [])
            self.assertEqual(r["skipped_existing"], [])
            self.assertEqual(r["open_flag_count"], 0)
            self.assertEqual(r["heat"], [])

    def test_demo_graph_emits_no_new_flags(self):
        """The realistic demo graph: the only orphan (demo-n11) is already
        flagged, the only edge-less inherited node (demo-n12) is foundational —
        so a live audit emits nothing new (foundational exclusion + idempotency
        + knowledge-edges-only all at once)."""
        with tempfile.TemporaryDirectory() as d:
            w = init_instance(d)
            fold_fixtures(w)
            r = run_audit(w)
            self.assertEqual(r["emitted"], [])
            self.assertEqual(
                r["skipped_existing"],
                [{"target": "demo-n11", "flag_type": "orphan"}],
            )
            self.assertEqual(r["open_flag_count"], 1)  # demo-f1 stands


class Orphan(unittest.TestCase):
    def test_orphan_detected_excludes_audit_plane_edges(self):
        """demo-n11's ONLY edge is the inbound `flags` edge from demo-f1, yet it
        is still an orphan — audit-plane edges are not knowledge connectivity."""
        with tempfile.TemporaryDirectory() as d:
            w = init_instance(d)
            fold_fixtures(w)
            conn = schema.connect(w / schema.INDEX_FILENAME)
            try:
                ids = [r[0] for r in audit._find_orphans(conn)]
            finally:
                conn.close()
            self.assertIn("demo-n11", ids)       # only-edge-is-a-flag → still orphan
            self.assertNotIn("demo-n12", ids)    # inherited → foundational, excluded

    def test_foundational_inherited_node_is_not_an_orphan(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            # an edge-less INHERITED constraint must be excused (platform axiom)
            foundational = append(w, kind="constraint", title="Inherited axiom",
                                  origin="inherited", source="platform")
            r = run_audit(w)
            self.assertNotIn(foundational, [e["target"] for e in r["emitted"]])
            self.assertEqual(r["open_flag_count"], 0)

    def test_edge_less_decision_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            orphan = append(w, kind="decision", title="Lonely decision",
                            scope="tooling", origin="decided")
            r = run_audit(w)
            self.assertEqual(
                [e for e in r["emitted"] if e["flag_type"] == "orphan"],
                [{"flag_id": "demo-f1", "target": orphan, "flag_type": "orphan"}],
            )

    def test_retired_edge_less_node_is_not_flagged(self):
        """G-D: the audit watches the LIVE graph — a retired node is
        deliberately dead, flagging it is noise."""
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            append(w, kind="decision", title="Retired and isolated",
                   scope="tooling", origin="decided", status="retired")
            r = run_audit(w)
            self.assertEqual(r["emitted"], [])


class RelatesToOveruse(unittest.TestCase):
    def test_at_threshold_not_flagged_over_threshold_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            five = [("relates-to", f"demo-n{i}") for i in range(1, 6)]
            at_k = append(w, kind="decision", title="Exactly K relations",
                          scope="ui", edges=five)
            r = run_audit(w)
            self.assertEqual(
                [e for e in r["emitted"] if e["flag_type"] == "relates-to-overuse"],
                [],
            )  # K=5 is not > K
            over = append(w, kind="decision", title="Over K relations",
                          scope="ui", edges=five + [("relates-to", "demo-n7")])
            r2 = run_audit(w)
            overuse = [e for e in r2["emitted"] if e["flag_type"] == "relates-to-overuse"]
            self.assertEqual([e["target"] for e in overuse], [over])

    def test_overuse_counts_source_not_target(self):
        """'Carrying' = the edges the node declares (it is the src)."""
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            hub = append(w, kind="decision", title="A popular target", scope="ui")
            # six DIFFERENT decisions each relate-to the hub; the hub is the
            # target of 6 edges but the SOURCE of none → not overuse.
            for i in range(6):
                append(w, kind="decision", title=f"Pointer {i}", scope="ui",
                       edges=[("relates-to", hub)])
            r = run_audit(w)
            self.assertEqual(
                [e for e in r["emitted"] if e["flag_type"] == "relates-to-overuse"],
                [],
            )


class MissingRecommendedEdge(unittest.TestCase):
    def test_lesson_without_about_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            # a lesson kept off the orphan list by a weak relates-to, but
            # missing its recommended about edge
            lesson = append(w, kind="lesson", title="Lesson sans about",
                            origin="observed", ticket="T-1", agent="Probator",
                            edges=[("relates-to", "demo-n1")])
            r = run_audit(w)
            self.assertEqual(
                [e for e in r["emitted"] if e["flag_type"] == "missing-recommended-edge"],
                [{"flag_id": "demo-f1", "target": lesson,
                  "flag_type": "missing-recommended-edge"}],
            )

    def test_lesson_with_about_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            append(w, kind="lesson", title="Compliant lesson", origin="observed",
                   ticket="T-1", agent="Probator", edges=[("about", "demo-n1")])
            r = run_audit(w)
            self.assertEqual(r["emitted"], [])

    def test_decision_without_about_is_not_flagged(self):
        """Only kinds in the seeded table are checked — no invented rules."""
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            append(w, kind="decision", title="A connected decision", scope="ui",
                   edges=[("derived-from", "demo-n1")])
            r = run_audit(w)
            self.assertEqual(
                [e for e in r["emitted"] if e["flag_type"] == "missing-recommended-edge"],
                [],
            )


class MultipleFlagsHeat(unittest.TestCase):
    def test_edge_less_lesson_trips_orphan_and_missing_edge(self):
        """A node may carry multiple independent flags; node 'heat' aggregates
        the open flags (S6)."""
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            lonely_lesson = append(w, kind="lesson", title="Isolated lesson",
                                   origin="observed", ticket="T-9", agent="Probator")
            r = run_audit(w)
            kinds = sorted(e["flag_type"] for e in r["emitted"]
                           if e["target"] == lonely_lesson)
            self.assertEqual(kinds, ["missing-recommended-edge", "orphan"])
            self.assertIn({"target": lonely_lesson, "open_flags": 2}, r["heat"])


class Idempotency(unittest.TestCase):
    def test_rerun_does_not_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_broken_instance(d)
            first = run_audit(w)
            self.assertEqual(len(first["emitted"]), 3)
            before = query_one(w, "SELECT COUNT(*) FROM nodes WHERE plane='f'")[0]
            second = run_audit(w)
            self.assertEqual(second["emitted"], [])
            self.assertEqual(len(second["skipped_existing"]), 3)
            after = query_one(w, "SELECT COUNT(*) FROM nodes WHERE plane='f'")[0]
            self.assertEqual(before, after)  # no new flag nodes minted

    def test_resolved_flag_does_not_block_reemission(self):
        """PC5: a *resolved* flag does not suppress a still-standing condition —
        a recurrence after resolution is a real new finding."""
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            orphan = append(w, kind="decision", title="Lonely", scope="tooling")
            first = run_audit(w)
            flag_id = first["emitted"][0]["flag_id"]
            # resolve the flag: a resolves edge from a knowledge node → the flag
            append(w, kind="decision", title="Resolver", scope="tooling",
                   edges=[("resolves", flag_id)])
            self.assertEqual(
                query_one(w, "SELECT flag_status FROM v_flag_status WHERE id=?",
                          (flag_id,))[0],
                "resolved",
            )
            # the orphan still stands → a NEW flag is emitted (not blocked)
            second = run_audit(w)
            reemitted = [e for e in second["emitted"]
                         if e["target"] == orphan and e["flag_type"] == "orphan"]
            self.assertEqual(len(reemitted), 1)
            self.assertNotEqual(reemitted[0]["flag_id"], flag_id)


class FlagOnly(unittest.TestCase):
    def test_target_node_is_never_mutated(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            orphan = append(w, kind="decision", title="Untouched", scope="tooling")
            before = query_one(
                w, "SELECT title, body, content_hash, status FROM nodes WHERE id=?",
                (orphan,))
            run_audit(w)
            after = query_one(
                w, "SELECT title, body, content_hash, status FROM nodes WHERE id=?",
                (orphan,))
            self.assertEqual(before, after)
            # and no edge was added FROM or the knowledge node was rewritten —
            # the only new edge is the flag's `flags` edge pointing AT it
            out_edges = query_all(w, "SELECT type FROM edges WHERE src=?", (orphan,))
            self.assertEqual(out_edges, [])

    def test_emitted_flag_is_a_valid_open_node_with_severity(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            orphan = append(w, kind="decision", title="Lonely", scope="tooling")
            run_audit(w)
            flag_path = Path(w) / store.FLAGS_DIR / "demo-f1.md"
            node = store.read_node_file(flag_path)  # round-trips through the codec
            self.assertEqual(node.kind, "flag")
            self.assertEqual(node.flag_type, "orphan")
            self.assertEqual(node.origin, "observed")
            self.assertEqual([(e.type, e.target) for e in node.edges],
                             [("flags", orphan)])
            self.assertIn("severity:", node.body)
            self.assertEqual(
                query_one(w, "SELECT flag_status FROM v_flag_status WHERE id=?",
                          (node.id,))[0],
                "open",
            )


class FlagsSurviveReconcile(unittest.TestCase):
    def test_flags_survive_a_reconcile_rebuild(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_broken_instance(d)
            run_audit(w)
            live = fold.logical_digest_of(w / schema.INDEX_FILENAME)
            fold.rebuild(w)
            # the flag nodes are canonical f-plane markdown → folded back, and
            # the live index already matched a fresh rebuild (A8 part 2)
            self.assertEqual(fold.logical_digest_of(w / schema.INDEX_FILENAME), live)
            self.assertTrue(fold.check(w).clean)
            self.assertEqual(
                query_one(w, "SELECT COUNT(*) FROM nodes WHERE plane='f'")[0], 3)
            # re-running the audit after a rebuild is still idempotent
            self.assertEqual(run_audit(w)["emitted"], [])


class Errors(unittest.TestCase):
    def test_audit_without_index_raises(self):
        with tempfile.TemporaryDirectory() as d:
            w = init_instance(d)
            (w / schema.INDEX_FILENAME).unlink()
            with self.assertRaises(AuditError):
                run_audit(w)


if __name__ == "__main__":
    unittest.main()
