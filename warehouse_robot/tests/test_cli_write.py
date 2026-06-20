"""B4 — CLI write-path surface: JSON on stdout, exit codes, gitignore (A12)."""

import json
import tempfile
import unittest
from pathlib import Path

from ._fold_helpers import quiet_cli
from ._write_helpers import build_instance, make_proposal, proposal_text


def _decision(**kw):
    base = dict(kind="decision", scope="ledger", ticket="SAW-30", agent="Praetor")
    base.update(kw)
    return make_proposal(**base)


def _propose(w, a, text, ticket="SAW-30", agent="Praetor"):
    proposal = a.parent / "_proposal.md"
    proposal.write_text(text, encoding="utf-8")
    return quiet_cli(["propose", "--warehouse-root", str(w), "--antechamber-root",
                      str(a), "--ticket", ticket, "--agent", agent,
                      "--file", str(proposal)])


class CliWritePath(unittest.TestCase):
    def test_propose_resolve_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            code, out, err = _propose(w, a, _decision())
            self.assertEqual(code, 0, err)
            r = json.loads(out)
            self.assertEqual(r["state"], "pending-senate")
            key = r["proposal_key"]
            code, out, err = quiet_cli(["resolve", "--warehouse-root", str(w),
                                        "--antechamber-root", str(a),
                                        "--proposal-key", key, "--verdict", "ingested"])
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)["node_id"], "demo-n13")

    def test_rejected_malformed_exits_1(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            code, out, err = _propose(w, a, make_proposal(kind="decision",
                                                          ticket="SAW-30", agent="P"))
            self.assertEqual(code, 1)  # recorded rejection, not a robot fault
            self.assertEqual(json.loads(out)["state"], "rejected-malformed")

    def test_structural_garbage_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            code, out, err = _propose(w, a, proposal_text("malformed-has-id"))
            self.assertEqual(code, 2)
            self.assertIn("error:", err)

    def test_revise_limit_exits_1_with_packet(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            _, out, _ = _propose(w, a, _decision())
            key = json.loads(out)["proposal_key"]
            base = ["resolve", "--warehouse-root", str(w), "--antechamber-root",
                    str(a), "--proposal-key", key, "--verdict", "revise"]
            # default limit is 3; exhaust by revising up to the bound
            quiet_cli(base)  # round 1 -> proposed
            self._revise(w, a, key)  # round 2
            quiet_cli(base)  # round 2 -> proposed
            self._revise(w, a, key)  # round 3
            code, out, err = quiet_cli(base)  # round 3 == limit -> escalate
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(out)["error"], "revise-limit-reached")

    def _revise(self, w, a, key):
        proposal = a.parent / "_revised.md"
        proposal.write_text(_decision(title="Revised again"), encoding="utf-8")
        return quiet_cli(["revise", "--warehouse-root", str(w), "--antechamber-root",
                          str(a), "--proposal-key", key, "--file", str(proposal)])

    def test_check_reports_antechamber(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            _propose(w, a, _decision())
            code, out, err = quiet_cli(["check", "--warehouse-root", str(w),
                                        "--antechamber-root", str(a)])
            self.assertEqual(code, 0, err)
            self.assertIn("antechamber: clean", out)

    def test_reconcile_antechamber_command(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            _propose(w, a, _decision())
            code, out, err = quiet_cli(["reconcile-antechamber",
                                        "--warehouse-root", str(w),
                                        "--antechamber-root", str(a)])
            self.assertEqual(code, 0, err)
            self.assertIn("1 proposal", out)

    def test_disposable_gitignore_covers_node_and_antechamber_markdown(self):
        # A12 ↔ A13: the broad ignore is for THROWAWAY instances only.
        with tempfile.TemporaryDirectory() as d:
            w = Path(d) / "pm" / "warehouse"
            code, _, err = quiet_cli(["init", "--warehouse-root", str(w),
                                      "--prefix", "demo", "--disposable"])
            self.assertEqual(code, 0, err)
            wig = (w / ".gitignore").read_text()
            self.assertIn("nodes/", wig)
            self.assertIn("flags/", wig)
            self.assertTrue((w.parent / "antechamber" / ".gitignore").exists())

    def test_canonical_init_versions_markdown(self):
        # A13: a real instance gitignores ONLY the derived index.
        with tempfile.TemporaryDirectory() as d:
            w = Path(d) / "pm" / "warehouse"
            quiet_cli(["init", "--warehouse-root", str(w), "--prefix", "demo"])
            wig = (w / ".gitignore").read_text()
            self.assertIn("index.sqlite", wig)
            self.assertNotIn("nodes/", wig)
            self.assertFalse((w.parent / "antechamber" / ".gitignore").exists())


if __name__ == "__main__":
    unittest.main()
