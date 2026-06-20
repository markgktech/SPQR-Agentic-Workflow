"""Shared helpers for the B4 write-gate tests.

Every test builds a disposable instance under the system tmp directory (A4/
A12): the warehouse root AND its antechamber sibling live under one tmp
parent and are deleted together. Nothing ever enters a canonical path or git.
"""

from pathlib import Path

from warehouse_robot import store

from ._fold_helpers import FIXTURES_ROOT, FIXTURE_PREFIX, fold_fixtures, init_instance

PROPOSALS_ROOT = FIXTURES_ROOT / "proposals"


def build_instance(parent, with_fixtures=True):
    """Disposable instance; fixtures folded in so edge targets (demo-n*) exist.

    Returns (warehouse_root, antechamber_root) — the A3 sibling layout."""
    wroot = init_instance(parent)
    if with_fixtures:
        fold_fixtures(wroot)
    return wroot, wroot.parent / "antechamber"


def proposal_text(name):
    """Load a versioned proposal fixture by file stem (e.g. 'valid-decision')."""
    return (PROPOSALS_ROOT / f"{name}.md").read_text(encoding="utf-8")


def make_proposal(kind="decision", title="A test proposal", body="Body text.\n",
                  **fields):
    """Build a proposal markdown string for unit tests (no id/timestamp/
    schema_version — the robot stamps those)."""
    defaults = {"status": "active", "origin": "decided"}
    defaults.update(fields)
    order = ("kind", "status", "title", "scope", "verdict", "flag_type",
             "origin", "ticket", "agent", "source")
    values = {"kind": kind, "title": title, **defaults}
    edges = values.pop("edges", None)
    lines = ["---"]
    for key in order:
        if values.get(key) is not None:
            lines.append(f"{key}: {values[key]}")
    if edges:
        lines.append("edges:")
        for etype, target in edges:
            lines.append(f"  - type: {etype}")
            lines.append(f"    target: {target}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body


def mirror_rows(warehouse_root):
    from warehouse_robot import schema
    conn = schema.connect(Path(warehouse_root) / schema.INDEX_FILENAME)
    try:
        cols = [c[1] for c in conn.execute("PRAGMA table_info(antechamber)")]
        return [dict(zip(cols, row)) for row in conn.execute("SELECT * FROM antechamber")]
    finally:
        conn.close()


def mirror_state(warehouse_root, key):
    for row in mirror_rows(warehouse_root):
        if row["proposal_key"] == key:
            return row["state"]
    return None
