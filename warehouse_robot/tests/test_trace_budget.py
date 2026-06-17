"""Intent/verdict bracket, budget windows and the consent-gate (B3).

Owner-confirmed invariants proven here (B3 planning #2):
- an open round only ever blocks its own session;
- the agent can always close its own open round with a verdict — there is
  no deadlock state.

Also proven: the index stays logically untouched by query traffic — trace
and grants are operational tables outside the A8 logical digest, the trace
survives a reconcile rebuild verbatim, and grants deliberately do not.
"""

import json
import tempfile
import unittest

from warehouse_robot import fold, query, schema
from warehouse_robot.errors import BudgetExhausted, ProtocolError

from . import _fold_helpers as h
from . import _query_helpers as q


class BracketTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.wroot = q.build_instance(self._tmp.name)

    def test_open_round_blocks_the_next_round(self):
        q.q_open(self.wroot, session="b-1", scope="tooling")
        with self.assertRaisesRegex(ProtocolError, "still open"):
            q.q_open(self.wroot, session="b-1", scope="tooling")

    def test_open_round_blocks_only_its_own_session(self):
        q.q_open(self.wroot, session="b-1", scope="tooling")
        response = q.q_open(self.wroot, session="b-2", scope="tooling")
        self.assertEqual(response["count"], 1)  # other sessions unaffected

    def test_verdict_closes_and_the_session_continues(self):
        first = q.q_open(self.wroot, session="b-1", scope="tooling")
        closed = q.q_verdict(self.wroot, "WRONG-ENTRY", session="b-1")
        self.assertEqual(closed["round_id"], first["round_id"])
        self.assertEqual(closed["closed_verb"], "open_scope")
        self.assertFalse(closed["session_closed"])
        q.q_open(self.wroot, session="b-1", scope="ux-pattern")  # admitted

    def test_verdict_without_open_round_is_rejected(self):
        with self.assertRaisesRegex(ProtocolError, "no open round"):
            q.q_verdict(self.wroot, "FOUND-ENOUGH", session="b-9")

    def test_unknown_verdict_is_rejected(self):
        q.q_open(self.wroot, session="b-1", scope="tooling")
        with self.assertRaisesRegex(ProtocolError, "unknown verdict"):
            q.q_verdict(self.wroot, "DONE", session="b-1")

    def test_missing_intent_or_session_is_rejected(self):
        with self.assertRaises(ProtocolError):
            q.q_open(self.wroot, session="b-1", intent="   ", scope="tooling")
        with self.assertRaises(ProtocolError):
            q.q_open(self.wroot, session="", scope="tooling")

    def test_round_is_traced_with_intent_params_and_results(self):
        q.q_open(self.wroot, session="b-1", intent="map the tooling scope",
                 scope="tooling")
        row = h.query_one(
            self.wroot,
            "SELECT session_id, archetype, verb, intent, params, "
            "result_count, result_ids, verdict, budget FROM trace",
        )
        self.assertEqual(row[0], "b-1")
        self.assertEqual(row[1], "execute")
        self.assertEqual(row[2], "open_scope")
        self.assertEqual(row[3], "map the tooling scope")
        self.assertEqual(
            json.loads(row[4]),
            {"scope": "tooling", "kind": None, "include_inactive": False},
        )
        self.assertEqual(row[5], 1)
        self.assertEqual(json.loads(row[6]), ["demo-n9"])
        self.assertIsNone(row[7])  # open until the verdict lands
        self.assertEqual(
            json.loads(row[8]),
            {"wrong_entry": "0/3", "traverse": "0/3", "bodies": "0/10"},
        )
        q.q_verdict(self.wroot, "FOUND-ENOUGH", session="b-1")
        row = h.query_one(self.wroot, "SELECT verdict FROM trace")
        self.assertEqual(row[0], "FOUND-ENOUGH")

    def test_queries_refuse_an_uninitialised_or_unfolded_root(self):
        with self.assertRaises(Exception):
            q.q_open(self.wroot / "nowhere", session="b-1", scope="x")


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.wroot = q.build_instance(self._tmp.name)

    def exhaust_wrong_entry(self, session, pol):
        q.q_open(self.wroot, session=session, scope="tooling", policy=pol)
        q.q_verdict(self.wroot, "WRONG-ENTRY", session=session)

    def test_terminal_verdict_closes_the_session(self):
        q.q_open(self.wroot, session="bud-1", scope="tooling")
        q.q_verdict(self.wroot, "ABSENT", session="bud-1")
        with self.assertRaises(BudgetExhausted) as ctx:
            q.q_open(self.wroot, session="bud-1", scope="tooling")
        self.assertIn("terminal verdict ABSENT", str(ctx.exception))

    def test_wrong_entry_cap_refuses_with_escalation_packet(self):
        pol = q.make_policy(wrong_entry_cap=1)
        self.exhaust_wrong_entry("bud-2", pol)
        with self.assertRaises(BudgetExhausted) as ctx:
            q.q_open(self.wroot, session="bud-2", scope="ux-pattern", policy=pol)
        packet = ctx.exception.packet
        self.assertIn("WRONG-ENTRY retry cap", packet["reason"])
        self.assertEqual(packet["refused"]["verb"], "open_scope")
        self.assertEqual(len(packet["session_trace"]), 1)
        self.assertEqual(packet["window_usage"]["wrong_entry"], 1)

    def test_insufficient_traverse_cap(self):
        pol = q.make_policy(traverse_cap=1)
        q.q_traverse(self.wroot, "demo-n2", "supersedes", session="bud-3",
                     policy=pol)
        q.q_verdict(self.wroot, "INSUFFICIENT-TRAVERSE", session="bud-3")
        with self.assertRaisesRegex(BudgetExhausted, "depth cap"):
            q.q_traverse(self.wroot, "demo-n7", "derived-from",
                         session="bud-3", policy=pol)

    def test_body_fetch_ceiling_across_rounds(self):
        pol = q.make_policy(body_fetch_ceiling=2)
        q.q_fetch(self.wroot, ["demo-n1", "demo-n7"], session="bud-4", policy=pol)
        q.q_verdict(self.wroot, "WRONG-ENTRY", session="bud-4")
        with self.assertRaisesRegex(BudgetExhausted, "body-fetch ceiling"):
            q.q_fetch(self.wroot, ["demo-n3"], session="bud-4", policy=pol)

    def test_outright_oversized_fetch_is_a_protocol_error(self):
        # A grant could never admit it, so it must not consume one.
        pol = q.make_policy(body_fetch_ceiling=2)
        query.issue_grant(self.wroot, "bud-5")
        with self.assertRaisesRegex(ProtocolError, "outright"):
            q.q_fetch(self.wroot, ["demo-n1", "demo-n3", "demo-n7"],
                      session="bud-5", policy=pol)
        unconsumed = h.query_one(
            self.wroot,
            "SELECT count(*) FROM grants WHERE consumed_after_round IS NULL",
        )
        self.assertEqual(unconsumed[0], 1)

    def test_grant_opens_a_fresh_window_once(self):
        pol = q.make_policy(wrong_entry_cap=1)
        self.exhaust_wrong_entry("bud-6", pol)
        query.issue_grant(self.wroot, "bud-6")
        response = q.q_open(self.wroot, session="bud-6", scope="ux-pattern",
                            policy=pol)
        self.assertEqual(  # fresh window: counters restart
            json.loads(json.dumps(response["budget"]))["wrong_entry"], "0/1"
        )
        q.q_verdict(self.wroot, "WRONG-ENTRY", session="bud-6")
        with self.assertRaises(BudgetExhausted):  # one-shot: consumed
            q.q_open(self.wroot, session="bud-6", scope="tooling", policy=pol)

    def test_grant_reopens_a_terminally_closed_session(self):
        q.q_open(self.wroot, session="bud-7", scope="tooling")
        q.q_verdict(self.wroot, "FOUND-ENOUGH", session="bud-7")
        query.issue_grant(self.wroot, "bud-7")
        response = q.q_open(self.wroot, session="bud-7", scope="ux-pattern")
        self.assertEqual(response["count"], 2)

    def test_grant_for_another_session_does_not_help(self):
        q.q_open(self.wroot, session="bud-8", scope="tooling")
        q.q_verdict(self.wroot, "ABSENT", session="bud-8")
        query.issue_grant(self.wroot, "other-session")
        with self.assertRaises(BudgetExhausted):
            q.q_open(self.wroot, session="bud-8", scope="tooling")


class IndexDisciplineTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.wroot = q.build_instance(self._tmp.name)

    def run_some_traffic(self):
        q.q_open(self.wroot, session="d-1", scope="error-handling")
        q.q_verdict(self.wroot, "WRONG-ENTRY", session="d-1")
        q.q_find(self.wroot, "envelopes", session="d-1")
        q.q_verdict(self.wroot, "FOUND-ENOUGH", session="d-1")
        query.issue_grant(self.wroot, "d-1")

    def test_query_traffic_leaves_the_logical_digest_unchanged(self):
        before = fold.logical_digest_of(h.index_path(self.wroot))
        self.run_some_traffic()
        after = fold.logical_digest_of(h.index_path(self.wroot))
        self.assertEqual(after, before)

    def test_divergence_check_stays_clean_after_query_traffic(self):
        self.run_some_traffic()
        self.assertTrue(fold.check(self.wroot).clean)

    def test_rebuild_carries_the_trace_but_never_grants(self):
        self.run_some_traffic()
        before = h.query_all(
            self.wroot,
            "SELECT round_id, session_id, verb, verdict FROM trace "
            "ORDER BY round_id",
        )
        result = fold.rebuild(self.wroot)
        self.assertEqual(result.carried_trace, 2)
        after = h.query_all(
            self.wroot,
            "SELECT round_id, session_id, verb, verdict FROM trace "
            "ORDER BY round_id",
        )
        self.assertEqual(after, before)
        # Grants are fresh consent — deliberately not carried (owner decision).
        grants = h.query_one(self.wroot, "SELECT count(*) FROM grants")
        self.assertEqual(grants[0], 0)

    def test_closed_session_stays_closed_after_rebuild_without_its_grant(self):
        q.q_open(self.wroot, session="d-2", scope="tooling")
        q.q_verdict(self.wroot, "ABSENT", session="d-2")
        query.issue_grant(self.wroot, "d-2")
        fold.rebuild(self.wroot)
        with self.assertRaises(BudgetExhausted):
            q.q_open(self.wroot, session="d-2", scope="tooling")
