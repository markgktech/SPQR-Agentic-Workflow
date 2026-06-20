"""B5 — versioned audit-fixture tests (A16).

The deliberately-broken nodes and the clean control graph travel with the
robot in fixtures/audit/ (synthetic, project-neutral) and only ever fold into
a disposable instance. These tests pin the exact, governed flag set so a
calibration change to a dial or table is a visible diff, not a silent drift.
"""

import tempfile
import unittest

from warehouse_robot import audit

from ._audit_helpers import build_broken_instance, build_clean_instance

TS = "2026-06-20T12:00:00Z"


class AuditFixtures(unittest.TestCase):
    def test_clean_fixture_set_is_flag_free(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_clean_instance(d)
            r = audit.audit(w, now=TS)
            self.assertEqual(r["emitted"], [])
            self.assertEqual(r["open_flag_count"], 0)

    def test_broken_fixture_set_trips_exactly_the_three_tripwires(self):
        with tempfile.TemporaryDirectory() as d:
            w = build_broken_instance(d)
            r = audit.audit(w, now=TS)
            emitted = {(e["target"], e["flag_type"]) for e in r["emitted"]}
            self.assertEqual(emitted, {
                ("demo-n4", "orphan"),
                ("demo-n5", "missing-recommended-edge"),
                ("demo-n6", "relates-to-overuse"),
            })
            self.assertEqual(r["open_flag_count"], 3)
            # the clean connected nodes (n1,n2,n3,n7,n8) trip nothing
            flagged = {t for t, _ in emitted}
            for clean in ("demo-n1", "demo-n2", "demo-n3", "demo-n7", "demo-n8"):
                self.assertNotIn(clean, flagged)

    def test_emission_order_is_deterministic(self):
        """Findings emit in (flag_type, target) order, so the f-plane id
        assignment — and therefore the rebuild digest — is stable."""
        with tempfile.TemporaryDirectory() as d:
            w = build_broken_instance(d)
            r = audit.audit(w, now=TS)
            self.assertEqual(
                [(e["flag_id"], e["flag_type"]) for e in r["emitted"]],
                [("demo-f1", "missing-recommended-edge"),
                 ("demo-f2", "orphan"),
                 ("demo-f3", "relates-to-overuse")],
            )


if __name__ == "__main__":
    unittest.main()
