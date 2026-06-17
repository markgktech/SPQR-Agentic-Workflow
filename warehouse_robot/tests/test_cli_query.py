"""CLI surface of the B3 query interface.

End-to-end against disposable instances built through the CLI itself:
init -> fixtures -> reconcile -> query verbs. JSON on stdout; exit codes
0 success / 1 budget-exhausted (escalation packet) / 2 error; check-on-open
warns on stderr and never refuses.
"""

import json
import tempfile
import unittest

from warehouse_robot import store

from . import _fold_helpers as h


def build_cli_instance(parent):
    wroot = h.init_instance(parent)
    h.copy_fixtures(wroot)
    code, _, err = h.quiet_cli(["reconcile", "--warehouse-root", str(wroot)])
    assert code == 0, err
    return wroot


def base_args(verb, wroot, session, archetype="execute", intent="cli test"):
    return [
        verb, "--warehouse-root", str(wroot), "--archetype", archetype,
        "--session", session, "--intent", intent,
    ]


class CliQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.wroot = build_cli_instance(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def run_ok(self, argv, expect_code=0):
        code, out, err = h.quiet_cli(argv)
        self.assertEqual(code, expect_code, err or out)
        return json.loads(out), err

    def close(self, session, value="FOUND-ENOUGH"):
        return self.run_ok([
            "verdict", "--warehouse-root", str(self.wroot),
            "--session", session, "--verdict", value,
        ])

    def test_open_scope_round_trip(self):
        response, err = self.run_ok(
            base_args("open-scope", self.wroot, "cli-1")
            + ["--scope", "ux-pattern"]
        )
        self.assertEqual(
            [c["id"] for c in response["candidates"]], ["demo-n3", "demo-n8"]
        )
        self.assertEqual(err, "")  # clean index: no divergence warning
        closed, _ = self.close("cli-1")
        self.assertEqual(closed["verdict"], "FOUND-ENOUGH")
        self.assertTrue(closed["session_closed"])

    def test_find_fetch_traverse_round_trip(self):
        response, _ = self.run_ok(
            base_args("find", self.wroot, "cli-2")
            + ["--text", "envelopes", "--top-n", "3"]
        )
        self.assertEqual([c["id"] for c in response["candidates"]], ["demo-n7"])
        self.close("cli-2", "WRONG-ENTRY")

        response, _ = self.run_ok(
            base_args("fetch", self.wroot, "cli-2") + ["--ids", "demo-n7"]
        )
        self.assertIn("Result-based envelopes", response["nodes"][0]["body"])
        self.close("cli-2", "INSUFFICIENT-TRAVERSE")

        response, _ = self.run_ok(
            base_args("traverse", self.wroot, "cli-2")
            + ["--id", "demo-n7", "--edge-type", "supersedes"]
        )
        self.assertEqual([n["id"] for n in response["nodes"]], ["demo-n2"])
        self.close("cli-2")

    def test_budget_exhaustion_exits_1_with_packet_and_grant_reopens(self):
        session = "cli-3"
        self.run_ok(base_args("open-scope", self.wroot, session)
                    + ["--scope", "tooling"])
        self.close(session, "ABSENT")

        code, out, _ = h.quiet_cli(
            base_args("open-scope", self.wroot, session) + ["--scope", "tooling"]
        )
        self.assertEqual(code, 1)
        refusal = json.loads(out)
        self.assertEqual(refusal["error"], "budget-exhausted")
        self.assertIn("terminal verdict", refusal["message"])
        self.assertEqual(len(refusal["packet"]["session_trace"]), 1)

        granted, _ = self.run_ok([
            "grant", "--warehouse-root", str(self.wroot), "--session", session,
        ])
        self.assertEqual(granted["session_id"], session)
        response, _ = self.run_ok(
            base_args("open-scope", self.wroot, session) + ["--scope", "tooling"]
        )
        self.assertEqual(response["count"], 1)
        self.close(session)

    def test_bracket_violation_exits_2(self):
        session = "cli-4"
        self.run_ok(base_args("open-scope", self.wroot, session)
                    + ["--scope", "tooling"])
        code, _, err = h.quiet_cli(
            base_args("open-scope", self.wroot, session) + ["--scope", "tooling"]
        )
        self.assertEqual(code, 2)
        self.assertIn("still open", err)
        self.close(session)

    def test_scrutinize_deny_exits_2(self):
        code, _, err = h.quiet_cli(
            base_args("traverse", self.wroot, "cli-5", archetype="scrutinize")
            + ["--id", "demo-n7", "--edge-type", "derived-from"]
        )
        self.assertEqual(code, 2)
        self.assertIn("SCRUTINIZE DENY", err)

    def test_tighten_only_tightens(self):
        code, _, err = h.quiet_cli(
            base_args("open-scope", self.wroot, "cli-6")
            + ["--scope", "ux-pattern", "--tighten", "altitude_ceiling=99"]
        )
        self.assertEqual(code, 2)
        self.assertIn("continuation grant", err)

        response, _ = self.run_ok(
            base_args("open-scope", self.wroot, "cli-6")
            + ["--scope", "ux-pattern", "--tighten", "altitude_ceiling=1"]
        )
        self.assertTrue(response["overflow"])
        self.close("cli-6", "WRONG-ENTRY")

        code, _, err = h.quiet_cli(
            base_args("open-scope", self.wroot, "cli-6")
            + ["--scope", "x", "--tighten", "altitude_ceiling=abc"]
        )
        self.assertEqual(code, 2)
        self.assertIn("DIAL=INTEGER", err)


class CliDivergenceWarningTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.wroot = build_cli_instance(self._tmp.name)

    def test_stale_index_warns_on_stderr_but_serves(self):
        node = store.Node(
            id="demo-n13", kind="decision", status="active",
            title="Hand-placed node the index has not folded yet",
            origin="decided", timestamp="2026-06-09T09:00:00Z",
            schema_version=1, scope="tooling",
            body="Divergence fixture: file exists, index row does not.\n",
        )
        store.write_node_file(self.wroot, node)

        code, out, err = h.quiet_cli(base_args("open-scope", self.wroot, "cli-7")
                                     + ["--scope", "tooling"])
        self.assertEqual(code, 0)  # degraded, not refused (B2 #1)
        self.assertIn("diverges from markdown", err)
        response = json.loads(out)
        # Served from the stale index: the unfolded node is not visible.
        self.assertEqual([c["id"] for c in response["candidates"]], ["demo-n9"])
