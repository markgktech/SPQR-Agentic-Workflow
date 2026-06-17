"""The fold — markdown truth into the derived SQLite index (S7 Cluster 2, B2).

Markdown is the source of truth; the index is a disposable, rebuildable
projection. Three surfaces:

- Hot path: `upsert_node_file` — one node mirrored into the index inside a
  single write transaction (nodes row + edges + manual FTS5 sync; external-
  content FTS tables never auto-sync). Library API only — the production
  caller is the B4 serializing gate; a public CLI fold command would open a
  gate-bypassing write path.
- Cold path: `rebuild` — reconcile/recovery. Builds a fresh index from the
  markdown tree in deterministic order (nodes by plane+number, edges sorted),
  re-derives `id_counter` as markdown max+1 per plane (S7), carries `trace`
  and `antechamber` rows over verbatim from the previous index (A8 — they are
  not derivable from warehouse markdown), then atomically replaces the old
  index after a WAL checkpoint.
- `check` — the cheap divergence check: per-file content-hash + count
  comparison, markdown vs index, reporting exactly which file diverged.

A8 exit criterion realized here:
1. Rebuild determinism — two `rebuild` runs from the same markdown tree (and
   the same carried-over state) produce byte-identical index files.
2. Live-vs-rebuild equivalence — `logical_digest` is the canonical ordered
   dump-hash of the derived tables (meta, nodes, edges, id_counter) plus an
   FTS5 integrity check; the live index and a fresh rebuild must agree on it.

Derived statuses (superseded / resolved) need no recompute step at the fold:
B1 realized them as SQL views, so the S7 "recompute edge-neighbor status"
delta is free by construction.

The fold is a mechanism, not a gate: markdown is truth, so an upsert always
mirrors the file as-is — detecting append-only violations (hand-edited node
files) is the job of `check` and the B5 audit, not of the fold.
"""

import hashlib
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from . import config, schema, store
from .errors import FoldError, RobotError
from .ids import AUDIT_PLANE, KNOWLEDGE_PLANE, parse_id

REBUILD_SUFFIX = ".rebuild"

_NODE_COLUMNS = (
    "id", "plane", "kind", "status", "title", "scope", "verdict", "flag_type",
    "origin", "timestamp", "ticket", "agent", "source", "schema_version",
    "body", "content_hash", "file_path",
)

_TRACE_COLUMNS = (
    "round_id", "ts", "session_id", "ticket", "agent", "archetype", "verb",
    "intent", "params", "result_count", "result_ids", "verdict", "budget",
)

_ANTECHAMBER_COLUMNS = (
    "proposal_key", "state", "ticket", "agent", "created_at", "updated_at",
    "content_hash", "file_path", "node_id",
)

_DIGEST_QUERIES = (
    ("meta", "SELECT key, value FROM meta ORDER BY key"),
    (
        "nodes",
        "SELECT " + ", ".join(_NODE_COLUMNS) + " FROM nodes ORDER BY id",
    ),
    ("edges", "SELECT src, type, target FROM edges ORDER BY src, type, target"),
    ("id_counter", "SELECT plane, next_value FROM id_counter ORDER BY plane"),
)


# ---------------------------------------------------------------------------
# Hot path — incremental upsert
# ---------------------------------------------------------------------------

def upsert_node(conn, node, text, file_path):
    """Mirror one parsed node into the index, in a single write transaction.

    Idempotent: re-folding the same file leaves the logical state unchanged.
    Also keeps the id_counter invariant (next_value >= max+1 per plane) so a
    fold of pre-existing files cannot leave the counter behind the markdown.
    """
    _, plane, number = parse_id(node.id)
    with conn:
        old = conn.execute(
            "SELECT rowid, title, body FROM nodes WHERE id = ?", (node.id,)
        ).fetchone()
        if old is not None:
            # External-content FTS5: the old row must be deleted explicitly,
            # with its old content, before the content row goes away.
            conn.execute(
                "INSERT INTO nodes_fts (nodes_fts, rowid, title, body) "
                "VALUES ('delete', ?, ?, ?)",
                old,
            )
            conn.execute("DELETE FROM edges WHERE src = ?", (node.id,))
            conn.execute("DELETE FROM nodes WHERE id = ?", (node.id,))
        cur = conn.execute(
            "INSERT INTO nodes (" + ", ".join(_NODE_COLUMNS) + ") VALUES ("
            + ", ".join("?" for _ in _NODE_COLUMNS) + ")",
            (
                node.id, plane, node.kind, node.status, node.title, node.scope,
                node.verdict, node.flag_type, node.origin, node.timestamp,
                node.ticket, node.agent, node.source, node.schema_version,
                node.body, store.content_hash(text), file_path,
            ),
        )
        conn.executemany(
            "INSERT INTO edges (src, type, target) VALUES (?, ?, ?)",
            sorted((node.id, e.type, e.target) for e in node.edges),
        )
        conn.execute(
            "INSERT INTO nodes_fts (rowid, title, body) VALUES (?, ?, ?)",
            (cur.lastrowid, node.title, node.body),
        )
        conn.execute(
            "UPDATE id_counter SET next_value = ? WHERE plane = ? AND next_value < ?",
            (number + 1, plane, number + 1),
        )


