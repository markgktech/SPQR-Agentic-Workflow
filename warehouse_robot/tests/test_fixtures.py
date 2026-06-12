"""Fixture-set integrity (A4: fixtures are the robot's versioned regression assets).

These tests assert that every shipped fixture node is canonical (parses and
round-trips byte-identically), that the fixture graph is internally closed,
and that the set covers both planes, all three knowledge kinds, and the full
edge ontology — so every later ticket (B2 fold, B3 queries, B4 gate, B5
tripwires) can rely on the same fixture warehouse.
"""

import unittest
from pathlib import Path

from warehouse_robot.ids import AUDIT_PLANE, KNOWLEDGE_PLANE, parse_id
from warehouse_robot.store import (
    EDGE_TYPES,
    KNOWLEDGE_KINDS,
    parse_node_text,
    read_node_file,
    serialize_node,
)

FIXTURES_ROOT = Path(__file__).resolve().parent.parent / "fixtures"


def fixture_paths():
    paths = sorted(FIXTURES_ROOT.glob("nodes/*.md")) + sorted(FIXTURES_ROOT.glob("flags/*.md"))
    assert paths, f"no fixtures found under {FIXTURES_ROOT}"
    return paths


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.nodes = [read_node_file(p) for p in fixture_paths()]
        self.by_id = {n.id: n for n in self.nodes}

    def test_every_fixture_round_trips_byte_identically(self):
        for path in fixture_paths():
            text = path.read_text(encoding="utf-8")
            self.assertEqual(
                serialize_node(parse_node_text(text)), text,
                f"fixture is not in canonical form: {path.name}",
            )

    def test_ids_unique_and_demo_prefixed(self):
        ids = [n.id for n in self.nodes]
        self.assertEqual(len(ids), len(set(ids)))
        for node_id in ids:
            prefix, _, _ = parse_id(node_id)
            self.assertEqual(prefix, "demo", node_id)

    def test_fixture_count_in_mandated_band(self):
        knowledge = [n for n in self.nodes if n.plane == KNOWLEDGE_PLANE]
        self.assertGreaterEqual(len(knowledge), 10)  # A4: 10–15 sample nodes
        self.assertLessEqual(len(knowledge), 15)

    def test_planes_match_directories(self):
        for path in fixture_paths():
            node = read_node_file(path)
            expected_dir = "nodes" if node.plane == KNOWLEDGE_PLANE else "flags"
            self.assertEqual(path.parent.name, expected_dir, node.id)

    def test_edge_targets_stay_inside_the_fixture_set(self):
        for node in self.nodes:
            for edge in node.edges:
                self.assertIn(
                    edge.target, self.by_id,
                    f"{node.id} points outside the fixture set: {edge.type} -> {edge.target}",
                )

    def test_coverage_of_kinds_planes_and_edge_ontology(self):
        kinds = {n.kind for n in self.nodes if n.plane == KNOWLEDGE_PLANE}
        self.assertEqual(kinds, set(KNOWLEDGE_KINDS))
        planes = {n.plane for n in self.nodes}
        self.assertEqual(planes, {KNOWLEDGE_PLANE, AUDIT_PLANE})
        used_edge_types = {e.type for n in self.nodes for e in n.edges}
        self.assertEqual(used_edge_types, set(EDGE_TYPES))
        verdicts = {n.verdict for n in self.nodes if n.kind == "lesson"}
        self.assertEqual(verdicts, {"GREEN", "YELLOW", "RED"})

    def test_supersede_and_resolve_pairs_present(self):
        # B2/B5 rely on one derived-superseded node and one open + one resolved flag.
        superseded_targets = {
            e.target for n in self.nodes for e in n.edges if e.type == "supersedes"
        }
        self.assertEqual(superseded_targets, {"demo-n2"})
        resolved_flags = {
            e.target for n in self.nodes for e in n.edges if e.type == "resolves"
        }
        flag_ids = {n.id for n in self.nodes if n.plane == AUDIT_PLANE}
        self.assertEqual(resolved_flags, {"demo-f2"})
        self.assertIn("demo-f1", flag_ids - resolved_flags)  # stays open

    def test_orphan_fixture_present_for_b5(self):
        linked = {e.target for n in self.nodes for e in n.edges}
        linked |= {n.id for n in self.nodes if n.edges}
        knowledge_ids = {n.id for n in self.nodes if n.plane == KNOWLEDGE_PLANE}
        orphans = knowledge_ids - linked
        self.assertIn("demo-n12", orphans)  # truly edge-free constraint
        # demo-n11 is edge-free itself but watched by flag demo-f1 (flags edge),
        # which is exactly the orphan-watch scenario B5 will exercise.
        n11 = self.by_id["demo-n11"]
        self.assertEqual(n11.edges, [])


if __name__ == "__main__":
    unittest.main()
