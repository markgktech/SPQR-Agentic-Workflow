"""Identity scheme for warehouse nodes (S3 Cluster 4).

ID form: <project-prefix>-<plane-marker><number>, e.g. food-n23.

The plane marker discriminates the knowledge plane ('n') from the audit/flag
plane ('f') — it does NOT encode the kind (S3: no kind in the ID; the marker
names the universal node type's plane, human readability comes from title).
Numbers are sequential per plane, unique but not gapless (a crash-skipped
number is acceptable, S7).
"""

import re

from .errors import IdError

KNOWLEDGE_PLANE = "n"
AUDIT_PLANE = "f"
PLANES = (KNOWLEDGE_PLANE, AUDIT_PLANE)

PREFIX_RE = re.compile(r"^[a-z][a-z0-9]*$")
ID_RE = re.compile(r"^(?P<prefix>[a-z][a-z0-9]*)-(?P<plane>[nf])(?P<number>[1-9][0-9]*)$")


def parse_id(node_id):
    """Split a node ID into (prefix, plane, number); raise IdError if malformed."""
    if not isinstance(node_id, str):
        raise IdError(f"node id must be a string, got {type(node_id).__name__}")
    m = ID_RE.match(node_id)
    if not m:
        raise IdError(f"malformed node id: {node_id!r} (expected <prefix>-<n|f><number>)")
    return m.group("prefix"), m.group("plane"), int(m.group("number"))


def format_id(prefix, plane, number):
    """Build a node ID from its parts; raise IdError on invalid parts."""
    if not isinstance(prefix, str) or not PREFIX_RE.match(prefix):
        raise IdError(f"malformed project prefix: {prefix!r} (expected [a-z][a-z0-9]*)")
    if plane not in PLANES:
        raise IdError(f"unknown plane marker: {plane!r} (expected one of {PLANES})")
    if not isinstance(number, int) or isinstance(number, bool) or number < 1:
        raise IdError(f"node number must be a positive integer, got {number!r}")
    return f"{prefix}-{plane}{number}"
