"""B4 — the versioned proposal fixture set (A16).

Each fixture is a synthetic, project-neutral proposal exercising one gate
outcome. Like the B3 query set, the fixtures ride with the robot at import
and only ever fold into a disposable instance (A4).
"""

import tempfile
import unittest

from warehouse_robot import write_gate as wg
from warehouse_robot.errors import MalformedProposal

from ._write_helpers import build_instance, proposal_text

# fixture stem -> expected gate outcome
VALIDATED = "validated"            # passes the hard-gate -> pending-senate
REJECTED = "rejected-malformed"   # persisted rejection
STRUCTURAL = "structural"         # raised at the door, never persisted

EXPECTATIONS = {
    "valid-decision": VALIDATED,
    "valid-constraint": VALIDATED,
    "valid-lesson": VALIDATED,
    "valid-flag": VALIDATED,
    "born-retired": VALIDATED,
    "malformed-missing-scope": REJECTED,
    "malformed-missing-source": REJECTED,
    "malformed-missing-agent": REJECTED,
    "malformed-bad-edge-kind": REJECTED,
    "malformed-bad-kind": REJECTED,
    "malformed-has-id": STRUCTURAL,
}


class WriteFixtures(unittest.TestCase):
    def test_every_fixture_hits_its_expected_outcome(self):
        for name, expected in EXPECTATIONS.items():
            with self.subTest(fixture=name):
                with tempfile.TemporaryDirectory() as d:
                    w, a = build_instance(d)
                    text = proposal_text(name)
                    if expected == STRUCTURAL:
                        with self.assertRaises(MalformedProposal):
                            wg.propose(w, a, text, "SAW-30", "Praetor")
                        # nothing persisted
                        self.assertEqual(list(a.glob("*" + wg.SIDECAR_SUFFIX)), [])
                    else:
                        r = wg.propose(w, a, text, "SAW-30", "Praetor")
                        if expected == VALIDATED:
                            self.assertEqual(r["state"], "pending-senate")
                        else:
                            self.assertEqual(r["state"], "rejected-malformed")

    def test_all_valid_fixtures_ingest_through_the_gate(self):
        # The migration mints only via this gate (A18) — prove each valid
        # fixture survives the full propose->ingest path.
        with tempfile.TemporaryDirectory() as d:
            w, a = build_instance(d)
            ingested = []
            for name, expected in EXPECTATIONS.items():
                if expected != VALIDATED:
                    continue
                r = wg.propose(w, a, proposal_text(name), "SAW-30", "Praetor")
                res = wg.resolve(w, a, r["proposal_key"], "ingested")
                ingested.append(res["node_id"])
            self.assertEqual(len(ingested), 5)
            self.assertTrue(wg.check_antechamber(w, a).clean)


if __name__ == "__main__":
    unittest.main()
