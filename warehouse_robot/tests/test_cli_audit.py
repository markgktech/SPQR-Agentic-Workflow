"""B5 — the `audit` CLI surface (JSON contract + exit codes).

The consumer is an LLM agent: JSON on stdout, deterministic shape. Exit codes
mirror `check` — 0 clean, 1 findings (open flags exist), 2 error — so the
audit is usable as a CI/retro gate. Tested in-process (quiet_cli) and as a real
subprocess against disposable system-tmp instances (A4/A12).
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from warehouse_robot import schema

from ._audit_helpers import build_broken_instance, build_clean_instance
from ._fold_helpers import init_instance, quiet_cli

REPO_ROOT = Path(__file__).resolve().parents[2]


class CliAudit(unittest.TestCase):
    def test_clean_graph_exit_zero_empty_json(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            code, out, err = quiet_cli(["audit", "--warehouse-root", str(w)])
            self.assertEqual(code, 0, err)
            payload = json.loads(out)
            self.assertEqual(payload["verb"], "audit")
            self.assertEqual(payload["emitted"], [])
            self.assertEqual(payload["open_flag_count"], 0)

    def test_findings_exit_one_with_structured_flags(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_broken_instance(d)
            code, out, err = quiet_cli(["audit", "--warehouse-root", str(w)])
            self.assertEqual(code, 1, err)  # open flags exist → findings present
            payload = json.loads(out)
            self.assertEqual(len(payload["emitted"]), 3)
            self.assertEqual(payload["open_flag_count"], 3)
            self.assertEqual({(e["target"], e["flag_type"]) for e in payload["emitted"]},
                             {("demo-n4", "orphan"),
                              ("demo-n5", "missing-recommended-edge"),
                              ("demo-n6", "relates-to-overuse")})

    def test_rerun_is_idempotent_still_exit_one(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_broken_instance(d)
            quiet_cli(["audit", "--warehouse-root", str(w)])
            code, out, _ = quiet_cli(["audit", "--warehouse-root", str(w)])
            self.assertEqual(code, 1)  # the standing flags keep it at 1
            payload = json.loads(out)
            self.assertEqual(payload["emitted"], [])  # no duplicates
            self.assertEqual(len(payload["skipped_existing"]), 3)

    def test_missing_index_exit_two(self):
        with tempfile.TemporaryDirectory() as d:
            w = init_instance(d)
            (w / schema.INDEX_FILENAME).unlink()
            code, _, err = quiet_cli(["audit", "--warehouse-root", str(w)])
            self.assertEqual(code, 2)
            self.assertIn("reconcile", err)

    def test_audit_as_a_real_subprocess(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_broken_instance(d)
            p = subprocess.run(
                [sys.executable, "-m", "warehouse_robot", "audit",
                 "--warehouse-root", str(w)],
                cwd=str(REPO_ROOT), capture_output=True, text=True,
            )
            self.assertEqual(p.returncode, 1, p.stderr)
            payload = json.loads(p.stdout)
            self.assertEqual(len(payload["emitted"]), 3)


if __name__ == "__main__":
    unittest.main()
