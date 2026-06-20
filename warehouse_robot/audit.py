"""The audit layer — deterministic, graph-structural tripwires (S6 Cluster B,
ticket B5). The last warehouse surface.

The tripwires ONLY ever FLAG; they never mutate, fix, or read a target's body
— they read the graph's shape and emit audit-plane flag nodes. A flag is an
append-only node on the SEPARATE audit plane (id marker `f`), pointing at its
target via a `flags` edge, never touching the target. Its open/resolved status
is DERIVED from an incoming `resolves` edge (`v_flag_status`) — the exact
mirror of S3's "superseded is derived". Resolution is a write-path / retro act
(B4 / SAW-31), NOT this module's concern.

Three tripwires (A14 — measurable predicates, numeric parts placeholder dials
calibrated later from real data, per the B3 budget-dial precedent):

- orphan = an ACTIVE knowledge node (decision/constraint/lesson) with ZERO
  incident KNOWLEDGE-plane edges, EXCLUDING origin-flagged foundational nodes.
  "Knowledge-plane edges" means the S3 typed set (supersedes/derived-from/
  constrains/about/relates-to); the audit-plane `flags`/`resolves` edges do
  NOT count as knowledge connectivity (else emitting a flag would "heal" the
  orphan, and a flagged orphan could never be re-detected). "Foundational" =
  origin `inherited` (platform axioms — Apple HIG / Swift-naming class — that
  legitimately stand alone).

- relates-to overuse = a node carrying (as the edge SOURCE) more than K
  `relates-to` edges. K = 5 (placeholder). `relates-to` is the second-class
  fallback edge (S3); overuse is the "Jira relate-vs-child-of" smell.

- missing-recommended-edge = a node whose kind is expected to carry an edge it
  lacks, per a per-kind table SEEDED from Session 3 with the single
  architecture-stated rule `lesson -> about` (strongly recommended). The table
  grows only by governance — no invented rules.

Idempotency (re-run safety): a flag is keyed to (target, flag_type). The audit
emits a flag only when no OPEN flag of that type already targets the node, so a
re-run over a standing condition is a no-op, never a duplicate. A *resolved*
flag does not block re-emission — a condition that recurs after resolution is a
real new finding.

Scope fence (NOT a B5 tripwire — flag if found): the periodic semantic /
contradiction audit (owner-driven), code/convention freshness (SAW-40), the
promotion gate (SAW-31), severity-metric calibration (parked). B5 stays purely
graph-structural.
"""

from datetime import datetime, timezone
from pathlib import Path

from . import config, schema, store, write_gate
from .errors import AuditError
from .store import Edge

# --- tripwire identifiers (also the flag_type slugs; [a-z][a-z0-9-]*) -------
TRIPWIRE_ORPHAN = "orphan"
TRIPWIRE_OVERUSE = "relates-to-overuse"
TRIPWIRE_MISSING_EDGE = "missing-recommended-edge"

# --- dials & tables (placeholders / governance-seeded) ----------------------
K_RELATES_TO = 5  # placeholder dial (B3/B4 precedent), retro-calibrated
FOUNDATIONAL_ORIGIN = "inherited"  # platform axioms legitimately stand alone (A14)

# Per-kind recommended-edge table, seeded from Session 3 (the single
# architecture-stated rule). Grows ONLY by governance — no invented rules (A14).
RECOMMENDED_EDGES = {
    "lesson": ("about",),
}

# Minimal PLACEHOLDER severity — the S6 hybrid's small fixed floor. The real
# emergent `frequency x damage` metric is the parked measurement lane; B5 does
# not calibrate (scope fence). Severity is written into the flag BODY (prose),
# never a schema column (no DDL change — schema_version stays 1).
_SEVERITY_FLOOR = {
    TRIPWIRE_ORPHAN: "medium",
    TRIPWIRE_OVERUSE: "low",
    TRIPWIRE_MISSING_EDGE: "low",
}

_KNOWLEDGE_EDGE_PLACEHOLDERS = ",".join("?" for _ in store.KNOWLEDGE_EDGE_TYPES)


