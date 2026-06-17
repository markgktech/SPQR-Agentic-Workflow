"""Per-archetype query policy (B3): defaults, the single DENY, tightening."""

import unittest

from warehouse_robot.errors import PolicyDenied, ProtocolError
from warehouse_robot.policy import (
    ARCHETYPES,
    DEFAULT_POLICIES,
    LINEAGE_EDGE_TYPES,
    NONTERMINAL_VERDICTS,
    TERMINAL_VERDICTS,
    policy_for,
    tightened,
)


class PolicyTableTests(unittest.TestCase):
    def test_every_archetype_has_a_policy(self):
        self.assertEqual(set(DEFAULT_POLICIES), set(ARCHETYPES))
        for archetype in ARCHETYPES:
            self.assertEqual(policy_for(archetype).archetype, archetype)

    def test_unknown_archetype_is_rejected(self):
        with self.assertRaisesRegex(ProtocolError, "unknown archetype"):
            policy_for("builder")

    def test_scrutinize_is_the_only_true_deny(self):
        # S4: only SCRUTINIZE is blind to lineage + journey memory.
        scrutinize = policy_for("scrutinize")
        self.assertEqual(scrutinize.denied_edge_types, LINEAGE_EDGE_TYPES)
        self.assertFalse(scrutinize.include_inactive_allowed)
        for archetype in ARCHETYPES:
            if archetype == "scrutinize":
                continue
            pol = policy_for(archetype)
            self.assertEqual(pol.denied_edge_types, ())
            self.assertTrue(pol.include_inactive_allowed)

    def test_verdict_vocabulary_is_the_s4_set(self):
        self.assertEqual(
            set(TERMINAL_VERDICTS),
            {"FOUND-ENOUGH", "ABSENT", "FOUND-UNLINKED"},
        )
        self.assertEqual(
            set(NONTERMINAL_VERDICTS),
            {"WRONG-ENTRY", "INSUFFICIENT-TRAVERSE"},
        )

    def test_consult_and_scrutinize_have_tighter_body_ceilings(self):
        base = policy_for("deliberate").body_fetch_ceiling
        self.assertLess(policy_for("consult").body_fetch_ceiling, base)
        self.assertLess(policy_for("scrutinize").body_fetch_ceiling, base)


class TighteningTests(unittest.TestCase):
    def test_tightening_lowers_a_dial(self):
        pol = tightened(policy_for("execute"), body_fetch_ceiling=2, max_depth=1)
        self.assertEqual(pol.body_fetch_ceiling, 2)
        self.assertEqual(pol.max_depth, 1)
        self.assertEqual(pol.archetype, "execute")

    def test_loosening_is_denied(self):
        base = policy_for("consult")  # body_fetch_ceiling below the base dial
        with self.assertRaisesRegex(PolicyDenied, "continuation grant"):
            tightened(base, body_fetch_ceiling=base.body_fetch_ceiling + 1)

    def test_equal_value_is_allowed(self):
        base = policy_for("execute")
        pol = tightened(base, max_depth=base.max_depth)
        self.assertEqual(pol.max_depth, base.max_depth)

    def test_unknown_dial_is_rejected(self):
        with self.assertRaisesRegex(ProtocolError, "unknown budget dial"):
            tightened(policy_for("execute"), denied_edge_types=("about",))

    def test_non_positive_or_non_int_dial_is_rejected(self):
        for bad in (0, -1, True, "3", 2.5):
            with self.assertRaises(ProtocolError):
                tightened(policy_for("execute"), max_depth=bad)
