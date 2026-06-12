"""Incremental upsert — the fold's hot path (B2).

Each test builds a disposable instance under the system tmp directory,
folds fixture files into it, asserts against the index, and deletes the
instance (A4 discipline).
"""

import tempfile
import unittest
from pathlib import Path

from warehouse_robot import fold, schema, store
from warehouse_robot.errors import FoldError
from warehouse_robot.ids import AUDIT_PLANE, KNOWLEDGE_PLANE, parse_id

from . import _fold_helpers as h


def fixture_nodes():
    paths = sorted(h.FIXTURES_ROOT.glob("nodes/*.md")) + sorted(h.FIXTURES_ROOT.glob("flags/*.md"))
    return [store.read_node_file(p) for p in paths]


class UpsertTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.wroot = h.init_instance(self._tmp.name)

    def test_single_upsert_mirrors_node_edges_fts_and_counter(self):
        h.copy_fixtures(self.wroot)
        path = self.wroot / "nodes" / "demo-n7.md"
        conn = schema.connect(h.index_path(self.wroot))
        try:
            node = fold.upsert_node_file(conn, self.wroot, path, expected_prefix="demo")
            row = conn.execute(
                "SELECT id, kind, title, content_hash, file_path FROM nodes WHERE id = 'demo-n7'"
            ).fetchone()
            self.assertEqual(row[0], "demo-n7")
            self.assertEqual(row[1], node.kind)
            self.assertEqual(row[3], store.content_hash(path.read_text(encoding="utf-8")))
            self.assertEqual(row[4], "nodes/demo-n7.md")
            edges = conn.execute(
                "SELECT type, target FROM edges WHERE src = 'demo-n7' ORDER BY type, target"
            ).fetchall()
            self.assertEqual(edges, sorted((e.type, e.target) for e in node.edges))
            fts_ids = [
                r[0] for r in conn.execute(
                    "SELECT n.id FROM nodes_fts f JOIN nodes n ON n.rowid = f.rowid "
                    "WHERE nodes_fts MATCH ?", (node.title.split()[0].lower(),)
                )
            ]
            self.assertIn("demo-n7", fts_ids)
            next_n = conn.execute(
                "SELECT next_value FROM id_counter WHERE plane = ?", (KNOWLEDGE_PLANE,)
            ).fetchone()[0]
            self.assertEqual(next_n, 8)  # max folded number + 1
        finally:
            conn.close()

    def test_folding_all_fixtures_mirrors_counts_and_counters(self):
        h.fold_fixtures(self.wroot)
        expected = fixture_nodes()
        node_count = h.query_one(self.wroot, "SELECT count(*) FROM nodes")[0]
        edge_count = h.query_one(self.wroot, "SELECT count(*) FROM edges")[0]
        self.assertEqual(node_count, len(expected))
        self.assertEqual(edge_count, sum(len(n.edges) for n in expected))
        counters = dict(h.query_all(self.wroot, "SELECT plane, next_value FROM id_counter"))
        max_per_plane = {KNOWLEDGE_PLANE: 0, AUDIT_PLANE: 0}
        for node in expected:
            _, plane, number = parse_id(node.id)
            max_per_plane[plane] = max(max_per_plane[plane], number)
        self.assertEqual(counters[KNOWLEDGE_PLANE], max_per_plane[KNOWLEDGE_PLANE] + 1)
        self.assertEqual(counters[AUDIT_PLANE], max_per_plane[AUDIT_PLANE] + 1)

    def test_derived_status_views_after_fold(self):
        h.fold_fixtures(self.wroot)
        effective = dict(h.query_all(self.wroot, "SELECT id, effective_status FROM v_effective_status"))
        self.assertEqual(effective["demo-n2"], "superseded")  # incoming supersedes edge
        self.assertEqual(effective["demo-n7"], "active")
        flags = dict(h.query_all(self.wroot, "SELECT id, flag_status FROM v_flag_status"))
        self.assertEqual(flags["demo-f1"], "open")
        self.assertEqual(flags["demo-f2"], "resolved")

    def test_refold_is_idempotent(self):
        paths = h.fold_fixtures(self.wroot)
        before = fold.logical_digest_of(h.index_path(self.wroot))
        conn = schema.connect(h.index_path(self.wroot))
        try:
            for path in paths:
                fold.upsert_node_file(conn, self.wroot, path, expected_prefix="demo")
        finally:
            conn.close()
        self.assertEqual(fold.logical_digest_of(h.index_path(self.wroot)), before)

    def test_upsert_mirrors_a_hand_edited_file(self):
        # Markdown is truth: the fold mirrors the file as-is; detecting the
        # append-only violation is the job of check / the B5 audit.
        paths = h.fold_fixtures(self.wroot)
        path = self.wroot / "nodes" / "demo-n12.md"
        node = store.read_node_file(path)
        node.body = "Edited body — an append-only violation the fold must still mirror.\n"
        path.write_text(store.serialize_node(node), encoding="utf-8")
        conn = schema.connect(h.index_path(self.wroot))
        try:
            fold.upsert_node_file(conn, self.wroot, path, expected_prefix="demo")
        finally:
            conn.close()
        row = h.query_one(self.wroot, "SELECT body, content_hash FROM nodes WHERE id = 'demo-n12'")
        self.assertEqual(row[0], node.body)
        self.assertEqual(row[1], store.content_hash(path.read_text(encoding="utf-8")))
        fts_hit = h.query_all(
            self.wroot,
            "SELECT n.id FROM nodes_fts f JOIN nodes n ON n.rowid = f.rowid "
            "WHERE nodes_fts MATCH 'violation'",
        )
        self.assertIn(("demo-n12",), fts_hit)  # FTS followed the new content

    def test_upsert_rejects_foreign_prefix(self):
        h.copy_fixtures(self.wroot)
        path = self.wroot / "nodes" / "demo-n1.md"
        conn = schema.connect(h.index_path(self.wroot))
        try:
            with self.assertRaisesRegex(FoldError, "foreign|prefix"):
                fold.upsert_node_file(conn, self.wroot, path, expected_prefix="other")
        finally:
            conn.close()

    def test_upsert_rejects_misplaced_file(self):
        h.copy_fixtures(self.wroot)
        src = self.wroot / "nodes" / "demo-n3.md"
        misplaced = self.wroot / "flags" / "demo-n3.md"
        misplaced.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        conn = schema.connect(h.index_path(self.wroot))
        try:
            with self.assertRaisesRegex(FoldError, "misplaced"):
                fold.upsert_node_file(conn, self.wroot, misplaced, expected_prefix="demo")
        finally:
            conn.close()

    def test_upsert_rejects_filename_id_mismatch(self):
        h.copy_fixtures(self.wroot)
        src = self.wroot / "nodes" / "demo-n3.md"
        renamed = self.wroot / "nodes" / "demo-n99.md"
        renamed.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        conn = schema.connect(h.index_path(self.wroot))
        try:
            with self.assertRaisesRegex(FoldError, "does not match node id"):
                fold.upsert_node_file(conn, self.wroot, renamed, expected_prefix="demo")
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
