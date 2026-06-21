"""SAW-31 — the read-only `list-pending` verb (the Senate-wake's backing).

Listing reads the antechamber SIDECARS (the truth), not the disposable mirror.
Default surfaces the live queue (non-terminal proposals); `--state` filters to
exactly one lifecycle state. Every test builds a disposable instance under tmp
(A4/A12) — nothing reaches a canonical path or git.
"""

import json
import tempfile
import unittest
from pathlib import Path

from warehouse_robot import write_gate as wg
from warehouse_robot.errors import ConfigError

from ._fold_helpers import quiet_cli
from ._write_helpers import build_instance, make_proposal

TS = "2026-06-20T10:00:00Z"


def _decision(**kw):
    base = dict(kind="decision", scope="ledger", ticket="SAW-30", agent="Praetor")
    base.update(kw)
    return make_proposal(**base)


def _propose(w, a, **kw):
    return wg.propose(w, a, _decision(**kw), "SAW-30", "Praetor", now=TS)


def _seed_states(w, a):
    """One proposal in each of pending-senate / proposed / ingested / rejected /
    rejected-malformed. Keys allocate p1..p5 in creation order."""
    pend = _propose(w, a, title="Pending")                       # -> pending-senate
    prop = _propose(w, a, title="To revise")
    wg.resolve(w, a, prop["proposal_key"], "revise", now=TS)     # -> proposed
    ing = _propose(w, a, title="To ingest")
    wg.resolve(w, a, ing["proposal_key"], "ingested", now=TS)    # -> ingested
    rej = _propose(w, a, title="To reject")
    wg.resolve(w, a, rej["proposal_key"], "rejected", now=TS)    # -> rejected
    mal = wg.propose(w, a, make_proposal(kind="decision", ticket="SAW-30",
                                         agent="P"),              # no scope -> malformed
                     "SAW-30", "P", now=TS)
    return {
        "pending": pend["proposal_key"], "proposed": prop["proposal_key"],
        "ingested": ing["proposal_key"], "rejected": rej["proposal_key"],
        "malformed": mal["proposal_key"],
    }


class ListPendingUnit(unittest.TestCase):
    def test_default_returns_only_the_live_queue(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            keys = _seed_states(w, a)
            got = {r["proposal_key"] for r in wg.list_pending(w, a)}
            self.assertEqual(got, {keys["pending"], keys["proposed"]})

    def test_state_filter_returns_exactly_one_state(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            keys = _seed_states(w, a)
            rows = wg.list_pending(w, a, state="pending-senate")
            self.assertEqual([r["proposal_key"] for r in rows], [keys["pending"]])
            self.assertEqual(rows[0]["state"], "pending-senate")

    def test_state_filter_can_address_a_terminal_state(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            keys = _seed_states(w, a)
            rows = wg.list_pending(w, a, state="rejected-malformed")
            self.assertEqual([r["proposal_key"] for r in rows], [keys["malformed"]])

    def test_rows_carry_exactly_the_contract_fields(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            _propose(w, a, title="Only one")
            (row,) = wg.list_pending(w, a)
            self.assertEqual(set(row), {"proposal_key", "state", "ticket",
                                        "agent", "created_at", "content_file"})
            self.assertEqual(row["ticket"], "SAW-30")
            self.assertEqual(row["agent"], "Praetor")
            self.assertEqual(row["created_at"], TS)

    def test_empty_antechamber_lists_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            self.assertEqual(wg.list_pending(w, a), [])

    def test_order_is_numeric_not_lexical(self):
        # Cross the p1/p10 boundary so a lexical sort (p1, p10, p11, p2, ...)
        # would visibly differ from the required numeric order.
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            for i in range(11):
                _propose(w, a, title=f"Pending {i}")
            keys = [r["proposal_key"] for r in wg.list_pending(w, a)]
            self.assertEqual(keys, [f"{wg.format_proposal_key('demo', n)}"
                                    for n in range(1, 12)])

    def test_uninitialised_root_is_a_robot_error(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ConfigError):
                wg.list_pending(Path(d) / "nope", Path(d) / "antechamber")

    def test_default_antechamber_resolves_to_the_a3_sibling(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            _propose(w, a, title="Sibling default")
            # a == w.parent / "antechamber"; omit it and the function must find it
            rows = wg.list_pending(w)
            self.assertEqual(len(rows), 1)


class ListPendingCli(unittest.TestCase):
    def test_cli_emits_verb_count_pending_envelope(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            keys = _seed_states(w, a)
            code, out, err = quiet_cli(["list-pending", "--warehouse-root", str(w),
                                        "--antechamber-root", str(a)])
            self.assertEqual(code, 0, err)
            payload = json.loads(out)
            self.assertEqual(payload["verb"], "list-pending")
            self.assertEqual(payload["count"], 2)
            self.assertEqual({r["proposal_key"] for r in payload["pending"]},
                             {keys["pending"], keys["proposed"]})

    def test_cli_state_filter(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            keys = _seed_states(w, a)
            code, out, err = quiet_cli(["list-pending", "--warehouse-root", str(w),
                                        "--antechamber-root", str(a),
                                        "--state", "pending-senate"])
            self.assertEqual(code, 0, err)
            payload = json.loads(out)
            self.assertEqual(payload["count"], 1)
            self.assertEqual(payload["pending"][0]["proposal_key"], keys["pending"])

    def test_cli_empty_queue_is_exit_0_count_0(self):
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            code, out, err = quiet_cli(["list-pending", "--warehouse-root", str(w),
                                        "--antechamber-root", str(a)])
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)["count"], 0)

    def test_cli_uninitialised_root_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, err = quiet_cli(["list-pending", "--warehouse-root",
                                        str(Path(d) / "nope")])
            self.assertEqual(code, 2)
            self.assertIn("error:", err)


if __name__ == "__main__":
    unittest.main()
