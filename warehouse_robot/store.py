"""Markdown node store — the canonical frontmatter codec and node file I/O.

Markdown is the source of truth (S7); this module defines the only file
format the robot reads or writes. The codec is strictly rejecting (owner
condition on B1 question #2): any input outside the canonical subset raises
CodecError with a precise reason — the codec never guesses or repairs.

Canonical node file:

    ---
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
    ---

    <body prose>

Grammar highlights (the full spec lives in docs/NODE_FORMAT.md):
- keys appear in canonical order; optional keys are omitted, never empty
- values are plain scalars — no quoting, no flow style, no multi-line
- `edges:` is always the last key and has at least one entry when present
- exactly one blank line between the closing fence and the body
- `superseded` is never a stored status — it is derived from an incoming
  `supersedes` edge (S3 invariant)

Round-trip guarantee: serialize(parse(text)) == text for every accepted
text, and parse(serialize(node)) == node for every valid node. This is the
precondition for B2's byte-identical reconcile rebuild.

Out of scope here (B4 write gate): per-kind conditional field requirements
(decision→scope, constraint→source, lesson→agent+ticket) and edge
endpoint-kind rules (e.g. supersedes is decision→decision).
"""

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from .errors import CodecError, IdError
from .ids import AUDIT_PLANE, KNOWLEDGE_PLANE, parse_id

KNOWLEDGE_EDGE_TYPES = ("supersedes", "derived-from", "constrains", "about", "relates-to")
AUDIT_EDGE_TYPES = ("flags", "resolves")
EDGE_TYPES = KNOWLEDGE_EDGE_TYPES + AUDIT_EDGE_TYPES

KNOWLEDGE_KINDS = ("decision", "constraint", "lesson")
AUDIT_KINDS = ("flag",)
STATUSES = ("active", "retired")
ORIGINS = ("decided", "inherited", "observed")
VERDICTS = ("GREEN", "YELLOW", "RED")

KEY_ORDER = (
    "id", "kind", "status", "title", "scope", "verdict", "flag_type",
    "origin", "timestamp", "ticket", "agent", "source", "schema_version",
)
REQUIRED_KEYS = ("id", "kind", "status", "title", "origin", "timestamp", "schema_version")

NODES_DIR = "nodes"
FLAGS_DIR = "flags"

_KEY_LINE_RE = re.compile(r"^([a-z][a-z0-9_]*): (.*)$")
_VALUE_RE = re.compile(r"^[A-Za-z0-9(][A-Za-z0-9 ._:/()&+,;'?-]*$")
_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_SCHEMA_VERSION_RE = re.compile(r"^[1-9][0-9]*$")
_EDGE_TYPE_LINE_RE = re.compile(r"^  - type: (.*)$")
_EDGE_TARGET_LINE_RE = re.compile(r"^    target: (.*)$")


@dataclass(frozen=True)
class Edge:
    type: str
    target: str


@dataclass
class Node:
    id: str
    kind: str
    status: str
    title: str
    origin: str
    timestamp: str
    schema_version: int
    body: str
    scope: str = None
    verdict: str = None
    flag_type: str = None
    ticket: str = None
    agent: str = None
    source: str = None
    edges: list = field(default_factory=list)

    @property
    def plane(self):
        return parse_id(self.id)[1]


def parse_node_text(text):
    """Parse a canonical node file into a Node; CodecError on any deviation."""
    if not isinstance(text, str) or not text.startswith("---\n"):
        raise CodecError("node file must start with a '---' fence line")
    fence_at = text.find("\n---\n", 3)
    if fence_at == -1:
        raise CodecError("closing '---' fence not found")
    fm_block = text[4:fence_at]
    rest = text[fence_at + 5:]
    if not rest.startswith("\n"):
        raise CodecError("exactly one blank line is required after the closing fence")
    body = rest[1:]
    fields, edges = _parse_frontmatter(fm_block)
    return _build_node(fields, edges, body)