def upsert_node_file(conn, warehouse_root, path, expected_prefix=None):
    """Read a canonical node file under the warehouse root and upsert it."""
    warehouse_root = Path(warehouse_root)
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    node = store.parse_node_text(text)
    if path.name != f"{node.id}.md":
        raise FoldError(f"filename {path.name!r} does not match node id {node.id!r}")
    relpath = path.relative_to(warehouse_root)
    if relpath != store.node_relpath(node.id):
        raise FoldError(
            f"node {node.id} is misplaced: found at {relpath.as_posix()!r}, "
            f"canonical path is {store.node_relpath(node.id).as_posix()!r}"
        )
    prefix = parse_id(node.id)[0]
    if expected_prefix is not None and prefix != expected_prefix:
        raise FoldError(
            f"node {node.id} carries prefix {prefix!r}, "
            f"instance prefix is {expected_prefix!r}"
        )
    upsert_node(conn, node, text, relpath.as_posix())
    return node


# ---------------------------------------------------------------------------
# Cold path — reconcile rebuild
# ---------------------------------------------------------------------------

@dataclass
class CarryOver:
    created_at: str
    trace: list = field(default_factory=list)
    antechamber: list = field(default_factory=list)


@dataclass
class RebuildResult:
    node_count: int
    edge_count: int
    carried_trace: int
    carried_antechamber: int
    digest: str


def rebuild(warehouse_root, fresh=False):
    """Reconcile rebuild: fresh index from markdown, atomically swapped in.

    Deterministic by construction (A8): nodes folded in (plane, number)
    order, edges sorted, `meta.created_at` and the trace/antechamber rows
    carried over from the previous index. `fresh=True` is the recovery
    escape hatch for a corrupt previous index — it discards the carried
    operational state (trace is lost, an accepted A8 cost).

    `grants` rows are deliberately NOT carried over (owner decision, B3):
    a continuation grant is fresh owner consent — consent does not survive
    an index rebuild, and re-issuing one is cheap.
    """
    warehouse_root = Path(warehouse_root)
    cfg = config.load_config(warehouse_root)
    index_path = warehouse_root / schema.INDEX_FILENAME
    carried = None
    if index_path.exists() and not fresh:
        carried = _read_carry_over(index_path)

    tmp_path = warehouse_root / (schema.INDEX_FILENAME + REBUILD_SUFFIX)
    for suffix in ("", "-wal", "-shm", "-journal"):
        stale = Path(str(tmp_path) + suffix)
        if stale.exists():
            stale.unlink()  # leftover from a crashed rebuild

    # Built in rollback-journal mode: under WAL, checkpoint bookkeeping bumps
    # the header file-change-counter non-deterministically, which breaks the
    # A8 byte criterion. The switch to WAL is the final canonicalization step.
    schema.create_index(
        tmp_path, cfg.project_prefix, cfg.schema_version,
        created_at=carried.created_at if carried else None,
        wal=False,
    )
    conn = schema.connect(tmp_path)
    try:
        node_count = 0
        for path in _sorted_node_files(warehouse_root):
            upsert_node_file(conn, warehouse_root, path, expected_prefix=cfg.project_prefix)
            node_count += 1
        if carried:
            with conn:
                conn.executemany(
                    "INSERT INTO trace (" + ", ".join(_TRACE_COLUMNS) + ") VALUES ("
                    + ", ".join("?" for _ in _TRACE_COLUMNS) + ")",
                    carried.trace,
                )
                conn.executemany(
                    "INSERT INTO antechamber (" + ", ".join(_ANTECHAMBER_COLUMNS)
                    + ") VALUES (" + ", ".join("?" for _ in _ANTECHAMBER_COLUMNS) + ")",
                    carried.antechamber,
                )
        edge_count = conn.execute("SELECT count(*) FROM edges").fetchone()[0]
        digest = logical_digest(conn)
        # Final canonicalization: one deterministic header write switches the
        # finished file to WAL, the instance's operating mode.
        conn.execute("PRAGMA journal_mode = WAL")
    finally:
        conn.close()

    tmp_path.replace(index_path)
    for suffix in ("-wal", "-shm"):
        leftover = Path(str(index_path) + suffix)
        if leftover.exists():
            leftover.unlink()  # stale WAL of the replaced index
    return RebuildResult(
        node_count=node_count,
        edge_count=edge_count,
        carried_trace=len(carried.trace) if carried else 0,
        carried_antechamber=len(carried.antechamber) if carried else 0,
        digest=digest,
    )


