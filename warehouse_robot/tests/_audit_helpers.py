"""Shared helpers for the B5 audit tests.

Every test builds a disposable instance under the system tmp directory (A4/
A12). The versioned audit fixtures live in `fixtures/audit/` — a subdir that
the demo-wide fold helpers (`fixtures/nodes`, `fixtures/flags`) never glob, so
the deliberately-broken nodes can never perturb the B1–B4 read/write tests.

  clean/  — a small connected graph that MUST produce zero flags (A16: the
            no-false-positives control).
  broken/ — folded ON TOP of clean/: an orphan (demo-n4), a lesson missing its
            about edge (demo-n5), and a relates-to over-user (demo-n6), plus
            two clean connected nodes (demo-n7/n8) that are demo-n6's edge
            targets and must not themselves trip a tripwire.
"""

import shutil
from pathlib import Path

from warehouse_robot import fold, schema

from ._fold_helpers import FIXTURE_PREFIX, FIXTURES_ROOT, init_instance

AUDIT_FIXTURES = FIXTURES_ROOT / "audit"


def _fold_dir(wroot, subdir):
    """Copy a versioned audit fixture subdir into the instance and fold each
    file incrementally (the B2 hot path). All audit fixtures are knowledge
    nodes, so they land in nodes/."""
    conn = schema.connect(Path(wroot) / schema.INDEX_FILENAME)
    try:
        for src in sorted((AUDIT_FIXTURES / subdir).glob("*.md")):
            dst = Path(wroot) / "nodes" / src.name
            shutil.copyfile(src, dst)
            fold.upsert_node_file(conn, wroot, dst, expected_prefix=FIXTURE_PREFIX)
    finally:
        conn.close()


def build_clean_instance(parent):
    """Disposable instance with the clean (zero-flag) graph only."""
    wroot = init_instance(parent)
    _fold_dir(wroot, "clean")
    return wroot


def build_broken_instance(parent):
    """Disposable instance with the clean graph + the deliberately-broken
    nodes folded on top (so demo-n6's relates-to targets resolve)."""
    wroot = init_instance(parent)
    _fold_dir(wroot, "clean")
    _fold_dir(wroot, "broken")
    return wroot
