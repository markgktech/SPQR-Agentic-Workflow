"""open_scope (B3): the deterministic scope-bounded feed.

S4 Cluster 3: the agent sees the COMPLETE slice — overflow facets, never a
ranking cutoff. An empty slice is legitimate ABSENT evidence and is never
auto-broadened (owner decision, B3 planning #7).
"""

import tempfile
import unittest

from warehouse_robot.errors import PolicyDenied, ProtocolError

from . import _query_helpers as q


class OpenScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.wroot = q.build_instance(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def call(self, session, **kw):
        response = q.q_open(self.wroot, session=session, **kw)
        q.q_verdict(self.wroot, "FOUND-ENOUGH", session=session)
        return response

    def test_scope_slice_is_complete_and_id_ordered(self):
        response = self.call("os-1", scope="ux-pattern")
        self.assertEqual(q.candidate_ids(response), ["demo-n3", "demo-n8"])
        self.assertEqual(response["count"], 2)
        skeleton = response["candidates"][0]
        # Skeleton shape (S4): id + title + kind + scope + status, NO body.
        self.assertEqual(
            set(skeleton), {"id", "title", "kind", "scope", "status"}
        )

    def test_scope_and_kind_intersect(self):
        response = self.call("os-2", scope="ux-pattern", kind="decision")
        self.assertEqual(q.candidate_ids(response), ["demo-n8"])

    def test_kind_only_slice_reaches_unscoped_nodes(self):
        # The three fixture lessons carry no scope; kind-only addressing is
        # the only deterministic way to them.
        response = self.call("os-3", kind="lesson")
        self.assertEqual(
            q.candidate_ids(response), ["demo-n5", "demo-n6", "demo-n10"]
        )

    def test_superseded_is_excluded_by_default(self):
        response = self.call("os-4", scope="error-handling")
        self.assertEqual(q.candidate_ids(response), ["demo-n7"])

    def test_include_inactive_shows_the_superseded_node(self):
        response = self.call(
            "os-5", scope="error-handling", include_inactive=True
        )
        self.assertEqual(q.candidate_ids(response), ["demo-n2", "demo-n7"])
        statuses = {c["id"]: c["status"] for c in response["candidates"]}
        self.assertEqual(statuses["demo-n2"], "superseded")
        self.assertEqual(statuses["demo-n7"], "active")

    def test_kind_flag_opens_the_audit_plane(self):
        response = self.call("os-6", kind="flag")
        self.assertEqual(q.candidate_ids(response), ["demo-f1"])  # f2 resolved
        response = self.call("os-7", kind="flag", include_inactive=True)
        self.assertEqual(q.candidate_ids(response), ["demo-f1", "demo-f2"])

    def test_scrutinize_may_not_include_inactive(self):
        with self.assertRaisesRegex(PolicyDenied, "lineage"):
            q.q_open(self.wroot, session="os-8", archetype="scrutinize",
                     scope="error-handling", include_inactive=True)

    def test_facet_view_when_neither_scope_nor_kind(self):
        response = self.call("os-9")
        self.assertEqual(response["view"], "scope-facets")
        facets = {f["scope"]: f["count"] for f in response["facets"]}
        self.assertEqual(
            facets,
            {
                "architecture": 1, "concurrency": 1, "data-layer": 2,
                "error-handling": 1, "tooling": 1, "ux-pattern": 2,
                None: 3,  # the unscoped lessons stay visible as a bucket
            },
        )
        # Deterministic order: scopes ascending, the null bucket last.
        self.assertIsNone(response["facets"][-1]["scope"])

    def test_facet_view_include_inactive_counts_the_superseded(self):
        response = self.call("os-10", include_inactive=True)
        facets = {f["scope"]: f["count"] for f in response["facets"]}
        self.assertEqual(facets["error-handling"], 2)

    def test_empty_slice_is_never_broadened(self):
        response = self.call("os-11", scope="architecture", kind="lesson")
        self.assertEqual(response["candidates"], [])
        self.assertEqual(response["count"], 0)
        self.assertNotIn("auto_broadened", response)

    def test_unknown_kind_is_rejected(self):
        with self.assertRaisesRegex(ProtocolError, "unknown kind"):
            q.q_open(self.wroot, session="os-12", kind="adr")

    def test_overflow_facets_by_kind_instead_of_truncating(self):
        pol = q.make_policy(altitude_ceiling=1)
        response = q.q_open(self.wroot, session="os-13", scope="ux-pattern",
                            policy=pol)
        q.q_verdict(self.wroot, "WRONG-ENTRY", session="os-13")
        self.assertTrue(response["overflow"])
        self.assertEqual(response["count"], 2)
        self.assertEqual(response["ceiling"], 1)
        self.assertEqual(
            response["facets"],
            [{"kind": "constraint", "count": 1}, {"kind": "decision", "count": 1}],
        )
        self.assertNotIn("candidates", response)

    def test_overflow_with_kind_filter_cannot_facet_further(self):
        pol = q.make_policy(altitude_ceiling=2)
        response = q.q_open(self.wroot, session="os-14", kind="decision",
                            policy=pol)
        q.q_verdict(self.wroot, "WRONG-ENTRY", session="os-14")
        self.assertTrue(response["overflow"])
        self.assertEqual(response["count"], 5)  # active decisions
        self.assertIsNone(response["facets"])
        self.assertIn("find", response["guidance"])
