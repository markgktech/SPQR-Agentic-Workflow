"""Shared helpers for the B3 query-interface tests.

Every test builds a disposable instance under the system tmp directory (A4),
folds the versioned fixtures into it, queries against it, and deletes it.
Custom budget dials are injected as library-level policy objects — the CLI
only ever tightens the in-code defaults, it cannot loosen them.
"""

from warehouse_robot import query
from warehouse_robot.policy import QueryPolicy

from ._fold_helpers import fold_fixtures, init_instance


def build_instance(parent):
    """Disposable instance with all 14 fixture nodes folded in."""
    wroot = init_instance(parent)
    fold_fixtures(wroot)
    return wroot


def make_policy(archetype="execute", **overrides):
    """A policy with explicit dials; overrides replace the test defaults."""
    dials = dict(
        altitude_ceiling=50,
        wrong_entry_cap=3,
        traverse_cap=3,
        max_depth=3,
        body_fetch_ceiling=10,
        denied_edge_types=(),
        include_inactive_allowed=True,
    )
    dials.update(overrides)
    return QueryPolicy(archetype, **dials)


def q_open(wroot, session="s1", archetype="execute", intent="test intent", **kw):
    return query.open_scope(wroot, archetype, session, intent, **kw)


def q_find(wroot, text, session="s1", archetype="execute", intent="test intent", **kw):
    return query.find(wroot, archetype, session, intent, text, **kw)


def q_fetch(wroot, ids, session="s1", archetype="execute", intent="test intent", **kw):
    return query.fetch(wroot, archetype, session, intent, ids, **kw)


def q_traverse(wroot, node_id, edge_type, session="s1", archetype="execute",
               intent="test intent", **kw):
    return query.traverse(wroot, archetype, session, intent, node_id, edge_type, **kw)


def q_verdict(wroot, value, session="s1"):
    return query.verdict(wroot, session, value)


def candidate_ids(response):
    return [c["id"] for c in response["candidates"]]
