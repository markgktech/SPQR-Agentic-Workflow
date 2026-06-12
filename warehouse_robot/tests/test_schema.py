import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from warehouse_robot import schema
from warehouse_robot.errors import SchemaError

EXPECTED_OBJECTS = {
    "meta",
    "nodes",
    "edges",
    "nodes_fts",
    "id_counter",
    "antechamber",
    "trace",
    "v_effective_status",
    "v_flag_status",
}


def insert_node(conn, node_id, plane, kind, **overrides):
    row = dict(
        id=node_id,
        plane=plane,
        kind=kind,
        status="active",
        title=f"Title of {node_id}",
        scope=None,
        verdict=None,
        flag_type=None,
        origin="decided",
        timestamp="2026-06-01T09:00:00Z",
        ticket=None,
        agent=None,
        source=None,
        schema_version=1,
        body=f"Body of {node_id}.",
        content_hash="0" * 64,
        file_path=f"nodes/{node_id}.md",
    )
    row.update(overrides)
    conn.execute(
        """INSERT INTO nodes (id, plane, kind, status, title, scope, verdict,
                              flag_type, origin, timestamp, ticket, agent, source,
                              schema_version, body, content_hash, file_path)
           VALUES (:id, :plane, :kind, :status, :title, :scope, :verdict,
                   :flag_type, :origin, :timestamp, :ticket, :agent, :source,
                   :schema_version, :body, :content_hash, :file_path)""",
        row,
    )


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.db_path = Path(self._tmp.name) / schema.INDEX_FILENAME
        schema.create_index(self.db_path, "demo", 1)
        self.conn = schema.connect(self.db_path)
        self.addCleanup(self.conn.close)

    def names(self):
        rows = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table', 'view')"
        ).fetchall()
        return {r[0] for r in rows}

    def test_all_objects_exist(self):
        self.assertTrue(EXPECTED_OBJECTS.issubset(self.names()))

    def test_wal_mode_persists(self):
        mode = self.conn.execute("PRAGMA journal_mode").fetchone()[0]
        self.assertEqual(mode, "wal")

    def test_meta_and_counters_seeded(self):
        meta = dict(self.conn.execute("SELECT key, value FROM meta"))
        self.assertEqual(meta["schema_version"], "1")
        self.assertEqual(meta["project_prefix"], "demo")
        self.assertIn("created_at", meta)
        counters = dict(self.conn.execute("SELECT plane, next_value FROM id_counter"))
        self.assertEqual(counters, {"n": 1, "f": 1})

    def test_create_refuses_existing_index(self):
        with self.assertRaisesRegex(SchemaError, "already exists"):
            schema.create_index(self.db_path, "demo", 1)

    def test_check_constraints(self):
        with self.assertRaises(sqlite3.IntegrityError):  # unknown plane
            insert_node(self.conn, "demo-x1", "x", "decision")
        with self.assertRaises(sqlite3.IntegrityError):  # flag kind off the audit plane
            insert_node(self.conn, "demo-n1", "n", "flag")
        with self.assertRaises(sqlite3.IntegrityError):  # knowledge kind on the audit plane
            insert_node(self.conn, "demo-f1", "f", "decision")
        with self.assertRaises(sqlite3.IntegrityError):  # stored 'superseded' is forbidden
            insert_node(self.conn, "demo-n1", "n", "decision", status="superseded")
        with self.assertRaises(sqlite3.IntegrityError):  # bad verdict
            insert_node(self.conn, "demo-n1", "n", "lesson", verdict="OK")
        with self.assertRaises(sqlite3.IntegrityError):  # bad trace verb
            self.conn.execute(
                "INSERT INTO trace (ts, verb, intent) VALUES ('t', 'grep', 'i')"
            )
        with self.assertRaises(sqlite3.IntegrityError):  # bad antechamber state
            self.conn.execute(
                """INSERT INTO antechamber (proposal_key, state, ticket, agent,
                                            created_at, updated_at, content_hash, file_path)
                   VALUES ('p1', 'revise', 'T-1', 'Praetor', 't', 't', 'h', 'p')"""
            )

    def test_edge_src_requires_existing_node(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO edges (src, type, target) VALUES ('demo-n9', 'about', 'demo-n1')"
            )

    def test_fts5_match_works(self):
        insert_node(self.conn, "demo-n1", "n", "decision",
                    title="Adopt result-based error envelopes")
        self.conn.execute(
            "INSERT INTO nodes_fts (rowid, title, body) "
            "SELECT rowid, title, body FROM nodes"
        )
        rows = self.conn.execute(
            "SELECT n.id FROM nodes_fts f JOIN nodes n ON n.rowid = f.rowid "
            "WHERE nodes_fts MATCH 'envelopes'"
        ).fetchall()
        self.assertEqual(rows, [("demo-n1",)])

    def test_effective_status_is_derived(self):
        insert_node(self.conn, "demo-n1", "n", "decision")
        insert_node(self.conn, "demo-n2", "n", "decision")
        insert_node(self.conn, "demo-n3", "n", "decision", status="retired")
        self.conn.execute(
            "INSERT INTO edges (src, type, target) VALUES ('demo-n2', 'supersedes', 'demo-n1')"
        )
        self.conn.execute(
            "INSERT INTO edges (src, type, target) VALUES ('demo-n2', 'supersedes', 'demo-n3')"
        )
        status = dict(self.conn.execute("SELECT id, effective_status FROM v_effective_status"))
        self.assertEqual(status["demo-n1"], "superseded")  # derived, not stored
        self.assertEqual(status["demo-n2"], "active")
        self.assertEqual(status["demo-n3"], "retired")     # stored retired wins

    def test_flag_status_is_derived(self):
        insert_node(self.conn, "demo-n1", "n", "decision")
        insert_node(self.conn, "demo-f1", "f", "flag", origin="observed",
                    file_path="flags/demo-f1.md")
        insert_node(self.conn, "demo-f2", "f", "flag", origin="observed",
                    file_path="flags/demo-f2.md")
        self.conn.execute(
            "INSERT INTO edges (src, type, target) VALUES ('demo-n1', 'resolves', 'demo-f2')"
        )
        status = dict(self.conn.execute("SELECT id, flag_status FROM v_flag_status"))
        self.assertEqual(status, {"demo-f1": "open", "demo-f2": "resolved"})
        knowledge_ids = {r[0] for r in self.conn.execute("SELECT id FROM v_effective_status")}
        self.assertNotIn("demo-f1", knowledge_ids)  # planes stay separate


class Fts5ProbeTests(unittest.TestCase):
    def test_probe_passes_on_this_build(self):
        schema.check_fts5()  # must not raise here; init depends on it

    def test_probe_hard_fails_without_fts5(self):
        class FakeConn:
            def execute(self, sql):
                raise sqlite3.OperationalError("no such module: fts5")

            def close(self):
                pass

        with mock.patch.object(schema.sqlite3, "connect", return_value=FakeConn()):
            with self.assertRaisesRegex(SchemaError, "no FTS5 support"):
                schema.check_fts5()


if __name__ == "__main__":
    unittest.main()
