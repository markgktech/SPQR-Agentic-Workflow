"""find (B3): the FTS5/BM25 finder side-door (rank-bounded top-N).

Auto-broaden is strictly one deterministic step: only here, only by dropping
the scope filter; a kind filter is never dropped by the robot (owner
decision, B3 planning #7).
"""

import tempfile
import unittest

from warehouse_robot.errors import ProtocolError

from . import _query_helpers as q


class FindTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.wroot = q.build_instance(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def call(self, session, text, **kw):
        response = q.q_find(self.wroot, text, session=session, **kw)
        q.q_verdict(self.wroot, "FOUND-ENOUGH", session=session)
        return response

    def test_match_excludes_inactive_by_default(self):
        # "envelopes" appears in the titles of demo-n2 (superseded) and
        # demo-n7 (active); only the active one may surface.
        response = self.call("f-1", "envelopes")
        self.assertEqual(q.candidate_ids(response), ["demo-n7"])
        self.assertFalse(response["auto_broadened"])

    def test_include_inactive_surfaces_the_superseded(self):
        response = self.call("f-2", "envelopes", include_inactive=True)
        self.assertEqual(
            set(q.candidate_ids(response)), {"demo-n2", "demo-n7"}
        )

    def test_kind_filter_applies(self):
        response = self.call("f-3", "envelopes", kind="lesson",
                             include_inactive=True)
        for candidate in response["candidates"]:
            self.assertEqual(candidate["kind"], "lesson")

    def test_flag_plane_only_via_explicit_kind(self):
        knowledge = self.call("f-4", "orphan watch")
        self.assertNotIn("demo-f1", q.candidate_ids(knowledge))
        audit = self.call("f-5", "orphan watch", kind="flag")
        self.assertEqual(q.candidate_ids(audit), ["demo-f1"])

    def test_auto_broaden_drops_scope_only_and_once(self):
        # Zero hits inside scope=tooling -> the robot drops scope (one step).
        response = self.call("f-6", "envelopes", scope="tooling")
        self.assertTrue(response["auto_broadened"])
        self.assertEqual(response["dropped_filter"], "scope")
        self.assertEqual(q.candidate_ids(response), ["demo-n7"])

    def test_auto_broaden_never_drops_kind(self):
        # After the scope drop the kind filter still excludes everything;
        # the robot stops — a second step would be agent judgment.
        response = self.call("f-7", "envelopes", scope="tooling", kind="lesson")
        self.assertTrue(response["auto_broadened"])
        self.assertEqual(response["candidates"], [])

    def test_no_broaden_when_scope_was_not_given(self):
        response = self.call("f-8", "nonexistent-term-xyz")
        self.assertEqual(response["candidates"], [])
        self.assertFalse(response["auto_broadened"])

    def test_top_n_bounds_the_ranked_list(self):
        wide = self.call("f-9", "the local data error")
        self.assertGreater(wide["count"], 2)
        narrow = self.call("f-10", "the local data error", top_n=2)
        self.assertEqual(narrow["count"], 2)
        # The narrow list is a prefix of the wide one (same deterministic rank).
        self.assertEqual(
            q.candidate_ids(narrow), q.candidate_ids(wide)[:2]
        )

    def test_top_n_validation(self):
        for bad in (0, -1, True, "5"):
            with self.assertRaises(ProtocolError):
                q.q_find(self.wroot, "x", session="f-11", top_n=bad)
        pol = q.make_policy(altitude_ceiling=5)
        with self.assertRaisesRegex(ProtocolError, "altitude ceiling"):
            q.q_find(self.wroot, "x", session="f-12", top_n=6, policy=pol)

    def test_unsearchable_text_is_rejected(self):
        for junk in ("", "###", "   "):
            with self.assertRaisesRegex(ProtocolError, "searchable|string"):
                q.q_find(self.wroot, junk, session="f-13")

    def test_fts_syntax_is_disarmed(self):
        # Raw FTS5 operators must not reach the engine as syntax.
        response = self.call("f-14", 'envelopes" OR x NEAR/2 (')
        self.assertIn("demo-n7", q.candidate_ids(response))
