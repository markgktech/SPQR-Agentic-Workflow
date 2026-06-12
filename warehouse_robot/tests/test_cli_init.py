import contextlib
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from warehouse_robot import cli
from warehouse_robot.errors import SchemaError


def run_cli(argv):
    """Run the CLI quietly; return (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


class InitCliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.parent = Path(self._tmp.name) / "project_memory"
        self.wroot = self.parent / "warehouse"

    def test_init_creates_full_layout(self):
        code, out, _ = run_cli(["init", "--warehouse-root", str(self.wroot), "--prefix", "demo"])
        self.assertEqual(code, 0)
        self.assertIn("initialised warehouse instance", out)
        self.assertTrue((self.wroot / "nodes").is_dir())
        self.assertTrue((self.wroot / "flags").is_dir())
        self.assertTrue((self.parent / "antechamber").is_dir())  # sibling default (A3)
        self.assertTrue((self.wroot / "index.sqlite").is_file())
        gitignore = (self.wroot / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("index.sqlite", gitignore)
        manifest = json.loads((self.wroot / "warehouse.config.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest,
            {"project_prefix": "demo", "schema_version": 1, "scope_vocabulary": []},
        )

    def test_warehouse_root_is_mandatory(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                cli.main(["init", "--prefix", "demo"])
        self.assertNotEqual(ctx.exception.code, 0)

    def test_init_refuses_initialised_root(self):
        self.assertEqual(run_cli(["init", "--warehouse-root", str(self.wroot), "--prefix", "demo"])[0], 0)
        code, _, err = run_cli(["init", "--warehouse-root", str(self.wroot), "--prefix", "demo"])
        self.assertEqual(code, 2)
        self.assertIn("already initialised", err)

    def test_invalid_prefix_creates_nothing(self):
        code, _, err = run_cli(["init", "--warehouse-root", str(self.wroot), "--prefix", "BAD"])
        self.assertEqual(code, 2)
        self.assertIn("invalid project prefix", err)
        self.assertFalse(self.wroot.exists())

    def test_antechamber_override(self):
        ante = Path(self._tmp.name) / "elsewhere" / "ante"
        code, _, _ = run_cli([
            "init", "--warehouse-root", str(self.wroot), "--prefix", "demo",
            "--antechamber-root", str(ante),
        ])
        self.assertEqual(code, 0)
        self.assertTrue(ante.is_dir())
        self.assertFalse((self.parent / "antechamber").exists())

    def test_missing_fts5_hard_fails_and_creates_nothing(self):
        # Owner condition on B1 #1: init verifies FTS5 at runtime and hard-fails.
        with mock.patch.object(cli.schema, "check_fts5", side_effect=SchemaError("no FTS5 support")):
            code, _, err = run_cli(["init", "--warehouse-root", str(self.wroot), "--prefix", "demo"])
        self.assertEqual(code, 2)
        self.assertIn("no FTS5 support", err)
        self.assertFalse(self.wroot.exists())

    def test_two_roots_are_isolated(self):
        root_a = Path(self._tmp.name) / "a" / "warehouse"
        root_b = Path(self._tmp.name) / "b" / "warehouse"
        self.assertEqual(run_cli(["init", "--warehouse-root", str(root_a), "--prefix", "aaa"])[0], 0)
        self.assertEqual(run_cli(["init", "--warehouse-root", str(root_b), "--prefix", "bbb"])[0], 0)

        conn = sqlite3.connect(root_a / "index.sqlite")
        with conn:
            conn.execute(
                "UPDATE id_counter SET next_value = 99 WHERE plane = 'n'"
            )
        conn.close()

        conn = sqlite3.connect(root_b / "index.sqlite")
        counter_b = conn.execute(
            "SELECT next_value FROM id_counter WHERE plane = 'n'"
        ).fetchone()[0]
        prefix_b = conn.execute(
            "SELECT value FROM meta WHERE key = 'project_prefix'"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(counter_b, 1)  # untouched by writes to root A
        self.assertEqual(prefix_b, "bbb")


if __name__ == "__main__":
    unittest.main()
