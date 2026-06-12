import tempfile
import unittest
from pathlib import Path

from warehouse_robot.errors import CodecError
from warehouse_robot.store import (
    Edge,
    Node,
    node_relpath,
    parse_node_text,
    read_node_file,
    serialize_node,
    write_node_file,
)

CANONICAL = """---
id: demo-n7
kind: decision
status: active
title: Adopt result-based error envelopes
scope: error-handling
origin: decided
timestamp: 2026-06-05T09:30:00Z
ticket: DEMO-5
agent: Praetor
schema_version: 1
edges:
  - type: supersedes
    target: demo-n2
  - type: derived-from
    target: demo-n1
---

Body prose of the decision.
"""


def make_node(**overrides):
    base = dict(
        id="demo-n1",
        kind="decision",
        status="active",
        title="A title",
        origin="decided",
        timestamp="2026-06-01T09:00:00Z",
        schema_version=1,
        body="Body.\n",
        scope="architecture",
    )
    base.update(overrides)
    return Node(**base)


class RoundTripTests(unittest.TestCase):
    def test_parse_then_serialize_is_byte_identical(self):
        node = parse_node_text(CANONICAL)
        self.assertEqual(serialize_node(node), CANONICAL)

    def test_serialize_then_parse_is_equal(self):
        node = make_node(edges=[Edge("relates-to", "demo-n2")])
        self.assertEqual(parse_node_text(serialize_node(node)), node)

    def test_parsed_fields(self):
        node = parse_node_text(CANONICAL)
        self.assertEqual(node.id, "demo-n7")
        self.assertEqual(node.plane, "n")
        self.assertEqual(node.kind, "decision")
        self.assertEqual(node.schema_version, 1)
        self.assertEqual(
            node.edges,
            [Edge("supersedes", "demo-n2"), Edge("derived-from", "demo-n1")],
        )
        self.assertEqual(node.body, "Body prose of the decision.\n")

    def test_body_may_contain_fence_line(self):
        node = make_node(body="prose\n---\nmore prose\n")
        self.assertEqual(parse_node_text(serialize_node(node)), node)


class StrictRejectionTests(unittest.TestCase):
    """Owner condition on B1 #2: outside the canonical subset = explicit error."""

    def reject(self, text, pattern):
        with self.assertRaisesRegex(CodecError, pattern):
            parse_node_text(text)

    def test_missing_opening_fence(self):
        self.reject("id: demo-n1\n", "must start with")

    def test_missing_closing_fence(self):
        self.reject("---\nid: demo-n1\n", "closing")

    def test_missing_blank_line_after_fence(self):
        self.reject(CANONICAL.replace("---\n\nBody", "---\nBody"), "blank line")

    def test_extra_blank_line_before_body(self):
        self.reject(CANONICAL.replace("---\n\nBody", "---\n\n\nBody"), "extra blank")

    def test_tab_rejected(self):
        self.reject(CANONICAL.replace("kind: decision", "kind:\tdecision"), "tab")

    def test_unknown_key(self):
        self.reject(CANONICAL.replace("scope:", "scopes:"), "unknown frontmatter key")

    def test_out_of_canonical_order(self):
        broken = CANONICAL.replace(
            "id: demo-n7\nkind: decision", "kind: decision\nid: demo-n7"
        )
        self.reject(broken, "out of canonical order")

    def test_duplicate_key(self):
        self.reject(
            CANONICAL.replace("kind: decision", "kind: decision\nkind: decision"),
            "duplicated or out of canonical order",
        )

    def test_quoted_value(self):
        self.reject(
            CANONICAL.replace("title: Adopt", 'title: "Adopt'), "canonical scalar subset"
        )

    def test_flow_style_edges(self):
        self.reject(
            CANONICAL.replace("edges:\n  - type: supersedes\n    target: demo-n2\n", "edges: [x]\n"),
            "block of entries",
        )

    def test_empty_edges_block(self):
        text = CANONICAL.split("edges:")[0] + "edges:\n---\n\nBody.\n"
        self.reject(text, "at least one entry")

    def test_unknown_edge_type(self):
        self.reject(CANONICAL.replace("type: supersedes", "type: blocks"), "unknown edge type")

    def test_bad_edge_target(self):
        self.reject(CANONICAL.replace("target: demo-n2", "target: demo-x2"), "malformed node id")

    def test_continuation_line(self):
        self.reject(
            CANONICAL.replace("title: Adopt result-based error envelopes",
                              "title: Adopt result-based\n  error envelopes"),
            "outside the canonical subset",
        )

    def test_missing_required_key(self):
        self.reject(CANONICAL.replace("origin: decided\n", ""), "missing required keys")

    def test_stored_superseded_status(self):
        self.reject(
            CANONICAL.replace("status: active", "status: superseded"),
            "derived from an incoming supersedes edge",
        )

    def test_verdict_on_decision(self):
        self.reject(
            CANONICAL.replace("scope: error-handling",
                              "scope: error-handling\nverdict: GREEN"),
            "only valid on kind: lesson",
        )

    def test_flag_type_on_knowledge_plane(self):
        self.reject(
            CANONICAL.replace("scope: error-handling",
                              "scope: error-handling\nflag_type: orphan"),
            "only valid on the audit plane",
        )

    def test_flag_kind_on_knowledge_plane(self):
        self.reject(CANONICAL.replace("kind: decision", "kind: flag"), "not valid on plane")

    def test_bad_timestamp(self):
        self.reject(
            CANONICAL.replace("2026-06-05T09:30:00Z", "2026-06-05 09:30"), "timestamp"
        )

    def test_trailing_space_value(self):
        self.reject(CANONICAL.replace("agent: Praetor", "agent: Praetor "), "canonical scalar")

    def test_empty_body(self):
        self.reject(CANONICAL.replace("Body prose of the decision.\n", ""), "non-empty")

    def test_serialize_rejects_invalid_node(self):
        with self.assertRaises(CodecError):
            serialize_node(make_node(status="superseded"))
        with self.assertRaises(CodecError):
            serialize_node(make_node(edges=[Edge("blocks", "demo-n2")]))
        with self.assertRaises(CodecError):
            serialize_node(make_node(schema_version="1"))


class FileIoTests(unittest.TestCase):
    def test_relpath_by_plane(self):
        self.assertEqual(str(node_relpath("demo-n1")), "nodes/demo-n1.md")
        self.assertEqual(str(node_relpath("demo-f1")), "flags/demo-f1.md")

    def test_write_and_read_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "nodes").mkdir()
            node = make_node()
            path = write_node_file(root, node)
            self.assertEqual(path, root / "nodes" / "demo-n1.md")
            self.assertEqual(read_node_file(path), node)

    def test_write_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "nodes").mkdir()
            write_node_file(root, make_node())
            with self.assertRaisesRegex(CodecError, "append-only"):
                write_node_file(root, make_node())

    def test_read_rejects_filename_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "demo-n2.md"
            path.write_text(serialize_node(make_node()), encoding="utf-8")
            with self.assertRaisesRegex(CodecError, "does not match node id"):
                read_node_file(path)


if __name__ == "__main__":
    unittest.main()
