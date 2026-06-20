"""B4 — L2 subprocess CLI session (A17).

Drives `python3 -m warehouse_robot ...` as a real process through a realistic
write-path session: propose (stdin) -> Senate verdict -> the new node is
visible to a query verb inside its intent/verdict bracket -> divergence clean.
This is the contract (JSON/exit codes) that breaks silently and is painful to
debug in Foodoire — proven here against a disposable system-tmp instance.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

PROPOSAL = """---
kind: decision
status: active
title: Use embedded SQLite as the derived index
scope: substrate
origin: decided
ticket: SAW-30
agent: Praetor
---

Markdown is truth; the index is a disposable embedded-SQLite projection (S7).
"""


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, "-m", "warehouse_robot", *args],
        cwd=str(REPO_ROOT), input=stdin, capture_output=True, text=True,
    )


class CliSession(unittest.TestCase):
    def test_write_path_session_as_a_real_process(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d) / "project_memory" / "warehouse"
            a = Path(d) / "project_memory" / "antechamber"

            p = run(["init", "--warehouse-root", str(w), "--prefix", "demo", "--disposable"])
            self.assertEqual(p.returncode, 0, p.stderr)

            p = run(["propose", "--warehouse-root", str(w), "--antechamber-root", str(a),
                     "--ticket", "SAW-30", "--agent", "Praetor", "--file", "-"],
                    stdin=PROPOSAL)
            self.assertEqual(p.returncode, 0, p.stderr)
            key = json.loads(p.stdout)["proposal_key"]

            p = run(["resolve", "--warehouse-root", str(w), "--antechamber-root", str(a),
                     "--proposal-key", key, "--verdict", "ingested"])
            self.assertEqual(p.returncode, 0, p.stderr)
            node_id = json.loads(p.stdout)["node_id"]
            self.assertEqual(node_id, "demo-n1")

            # The new node is visible to a query verb (intent half of the bracket).
            p = run(["open-scope", "--warehouse-root", str(w), "--archetype", "execute",
                     "--session", "sess-1", "--intent", "find the substrate decision",
                     "--scope", "substrate"])
            self.assertEqual(p.returncode, 0, p.stderr)
            ids = [c["id"] for c in json.loads(p.stdout)["candidates"]]
            self.assertIn(node_id, ids)

            # Close the bracket (verdict half) — the trace stays well-formed.
            p = run(["verdict", "--warehouse-root", str(w), "--session", "sess-1",
                     "--verdict", "FOUND-ENOUGH"])
            self.assertEqual(p.returncode, 0, p.stderr)

            # B5 audit as a real process: the lone ingested decision has no
            # edges → the orphan tripwire flags it (exit 1 = findings present).
            p = run(["audit", "--warehouse-root", str(w)])
            self.assertEqual(p.returncode, 1, p.stderr)
            payload = json.loads(p.stdout)
            self.assertEqual(
                payload["emitted"],
                [{"flag_id": "demo-f1", "target": node_id, "flag_type": "orphan"}],
            )

            # Re-running the audit is idempotent — no duplicate flag is minted.
            p = run(["audit", "--warehouse-root", str(w)])
            self.assertEqual(p.returncode, 1, p.stderr)
            self.assertEqual(json.loads(p.stdout)["emitted"], [])

            # Markdown and both projections agree — the flag is canonical f-plane
            # markdown, folded at emission, so check stays clean.
            p = run(["check", "--warehouse-root", str(w), "--antechamber-root", str(a)])
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("antechamber: clean", p.stdout)


if __name__ == "__main__":
    unittest.main()