def _utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Tripwire detectors — pure reads over the derived index (no mutation)
# ---------------------------------------------------------------------------

def _find_orphans(conn):
    """Active knowledge nodes with no incident knowledge-plane edge, excluding
    foundational (inherited) nodes. Audit-plane edges do not count (A14)."""
    return conn.execute(
        f"""
        SELECT n.id, n.title FROM nodes n
        JOIN v_effective_status es ON es.id = n.id
        WHERE n.plane = 'n'
          AND es.effective_status = 'active'
          AND n.origin != ?
          AND NOT EXISTS (
            SELECT 1 FROM edges e
            WHERE e.type IN ({_KNOWLEDGE_EDGE_PLACEHOLDERS})
              AND (e.src = n.id OR e.target = n.id))
        ORDER BY n.id
        """,
        (FOUNDATIONAL_ORIGIN, *store.KNOWLEDGE_EDGE_TYPES),
    ).fetchall()


def _find_overuse(conn, k=K_RELATES_TO):
    """Active knowledge nodes carrying (as src) more than k relates-to edges."""
    return conn.execute(
        """
        SELECT e.src, n.title, COUNT(*) AS c FROM edges e
        JOIN nodes n ON n.id = e.src
        JOIN v_effective_status es ON es.id = n.id
        WHERE e.type = 'relates-to'
          AND n.plane = 'n'
          AND es.effective_status = 'active'
        GROUP BY e.src
        HAVING c > ?
        ORDER BY e.src
        """,
        (k,),
    ).fetchall()


def _find_missing_edges(conn):
    """Active knowledge nodes whose kind has a recommended out-edge it lacks."""
    findings = []
    for kind, required_types in sorted(RECOMMENDED_EDGES.items()):
        for etype in required_types:
            rows = conn.execute(
                """
                SELECT n.id, n.title FROM nodes n
                JOIN v_effective_status es ON es.id = n.id
                WHERE n.plane = 'n' AND n.kind = ?
                  AND es.effective_status = 'active'
                  AND NOT EXISTS (
                    SELECT 1 FROM edges e
                    WHERE e.src = n.id AND e.type = ?)
                ORDER BY n.id
                """,
                (kind, etype),
            ).fetchall()
            findings.extend((node_id, title, kind, etype) for node_id, title in rows)
    return findings


# ---------------------------------------------------------------------------
# Flag plane — dedup (idempotency) + emission + heat census
# ---------------------------------------------------------------------------

def _has_open_flag(conn, target, flag_type):
    """Is there already an OPEN flag of this type pointing at this target?
    The (target, flag_type) dedup key that makes a re-run idempotent."""
    return conn.execute(
        """
        SELECT 1 FROM nodes n
        JOIN edges e ON e.src = n.id AND e.type = 'flags' AND e.target = ?
        JOIN v_flag_status fs ON fs.id = n.id
        WHERE n.plane = 'f' AND n.flag_type = ? AND fs.flag_status = 'open'
        LIMIT 1
        """,
        (target, flag_type),
    ).fetchone() is not None


def _emit_flag(conn, warehouse_root, cfg, *, target, flag_type, title, detail, now):
    """Append a flag node on the audit plane (kind: flag, a `flags` edge at the
    target). Reuses the single ID-allocation path (write_gate.append_node) —
    flags do NOT enter the antechamber / Senate flow (deterministic robot
    output, not a proposal needing semantic judgment)."""
    severity = _SEVERITY_FLOOR[flag_type]
    body = (
        f"{detail}\n\n"
        f"severity: {severity} (placeholder fixed floor — the real frequency x "
        f"damage metric is the parked measurement lane; B5 emits structural "
        f"flags only).\n"
    )
    flag_id, _ = write_gate.append_node(
        conn, warehouse_root, cfg, kind="flag", status="active", title=title,
        origin="observed", flag_type=flag_type, body=body, now=now,
        edges=[Edge("flags", target)],
    )
    return flag_id