def _read_carry_over(index_path):
    try:
        conn = schema.connect(index_path)
        try:
            created_at = conn.execute(
                "SELECT value FROM meta WHERE key = 'created_at'"
            ).fetchone()[0]
            trace = conn.execute(
                "SELECT " + ", ".join(_TRACE_COLUMNS) + " FROM trace ORDER BY round_id"
            ).fetchall()
            antechamber = conn.execute(
                "SELECT " + ", ".join(_ANTECHAMBER_COLUMNS)
                + " FROM antechamber ORDER BY proposal_key"
            ).fetchall()
        finally:
            conn.close()
    except sqlite3.DatabaseError as exc:
        raise FoldError(
            f"previous index is unreadable ({exc}); re-run reconcile with "
            "fresh=True / --fresh to rebuild without carry-over "
            "(trace and antechamber mirror are lost, A8 accepted cost)"
        ) from exc
    return CarryOver(created_at=created_at, trace=trace, antechamber=antechamber)


def _sorted_node_files(warehouse_root):
    """All canonical node files in deterministic (plane, number) order."""
    paths = []
    for subdir, plane_rank in ((store.NODES_DIR, 0), (store.FLAGS_DIR, 1)):
        directory = Path(warehouse_root) / subdir
        if not directory.is_dir():
            raise FoldError(f"missing warehouse directory: {directory}")
        for path in directory.glob("*.md"):
            try:
                _, _, number = parse_id(path.stem)
            except RobotError as exc:
                raise FoldError(f"file is not a canonical node file: {path} ({exc})") from exc
            paths.append((plane_rank, number, path))
    return [path for _, _, path in sorted(paths, key=lambda t: t[:2])]


# ---------------------------------------------------------------------------
# Canonical logical digest (A8 part 2)
# ---------------------------------------------------------------------------

def logical_digest(conn):
    """Ordered dump-hash of the derived tables + FTS5 integrity check.

    The live index and a fresh rebuild must agree on this digest (A8). The
    FTS index itself is covered structurally: its content equals nodes
    title+body (hashed via the nodes dump) and the integrity check proves
    the index matches that content.
    """
    digest = hashlib.sha256()
    for name, sql in _DIGEST_QUERIES:
        digest.update(name.encode("ascii"))
        for row in conn.execute(sql):
            digest.update(repr(row).encode("utf-8"))
    try:
        conn.execute("INSERT INTO nodes_fts (nodes_fts) VALUES ('integrity-check')")
    except sqlite3.DatabaseError as exc:
        raise FoldError(f"FTS5 index diverges from node content: {exc}") from exc
    finally:
        # The integrity-check command is INSERT-shaped, so python sqlite3
        # opens an implicit transaction for it; close it so the rebuild's
        # final journal_mode switch is not blocked by an open transaction.
        conn.commit()
    return digest.hexdigest()


def logical_digest_of(index_path):
    conn = schema.connect(index_path)
    try:
        return logical_digest(conn)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Divergence check (cheap; per-file granularity)
# ---------------------------------------------------------------------------