def serialize_node(node):
    """Serialize a Node to its canonical text; CodecError if the node is invalid."""
    fields = _fields_from_node(node)
    for key, value in fields.items():
        _validate_scalar(key, value)
    _build_node(dict(fields), list(node.edges), node.body)  # full semantic check
    lines = ["---"]
    for key in KEY_ORDER:
        if key in fields:
            lines.append(f"{key}: {fields[key]}")
    if node.edges:
        lines.append("edges:")
        for edge in node.edges:
            lines.append(f"  - type: {edge.type}")
            lines.append(f"    target: {edge.target}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + node.body


def node_relpath(node_id):
    """Path of a node file relative to the warehouse root, by plane."""
    _, plane, _ = parse_id(node_id)
    subdir = NODES_DIR if plane == KNOWLEDGE_PLANE else FLAGS_DIR
    return Path(subdir) / f"{node_id}.md"


def read_node_file(path):
    path = Path(path)
    node = parse_node_text(path.read_text(encoding="utf-8"))
    if path.name != f"{node.id}.md":
        raise CodecError(f"filename {path.name!r} does not match node id {node.id!r}")
    return node


def write_node_file(warehouse_root, node):
    """Write a node under the warehouse root; refuses to overwrite (append-only)."""
    text = serialize_node(node)
    path = Path(warehouse_root) / node_relpath(node.id)
    if path.exists():
        raise CodecError(f"refusing to overwrite existing node file: {path} (append-only store)")
    path.write_text(text, encoding="utf-8")
    return path


def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _parse_frontmatter(fm_block):
    lines = fm_block.split("\n")
    fields = {}
    edges = []
    last_idx = -1
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == "edges:":
            edges = _parse_edges(lines, i + 1)
            i = len(lines)
            break
        if "\t" in line:
            raise CodecError(f"tab character in frontmatter line: {line!r}")
        m = _KEY_LINE_RE.match(line)
        if not m:
            raise CodecError(f"frontmatter line outside the canonical subset: {line!r}")
        key, value = m.group(1), m.group(2)
        if key == "edges":
            raise CodecError("'edges' takes a block of entries, not an inline value")
        if key not in KEY_ORDER:
            raise CodecError(f"unknown frontmatter key: {key!r}")
        idx = KEY_ORDER.index(key)
        if idx <= last_idx:
            raise CodecError(f"frontmatter key {key!r} is duplicated or out of canonical order")
        last_idx = idx
        _validate_scalar(key, value)
        fields[key] = value
        i += 1
    return fields, edges


def _parse_edges(lines, start):
    if start >= len(lines):
        raise CodecError("'edges:' block must contain at least one entry")
    edges = []
    i = start
    while i < len(lines):
        m = _EDGE_TYPE_LINE_RE.match(lines[i])
        if not m:
            raise CodecError(f"expected edge entry '  - type: <type>', got: {lines[i]!r}")
        edge_type = m.group(1)
        i += 1
        if i >= len(lines):
            raise CodecError("edge entry is missing its '    target: <id>' line")
        m = _EDGE_TARGET_LINE_RE.match(lines[i])
        if not m:
            raise CodecError(f"expected '    target: <id>', got: {lines[i]!r}")
        edges.append(Edge(type=edge_type, target=m.group(1)))
        i += 1
    return edges


def _validate_scalar(key, value):
    if not isinstance(value, str) or not _VALUE_RE.match(value) or value.endswith(" "):
        raise CodecError(f"value for {key!r} outside the canonical scalar subset: {value!r}")


def _fields_from_node(node):
    fields = {}
    for key in KEY_ORDER:
        if key == "schema_version":
            if not isinstance(node.schema_version, int) or isinstance(node.schema_version, bool):
                raise CodecError("schema_version must be an integer")
            fields[key] = str(node.schema_version)
            continue
        value = getattr(node, key)
        if value is None:
            continue
        if not isinstance(value, str):
            raise CodecError(f"{key} must be a string, got {type(value).__name__}")
        fields[key] = value
    return fields


def _build_node(fields, edges, body):
    missing = [k for k in REQUIRED_KEYS if k not in fields]
    if missing:
        raise CodecError(f"missing required keys: {', '.join(missing)}")

    node_id = fields["id"]
    try:
        _, plane, _ = parse_id(node_id)
    except IdError as exc:
        raise CodecError(str(exc)) from exc

    kind = fields["kind"]
    allowed_kinds = KNOWLEDGE_KINDS if plane == KNOWLEDGE_PLANE else AUDIT_KINDS
    if kind not in allowed_kinds:
        raise CodecError(f"kind {kind!r} is not valid on plane {plane!r}")

    status = fields["status"]
    if status not in STATUSES:
        if status == "superseded":
            raise CodecError(
                "'superseded' is derived from an incoming supersedes edge, never stored (S3)"
            )
        raise CodecError(f"unknown status: {status!r} (expected one of {STATUSES})")

    if fields["origin"] not in ORIGINS:
        raise CodecError(f"unknown origin: {fields['origin']!r} (expected one of {ORIGINS})")
    if not _TIMESTAMP_RE.match(fields["timestamp"]):
        raise CodecError(
            f"timestamp {fields['timestamp']!r} must be UTC in the form YYYY-MM-DDTHH:MM:SSZ"
        )
    if not _SCHEMA_VERSION_RE.match(fields["schema_version"]):
        raise CodecError(f"schema_version must be a positive integer, got {fields['schema_version']!r}")

    verdict = fields.get("verdict")
    if verdict is not None:
        if kind != "lesson":
            raise CodecError("verdict is only valid on kind: lesson (S5)")
        if verdict not in VERDICTS:
            raise CodecError(f"unknown verdict: {verdict!r} (expected one of {VERDICTS})")

    flag_type = fields.get("flag_type")
    if flag_type is not None:
        if plane != AUDIT_PLANE:
            raise CodecError("flag_type is only valid on the audit plane")
        if not _SLUG_RE.match(flag_type):
            raise CodecError(f"invalid flag_type {flag_type!r}: must match [a-z][a-z0-9-]*")

    scope = fields.get("scope")
    if scope is not None and not _SLUG_RE.match(scope):
        raise CodecError(f"invalid scope {scope!r}: must match [a-z][a-z0-9-]*")

    seen = set()
    for edge in edges:
        if not isinstance(edge, Edge):
            raise CodecError("edges must be Edge instances")
        if edge.type not in EDGE_TYPES:
            raise CodecError(f"unknown edge type: {edge.type!r} (expected one of {EDGE_TYPES})")
        try:
            parse_id(edge.target)
        except IdError as exc:
            raise CodecError(f"edge target invalid: {exc}") from exc
        if edge in seen:
            raise CodecError(f"duplicate edge: {edge.type} -> {edge.target}")
        seen.add(edge)

    if not isinstance(body, str) or body == "":
        raise CodecError("body must be non-empty prose")
    if body.startswith("\n"):
        raise CodecError("body must start right after the single blank line (no extra blank lines)")
    if not body.endswith("\n"):
        raise CodecError("body must end with a newline")

    return Node(
        id=node_id,
        kind=kind,
        status=status,
        title=fields["title"],
        origin=fields["origin"],
        timestamp=fields["timestamp"],
        schema_version=int(fields["schema_version"]),
        body=body,
        scope=scope,
        verdict=verdict,
        flag_type=flag_type,
        ticket=fields.get("ticket"),
        agent=fields.get("agent"),
        source=fields.get("source"),
        edges=list(edges),
    )
