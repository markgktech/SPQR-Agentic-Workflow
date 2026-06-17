"""Reconcile rebuild, A8 exit criterion and the divergence check (B2).

A8 two-part criterion proven here:
1. Rebuild determinism — two rebuilds from the same markdown tree (and the
   same carried-over state) produce byte-identical index files.
2. Live-vs-rebuild equivalence — the incrementally built index and a fresh
   rebuild agree on the canonical logical digest.

All instances are disposable under the system tmp directory (A4).
"""

import tempfile
import unittest
from pathlib import Path

from warehouse_robot import fold, schema, store
from warehouse_robot.errors import FoldError
from warehouse_robot.ids import KNOWLEDGE_PLANE

from . import _fold_helpers as h

SAMPLE_TRACE = (
    1, "2026-06-13T10:00:00Z", "sess-demo-1", "DEMO-9", "Praetor", "builder",
    "find", "looking for error-handling decisions", '{"top_n": 5}', 2,
    "demo-n2,demo-n7", "FOUND-ENOUGH", '{"rounds": 1}',
)

SAMPLE_ANTECHAMBER = (
    "prop-1", "proposed", "DEMO-9", "Praetor", "2026-06-13T10:05:00Z",
    "2026-06-13T10:05:00Z", "deadbeef", "antechamber/prop-1.md", None,
)


def insert_operational_rows(wroot):
    conn = schema.connect(h.index_path(wroot))
    try:
        with conn:
            conn.execute(
                "INSERT INTO trace (round_id, ts, session_id, ticket, agent, "
                "archetype, verb, intent, params, result_count, result_ids, "
                "verdict, budget) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                SAMPLE_TRACE,
            )
            conn.execute(
                "INSERT INTO antechamber (proposal_key, state, ticket, agent, "
                "created_at, updated_at, content_hash, file_path, node_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                SAMPLE_ANTECHAMBER,
            )
    finally:
        conn.close()


class RebuildTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.wroot = h.init_instance(self._tmp.name)

    def test_rebuild_determinism_is_byte_identical(self):
        # A8 part 1 — the hard byte criterion. Looped: WAL checkpoint
        # bookkeeping once made this flake at ~10% per double rebuild, so a
        # single comparison could ship the bug green again.
        h.fold_fixtures(self.wroot)
        first = fold.rebuild(self.wroot)
        hash_one = h.file_sha256(h.index_path(self.wroot))
        for iteration in range(5):
            result = fold.rebuild(self.wroot)
            self.assertEqual(
                h.file_sha256(h.index_path(self.wroot)), hash_one,
                f"rebuild #{iteration + 2} is not byte-identical to rebuild #1",
            )
            self.assertEqual(result.digest, first.digest)

    def test_live_and_rebuilt_index_agree_on_logical_digest(self):
        # A8 part 2 — live (arrival-order inserts) vs rebuild (plane+number order).
        h.fold_fixtures(self.wroot)
        live_digest = fold.logical_digest_of(h.index_path(self.wroot))
        result = fold.rebuild(self.wroot)
        self.assertEqual(result.digest, live_digest)
        self.assertEqual(fold.logical_digest_of(h.index_path(self.wroot)), live_digest)

    def test_rebuild_reproduces_counts_and_rederives_counter(self):
        h.fold_fixtures(self.wroot)
        h.execute(self.wroot, "UPDATE id_counter SET next_value = 1 WHERE plane = 'n'")
        result = fold.rebuild(self.wroot)
        self.assertEqual(result.node_count, 14)
        next_n = h.query_one(
            self.wroot, "SELECT next_value FROM id_counter WHERE plane = ?", (KNOWLEDGE_PLANE,)
        )[0]
        self.assertEqual(next_n, 13)  # markdown max (demo-n12) + 1, S7 rule

    def test_rebuild_carries_created_at(self):
        h.fold_fixtures(self.wroot)
        before = h.query_one(self.wroot, "SELECT value FROM meta WHERE key = 'created_at'")[0]
        fold.rebuild(self.wroot)
        after = h.query_one(self.wroot, "SELECT value FROM meta WHERE key = 'created_at'")[0]
        self.assertEqual(after, before)

    def test_rebuild_carries_trace_and_antechamber_verbatim(self):
        h.fold_fixtures(self.wroot)
        insert_operational_rows(self.wroot)
        result = fold.rebuild(self.wroot)
        self.assertEqual(result.carried_trace, 1)
        self.assertEqual(result.carried_antechamber, 1)
        trace = h.query_one(
            self.wroot,
            "SELECT round_id, ts, session_id, ticket, agent, archetype, verb, "
            "intent, params, result_count, result_ids, verdict, budget FROM trace",
        )
        self.assertEqual(trace, SAMPLE_TRACE)
        ante = h.query_one(
            self.wroot,
            "SELECT proposal_key, state, ticket, agent, created_at, updated_at, "
            "content_hash, file_path, node_id FROM antechamber",
        )
        self.assertEqual(ante, SAMPLE_ANTECHAMBER)
        # Determinism holds with carried rows too (A8 part 1) — looped, same
        # flake-hardening rationale as the determinism test above.
        hash_one = h.file_sha256(h.index_path(self.wroot))
        for iteration in range(5):
            fold.rebuild(self.wroot)
            self.assertEqual(
                h.file_sha256(h.index_path(self.wroot)), hash_one,
                f"carried-rows rebuild #{iteration + 2} is not byte-identical",
            )

    def test_fresh_rebuild_discards_operational_state(self):
        h.fold_fixtures(self.wroot)
        insert_operational_rows(self.wroot)
        result = fold.rebuild(self.wroot, fresh=True)
        self.assertEqual(result.carried_trace, 0)
        self.assertEqual(h.query_one(self.wroot, "SELECT count(*) FROM trace")[0], 0)
        self.assertEqual(h.query_one(self.wroot, "SELECT count(*) FROM antechamber")[0], 0)

    def test_rebuild_recovers_when_index_is_deleted(self):
        h.fold_fixtures(self.wroot)
        h.index_path(self.wroot).unlink()
        result = fold.rebuild(self.wroot)
        self.assertEqual(result.node_count, 14)
        self.assertTrue(fold.check(self.wroot).clean)
        # Nothing to carry: meta.created_at is freshly minted, trace is empty.
        self.assertEqual(result.carried_trace, 0)
        self.assertEqual(h.query_one(self.wroot, "SELECT count(*) FROM trace")[0], 0)

    def test_corrupt_index_demands_fresh(self):
        h.fold_fixtures(self.wroot)
        h.index_path(self.wroot).write_bytes(b"this is not a sqlite file at all")
        with self.assertRaisesRegex(FoldError, "fresh"):
            fold.rebuild(self.wroot)
        result = fold.rebuild(self.wroot, fresh=True)
        self.assertEqual(result.node_count, 14)
        self.assertTrue(fold.check(self.wroot).clean)

    def test_crashed_rebuild_leftover_is_cleaned_up(self):
        h.fold_fixtures(self.wroot)
        leftover = Path(str(h.index_path(self.wroot)) + fold.REBUILD_SUFFIX)
        leftover.write_bytes(b"crashed rebuild leftover")
        fold.rebuild(self.wroot)
        self.assertFalse(leftover.exists())
        self.assertTrue(fold.check(self.wroot).clean)


class DivergenceCheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.wroot = h.init_instance(self._tmp.name)
        h.fold_fixtures(self.wroot)

    def test_clean_instance_reports_clean(self):
        report = fold.check(self.wroot)
        self.assertTrue(report.clean)
        self.assertEqual(report.lines(), ["clean: markdown and index agree"])

    def test_index_missing(self):
        h.index_path(self.wroot).unlink()
        report = fold.check(self.wroot)
        self.assertTrue(report.index_missing)
        self.assertFalse(report.clean)

    def test_file_without_index_row_is_missing_in_index(self):
        # The crash window: markdown written first (truth), index upsert lost.
        node = store.Node(
            id="demo-n13", kind="decision", status="active",
            title="Crash-window node", scope="error-handling", origin="decided",
            timestamp="2026-06-13T11:00:00Z", schema_version=1,
            body="Written to markdown; the index upsert never ran.\n",
        )
        store.write_node_file(self.wroot, node)
        report = fold.check(self.wroot)
        self.assertEqual(report.missing_in_index, ["demo-n13"])
        # Reconcile heals it.
        fold.rebuild(self.wroot)
        self.assertTrue(fold.check(self.wroot).clean)

    def test_deleted_file_is_missing_in_markdown(self):
        (self.wroot / "nodes" / "demo-n12.md").unlink()
        report = fold.check(self.wroot)
        self.assertEqual(report.missing_in_markdown, ["demo-n12"])
        fold.rebuild(self.wroot)
        self.assertTrue(fold.check(self.wroot).clean)

    def test_hand_edited_file_is_hash_mismatch(self):
        path = self.wroot / "nodes" / "demo-n12.md"
        node = store.read_node_file(path)
        node.body = "Hand-edited after the fold — an append-only violation.\n"
        path.write_text(store.serialize_node(node), encoding="utf-8")
        report = fold.check(self.wroot)
        self.assertEqual(report.hash_mismatch, ["demo-n12"])

    def test_misplaced_file_is_reported(self):
        src = self.wroot / "nodes" / "demo-n3.md"
        (self.wroot / "flags" / "demo-n3.md").write_text(
            src.read_text(encoding="utf-8"), encoding="utf-8"
        )
        report = fold.check(self.wroot)
        self.assertEqual(report.misplaced, [("demo-n3", "flags/demo-n3.md")])

    def test_unreadable_file_is_reported_not_fatal(self):
        (self.wroot / "nodes" / "demo-n99.md").write_text("not a node\n", encoding="utf-8")
        report = fold.check(self.wroot)
        self.assertEqual(len(report.unreadable), 1)
        self.assertEqual(report.unreadable[0][0], "nodes/demo-n99.md")
        self.assertFalse(report.clean)

    def test_counter_behind_is_reported(self):
        h.execute(self.wroot, "UPDATE id_counter SET next_value = 1 WHERE plane = 'n'")
        report = fold.check(self.wroot)
        self.assertEqual(report.counter_behind, [("n", 1, 12)])


class FoldCliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.wroot = h.init_instance(self._tmp.name)
        h.fold_fixtures(self.wroot)

    def test_check_exits_zero_when_clean(self):
        code, out, _ = h.quiet_cli(["check", "--warehouse-root", str(self.wroot)])
        self.assertEqual(code, 0)
        self.assertIn("clean", out)

    def test_check_exits_one_when_divergent(self):
        (self.wroot / "nodes" / "demo-n12.md").unlink()
        code, out, _ = h.quiet_cli(["check", "--warehouse-root", str(self.wroot)])
        self.assertEqual(code, 1)
        self.assertIn("missing in markdown: demo-n12", out)

    def test_reconcile_reports_digest_and_heals(self):
        (self.wroot / "nodes" / "demo-n12.md").unlink()
        code, out, _ = h.quiet_cli(["reconcile", "--warehouse-root", str(self.wroot)])
        self.assertEqual(code, 0)
        self.assertIn("logical digest", out)
        self.assertIn("nodes folded        : 13", out)
        self.assertEqual(h.quiet_cli(["check", "--warehouse-root", str(self.wroot)])[0], 0)

    def test_reconcile_fresh_flag(self):
        insert_operational_rows(self.wroot)
        code, out, _ = h.quiet_cli(["reconcile", "--warehouse-root", str(self.wroot), "--fresh"])
        self.assertEqual(code, 0)
        self.assertIn("trace rows carried  : 0", out)

    def test_uninitialised_root_is_a_clean_error(self):
        bogus = Path(self._tmp.name) / "nowhere"
        code, _, err = h.quiet_cli(["check", "--warehouse-root", str(bogus)])
        self.assertEqual(code, 2)
        self.assertIn("not an initialised warehouse root", err)


if __name__ == "__main__":
    unittest.main()