@dataclass
class DivergenceReport:
    index_missing: bool = False
    missing_in_index: list = field(default_factory=list)   # ids on disk, not in index
    missing_in_markdown: list = field(default_factory=list)  # ids in index, no file
    hash_mismatch: list = field(default_factory=list)      # ids whose file changed
    misplaced: list = field(default_factory=list)          # (id, found-at) wrong dir
    unreadable: list = field(default_factory=list)         # (path, reason)
    counter_behind: list = field(default_factory=list)     # (plane, next_value, markdown max)
    fts_corrupt: bool = False

    @property
    def clean(self):
        return not (
            self.index_missing or self.missing_in_index or self.missing_in_markdown
            or self.hash_mismatch or self.misplaced or self.unreadable
            or self.counter_behind or self.fts_corrupt
        )

    def lines(self):
        if self.clean:
            return ["clean: markdown and index agree"]
        out = []
        if self.index_missing:
            out.append("index file is missing — run reconcile to rebuild it")
            return out
        for node_id in self.missing_in_index:
            out.append(f"missing in index: {node_id} (file exists, no index row)")
        for node_id in self.missing_in_markdown:
            out.append(f"missing in markdown: {node_id} (index row exists, no file)")
        for node_id in self.hash_mismatch:
            out.append(f"hash mismatch: {node_id} (file content diverged from index)")
        for node_id, found_at in self.misplaced:
            out.append(f"misplaced: {node_id} found at {found_at}")
        for path, reason in self.unreadable:
            out.append(f"unreadable: {path} ({reason})")
        for plane, next_value, max_number in self.counter_behind:
            out.append(
                f"counter behind: plane {plane!r} next_value={next_value}, "
                f"markdown max={max_number}"
            )
        if self.fts_corrupt:
            out.append("FTS5 index diverges from node content")
        return out


def check(warehouse_root):
    """Cheap divergence check: per-file content-hash + count, markdown vs index."""
    warehouse_root = Path(warehouse_root)
    cfg = config.load_config(warehouse_root)
    report = DivergenceReport()
    index_path = warehouse_root / schema.INDEX_FILENAME
    if not index_path.exists():
        report.index_missing = True
        return report

    on_disk = {}  # id -> content hash
    max_number = {KNOWLEDGE_PLANE: 0, AUDIT_PLANE: 0}
    for subdir in (store.NODES_DIR, store.FLAGS_DIR):
        directory = warehouse_root / subdir
        if not directory.is_dir():
            report.unreadable.append((subdir, "warehouse directory missing"))
            continue
        for path in sorted(directory.glob("*.md")):
            relpath = path.relative_to(warehouse_root)
            try:
                text = path.read_text(encoding="utf-8")
                node = store.parse_node_text(text)
                if path.name != f"{node.id}.md":
                    raise FoldError(
                        f"filename does not match node id {node.id!r}"
                    )
                prefix, plane, number = parse_id(node.id)
                if prefix != cfg.project_prefix:
                    raise FoldError(
                        f"prefix {prefix!r} is foreign to instance prefix "
                        f"{cfg.project_prefix!r}"
                    )
            except RobotError as exc:
                report.unreadable.append((relpath.as_posix(), str(exc)))
                continue
            if relpath != store.node_relpath(node.id):
                report.misplaced.append((node.id, relpath.as_posix()))
                continue
            on_disk[node.id] = store.content_hash(text)
            max_number[plane] = max(max_number[plane], number)

    conn = schema.connect(index_path)
    try:
        in_index = dict(conn.execute("SELECT id, content_hash FROM nodes"))
        counters = dict(conn.execute("SELECT plane, next_value FROM id_counter"))
        try:
            conn.execute("INSERT INTO nodes_fts (nodes_fts) VALUES ('integrity-check')")
        except sqlite3.DatabaseError:
            report.fts_corrupt = True
    finally:
        conn.close()

    report.missing_in_index = sorted(set(on_disk) - set(in_index))
    report.missing_in_markdown = sorted(set(in_index) - set(on_disk))
    report.hash_mismatch = sorted(
        node_id for node_id in set(on_disk) & set(in_index)
        if on_disk[node_id] != in_index[node_id]
    )
    for plane in (KNOWLEDGE_PLANE, AUDIT_PLANE):
        next_value = counters.get(plane, 0)
        if next_value < max_number[plane] + 1:
            report.counter_behind.append((plane, next_value, max_number[plane]))
    return report