def _open_flag_census(conn):
    """Node 'heat' = the count of OPEN flags per target (aggregate, S6)."""
    rows = conn.execute(
        """
        SELECT e.target, COUNT(*) AS c FROM nodes n
        JOIN edges e ON e.src = n.id AND e.type = 'flags'
        JOIN v_flag_status fs ON fs.id = n.id
        WHERE n.plane = 'f' AND fs.flag_status = 'open'
        GROUP BY e.target
        ORDER BY c DESC, e.target
        """
    ).fetchall()
    return [{"target": target, "open_flags": count} for target, count in rows]


def _open_flag_count(conn):
    return conn.execute(
        "SELECT COUNT(*) FROM nodes n "
        "JOIN v_flag_status fs ON fs.id = n.id "
        "WHERE n.plane = 'f' AND fs.flag_status = 'open'"
    ).fetchone()[0]


# ---------------------------------------------------------------------------
# The audit run
# ---------------------------------------------------------------------------

def _collect_findings(conn):
    """Run the three detectors → a flat list of (target, flag_type, title,
    detail) tuples, in a deterministic (flag_type, target) order so emission
    (and therefore the f-plane id assignment and the rebuild digest) is stable
    across runs."""
    findings = []
    for node_id, title in _find_orphans(conn):
        findings.append((
            node_id, TRIPWIRE_ORPHAN,
            f"Orphan watch: {node_id} has no knowledge edges",
            f"{node_id} ({title}) is an active knowledge node with no incident "
            f"knowledge-plane edge and is not foundational (origin != "
            f"{FOUNDATIONAL_ORIGIN}). An orphan is unreachable by traversal.",
        ))
    for src, title, count in _find_overuse(conn):
        findings.append((
            src, TRIPWIRE_OVERUSE,
            f"relates-to overuse: {src} carries {count} relates-to edges",
            f"{src} ({title}) declares {count} relates-to edges (> K="
            f"{K_RELATES_TO}); relates-to is the second-class fallback edge "
            f"(S3) — consider a typed edge for the strong relations.",
        ))
    for node_id, title, kind, etype in _find_missing_edges(conn):
        findings.append((
            node_id, TRIPWIRE_MISSING_EDGE,
            f"missing recommended edge: {node_id} ({kind}) lacks an {etype} edge",
            f"{node_id} ({title}) is a {kind} but carries no outbound {etype} "
            f"edge (Session 3 recommends {kind} -> {etype}).",
        ))
    return sorted(findings, key=lambda f: (f[1], f[0]))


def audit(warehouse_root, *, now=None):
    """Run the three deterministic tripwires against the derived index and emit
    a flag (audit plane) for each NEW standing condition. Flag-only: nothing
    on the knowledge plane is ever mutated.

    Returns a structured report:
      emitted          — flags created this run [{flag_id, target, flag_type}]
      skipped_existing — conditions already covered by an OPEN flag (idempotent)
      open_flag_count  — total OPEN flags after the run
      heat             — open-flag census per target (node 'heat')
    """
    warehouse_root = Path(warehouse_root)
    cfg = config.load_config(warehouse_root)  # asserts an initialised root
    index_path = warehouse_root / schema.INDEX_FILENAME
    if not index_path.exists():
        raise AuditError(
            f"no derived index at {index_path} — run reconcile before the audit"
        )
    now = now or _utc_now()

    conn = schema.connect(index_path)
    try:
        emitted, skipped = [], []
        for target, flag_type, title, detail in _collect_findings(conn):
            if _has_open_flag(conn, target, flag_type):
                skipped.append({"target": target, "flag_type": flag_type})
                continue
            flag_id = _emit_flag(conn, warehouse_root, cfg, target=target,
                                 flag_type=flag_type, title=title, detail=detail,
                                 now=now)
            emitted.append({"flag_id": flag_id, "target": target,
                            "flag_type": flag_type})
        return {
            "verb": "audit",
            "emitted": emitted,
            "skipped_existing": skipped,
            "open_flag_count": _open_flag_count(conn),
            "heat": _open_flag_census(conn),
        }
    finally:
        conn.close()
