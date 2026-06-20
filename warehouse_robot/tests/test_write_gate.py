"""B4 — proposal codec + hard-schema gate."""

import tempfile
import unittest

from warehouse_robot import write_gate as wg
from warehouse_robot.errors import MalformedProposal

from ._write_helpers import make_proposal


class ParseProposalText(unittest.TestCase):
    def test_parses_a_well_formed_proposal(self):
        text = make_proposal(scope="ledger", ticket="SAW-1", agent="Praetor",
                             edges=[("derived-from", "demo-n1")])
        draft = wg.parse_proposal_text(text)
        self.assertEqual(draft.kind, "decision")
        self.assertEqual(draft.scope, "ledger")
        self.assertEqual(draft.plane, "n")
        self.assertEqual([(e.type, e.target) for e in draft.edges],
                         [("derived-from", "demo-n1")])

    def test_flag_proposal_is_audit_plane(self):
        draft = wg.parse_proposal_text(make_proposal(kind="flag", origin="observed"))
        self.assertEqual(draft.plane, "f")

    def test_robot_stamped_key_is_structural_reject(self):
        # id / timestamp / schema_version are stamped by the robot — never persisted.
        for key, value in (("id", "demo-n5"), ("timestamp", "2026-01-01T00:00:00Z"),
                           ("schema_version", "1")):
            text = "---\n%s: %s\nkind: decision\nstatus: active\n" \
                   "title: X\norigin: decided\n---\n\nbody\n" % (key, value)
            with self.assertRaises(MalformedProposal):
                wg.parse_proposal_text(text)

    def test_unknown_key_and_bad_fence_are_structural_rejects(self):
        with self.assertRaises(MalformedProposal):
            wg.parse_proposal_text("no fence here\n")
        with self.assertRaises(MalformedProposal):
            wg.parse_proposal_text("---\nbogus: x\nkind: decision\n---\n\nbody\n")

    def test_out_of_order_key_is_structural_reject(self):
        text = "---\nstatus: active\nkind: decision\ntitle: X\norigin: decided\n---\n\nbody\n"
        with self.assertRaises(MalformedProposal):
            wg.parse_proposal_text(text)


class HardGate(unittest.TestCase):
    def _gate(self, **kw):
        wg.hard_gate(wg.parse_proposal_text(make_proposal(**kw)), "demo")

    def test_valid_decision_passes(self):
        self._gate(kind="decision", scope="ledger")

    def test_decision_requires_scope(self):
        with self.assertRaises(MalformedProposal):
            self._gate(kind="decision")  # no scope

    def test_constraint_requires_source(self):
        self._gate(kind="constraint", origin="inherited", source="platform")
        with self.assertRaises(MalformedProposal):
            self._gate(kind="constraint", origin="inherited")

    def test_lesson_requires_agent_and_ticket(self):
        self._gate(kind="lesson", origin="observed", ticket="SAW-1", agent="Probator")
        with self.assertRaises(MalformedProposal):
            self._gate(kind="lesson", origin="observed", ticket="SAW-1")  # no agent

    def test_unknown_kind_rejected_by_codec_layer(self):
        with self.assertRaises(MalformedProposal):
            self._gate(kind="idea")

    def test_edge_source_kind_enforced(self):
        # a constraint may not supersede (S3)
        with self.assertRaises(MalformedProposal):
            self._gate(kind="constraint", origin="inherited", source="x",
                       edges=[("supersedes", "demo-n2")])
        # a decision may emit resolves (verified against demo-n7)
        self._gate(kind="decision", scope="ledger",
                   edges=[("resolves", "demo-f2")])

    def test_born_retired_is_accepted(self):
        self._gate(kind="constraint", status="retired", origin="inherited",
                   source="legacy")

    def test_superseded_status_is_rejected(self):
        with self.assertRaises(MalformedProposal):
            self._gate(kind="decision", scope="x", status="superseded")


if __name__ == "__main__":
    unittest.main()
