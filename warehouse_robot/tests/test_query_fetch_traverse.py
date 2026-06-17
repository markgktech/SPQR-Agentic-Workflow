"""fetch + traverse (B3): phase-2 retrieval and the SCRUTINIZE DENY.

fetch returns bodies + the edge TOC for explicitly selected IDs; traverse is
bounded typed-edge neighborhood expansion in both edge directions. The S4
structural DENY is enforced here: SCRUTINIZE cannot traverse lineage
(`supersedes` / `derived-from`) or journey memory (`about`), and those edge
TOC rows are hidden — visibly, never silently.
"""

import tempfile
import unittest

from warehouse_robot import fold, schema, store
from warehouse_robot.errors import PolicyDenied, ProtocolError

from . import _fold_helpers as h
from . import _query_helpers as q


class FetchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.wroot = q.build_instance(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def call(self, session, ids, **kw):
        response = q.q_fetch(self.wroot, ids, session=session, **kw)
        q.q_verdict(self.wroot, "FOUND-ENOUGH", session=session)
        return response

    def test_fetch_returns_body_and_full_edge_toc(self):
        response = self.call("ft-1", ["demo-n7"])
        (node,) = response["nodes"]
        self.assertEqual(node["id"], "demo-n7")
        self.assertIn("Result-based envelopes", node["body"])
        self.assertEqual(node["status"], "active")
        out = [(e["type"], e["id"]) for e in node["edges"]["out"]]
        self.assertEqual(
            out,
            [("derived-from", "demo-n1"), ("resolves", "demo-f2"),
             ("supersedes", "demo-n2")],
        )
        incoming = [(e["type"], e["id"]) for e in node["edges"]["in"]]
        self.assertEqual(incoming, [("about", "demo-n10")])
        # TOC rows are skeletons of the neighbor, not bodies.
        self.assertEqual(node["edges"]["in"][0]["kind"], "lesson")
        self.assertNotIn("body", node["edges"]["in"][0])

    def test_fetch_by_explicit_id_ignores_the_status_filter(self):
        response = self.call("ft-2", ["demo-n2"])
        (node,) = response["nodes"]
        self.assertEqual(node["status"], "superseded")
        self.assertIn("typed error envelope", node["body"])

    def test_missing_ids_are_reported_not_fatal(self):
        response = self.call("ft-3", ["demo-n1", "demo-n99"])
        self.assertEqual([n["id"] for n in response["nodes"]], ["demo-n1"])
        self.assertEqual(response["not_found"], ["demo-n99"])

    def test_selection_validation(self):
        for bad in ([], ["demo-n1", "demo-n1"], ["not an id"], "demo-n1"):
            with self.assertRaises(ProtocolError):
                q.q_fetch(self.wroot, bad, session="ft-4")

    def test_scrutinize_sees_no_lineage_edges(self):
        response = self.call("ft-5", ["demo-n7"], archetype="scrutinize")
        (node,) = response["nodes"]
        out = [(e["type"], e["id"]) for e in node["edges"]["out"]]
        self.assertEqual(out, [("resolves", "demo-f2")])
        self.assertEqual(node["edges"]["in"], [])  # the about-lesson is hidden
        # The hiding is declared, never silent (Law 4).
        self.assertEqual(
            response["hidden_edge_types"],
            ["about", "derived-from", "supersedes"],
        )

    def test_non_scrutinize_response_has_no_hidden_marker(self):
        response = self.call("ft-6", ["demo-n7"])
        self.assertNotIn("hidden_edge_types", response)


class TraverseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.wroot = q.build_instance(cls._tmp.name)
        # A depth-2 derived-from chain on top of the fixtures, built inside
        # the disposable instance only: demo-n13 -> demo-n7 -> demo-n1.
        node = store.Node(
            id="demo-n13", kind="decision", status="active",
            title="Error envelopes carry a stable error code",
            origin="decided", timestamp="2026-06-08T09:00:00Z",
            schema_version=1, scope="error-handling", ticket="DEMO-7",
            agent="Praetor",
            body="Each Result-based envelope exposes a stable code field.\n",
            edges=[store.Edge(type="derived-from", target="demo-n7")],
        )
        path = store.write_node_file(cls.wroot, node)
        conn = schema.connect(h.index_path(cls.wroot))
        try:
            fold.upsert_node_file(conn, cls.wroot, path, expected_prefix="demo")
        finally:
            conn.close()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def call(self, session, node_id, edge_type, **kw):
        response = q.q_traverse(self.wroot, node_id, edge_type,
                                session=session, **kw)
        q.q_verdict(self.wroot, "FOUND-ENOUGH", session=session)
        return response

    def test_traverse_follows_both_edge_directions(self):
        response = self.call("tr-1", "demo-n2", "supersedes")
        self.assertEqual(
            response["steps"],
            [{"level": 1, "from": "demo-n2", "direction": "in", "to": "demo-n7"}],
        )
        self.assertEqual([n["id"] for n in response["nodes"]], ["demo-n7"])

    def test_depth_two_walks_the_chain(self):
        shallow = self.call("tr-2", "demo-n1", "derived-from", depth=1)
        self.assertEqual([n["id"] for n in shallow["nodes"]], ["demo-n7"])
        deep = self.call("tr-3", "demo-n1", "derived-from", depth=2)
        self.assertEqual(
            [n["id"] for n in deep["nodes"]], ["demo-n7", "demo-n13"]
        )
        levels = {s["to"]: s["level"] for s in deep["steps"]}
        self.assertEqual(levels, {"demo-n7": 1, "demo-n13": 2})

    def test_an_edge_is_reported_once(self):
        # Depth 2 from demo-n2: level 1 discovers demo-n7 via the supersedes
        # edge; level 2 must not re-report the same edge from the other side.
        response = self.call("tr-4", "demo-n2", "supersedes", depth=2)
        self.assertEqual(len(response["steps"]), 1)

    def test_origin_skeleton_is_included(self):
        response = self.call("tr-5", "demo-n2", "supersedes")
        self.assertEqual(response["origin"]["id"], "demo-n2")
        self.assertEqual(response["origin"]["status"], "superseded")

    def test_scrutinize_lineage_traversal_is_denied(self):
        for edge_type in ("supersedes", "derived-from", "about"):
            with self.assertRaisesRegex(PolicyDenied, "SCRUTINIZE DENY"):
                q.q_traverse(self.wroot, "demo-n7", edge_type,
                             session="tr-6", archetype="scrutinize")

    def test_scrutinize_may_traverse_non_lineage_edges(self):
        response = self.call("tr-7", "demo-n1", "constrains",
                             archetype="scrutinize")
        self.assertEqual([n["id"] for n in response["nodes"]], ["demo-n3"])

    def test_parameter_validation(self):
        with self.assertRaisesRegex(ProtocolError, "unknown edge type"):
            q.q_traverse(self.wroot, "demo-n1", "links-to", session="tr-8")
        for bad_depth in (0, -1, True):
            with self.assertRaises(ProtocolError):
                q.q_traverse(self.wroot, "demo-n1", "constrains",
                             session="tr-8", depth=bad_depth)
        with self.assertRaisesRegex(ProtocolError, "exceeds the policy maximum"):
            q.q_traverse(self.wroot, "demo-n1", "constrains",
                         session="tr-8", depth=4)
        with self.assertRaisesRegex(ProtocolError, "origin not found"):
            q.q_traverse(self.wroot, "demo-n99", "constrains", session="tr-8")
        with self.assertRaisesRegex(ProtocolError, "origin invalid"):
            q.q_traverse(self.wroot, "DEMO N1", "constrains", session="tr-8")
