"""SQLite DDL for the derived index.

S7: markdown is the source of truth; this index is a disposable, rebuildable
projection. DDL changes in later tickets are cheap by design — a reconcile
rebuild (B2) recreates the file from markdown, so no migration machinery is
needed for the index itself.

Tables:
- meta             — schema_version / project_prefix / created_at
- nodes            — both planes ('n' knowledge, 'f' audit/flag), one row per node
- edges            — directed typed edges; no inverse edges (S3)
- nodes_fts        — FTS5 external-content table over title+body (BM25 finder, S7)
- id_counter       — per-plane allocation cache; canonical source is the
                     markdown (max+1 on rebuild, S7); consumed by the B4 gate
- antechamber      — index mirror of pending proposals (S6 state machine;
                     'revise' is not a stored state — it re-enters at 'proposed')
- trace            — intent/verdict bracket per query round (S4); written by
                     the B3 query path; carried over verbatim on rebuild (A8)
- grants           — one-shot continuation grants (S4 consent-gate, B3);
                     deliberately NOT carried over on reconcile rebuild —
                     a grant is fresh owner consent, re-issuing is cheap

Views (derived status — never stored, S3/S6):
- v_effective_status — knowledge plane; 'superseded' derived from an incoming
                       supersedes edge ('retired' wins over 'superseded')
- v_flag_status      — audit plane; 'resolved' derived from an incoming
                       resolves edge, otherwise 'open'
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .errors import SchemaError
from .ids import AUDIT_PLANE, KNOWLEDGE_PLANE

INDEX_FILENAME = "index.sqlite"

DDL = [
    """
    CREATE TABLE meta (
      key   TEXT PRIMARY KEY,
      value TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE nodes (
      id             TEXT PRIMARY KEY,
      plane          TEXT NOT NULL CHECK (plane IN ('n', 'f')),
      kind           TEXT NOT NULL CHECK (kind IN ('decision', 'constraint', 'lesson', 'flag')),
      status         TEXT NOT NULL CHECK (status IN ('active', 'retired')),
      title          TEXT NOT NULL,
      scope          TEXT,
      verdict        TEXT CHECK (verdict IN ('GREEN', 'YELLOW', 'RED')),
      flag_type      TEXT,
      origin         TEXT NOT NULL CHECK (origin IN ('decided', 'inherited', 'observed')),
      timestamp      TEXT NOT NULL,
      ticket         TEXT,
      agent          TEXT,
      source         TEXT,
      schema_version INTEGER NOT NULL,
      body           TEXT NOT NULL,
      content_hash   TEXT NOT NULL,
      file_path      TEXT NOT NULL,
      CHECK ((plane = 'f') = (kind = 'flag'))
    )
    """,
    "CREATE INDEX idx_nodes_filter ON nodes (plane, kind, scope)",
    "CREATE INDEX idx_nodes_status ON nodes (status)",
    """
    CREATE TABLE edges (
      src    TEXT NOT NULL REFERENCES nodes (id),
      type   TEXT NOT NULL CHECK (type IN
               ('supersedes', 'derived-from', 'constrains', 'about',
                'relates-to', 'flags', 'resolves')),
      target TEXT NOT NULL,
      PRIMARY KEY (src, type, target)
    ) WITHOUT ROWID
    """,
    "CREATE INDEX idx_edges_target ON edges (target, type)",
    """
    CREATE VIRTUAL TABLE nodes_fts USING fts5 (
      title,
      body,
      content='nodes',
      content_rowid='rowid'
    )
    """,
    """
    CREATE TABLE id_counter (
      plane      TEXT PRIMARY KEY CHECK (plane IN ('n', 'f')),
      next_value INTEGER NOT NULL CHECK (next_value >= 1)
    ) WITHOUT ROWID
    """,
    """
    CREATE TABLE antechamber (
      proposal_key TEXT PRIMARY KEY,
      state        TEXT NOT NULL CHECK (state IN
                     ('proposed', 'rejected-malformed', 'validated',
                      'pending-senate', 'auto-ingested', 'ingested', 'rejected')),
      ticket       TEXT NOT NULL,
      agent        TEXT NOT NULL,
      created_at   TEXT NOT NULL,
      updated_at   TEXT NOT NULL,
      content_hash TEXT NOT NULL,
      file_path    TEXT NOT NULL,
      node_id      TEXT
    )
    """,
    """
    CREATE TABLE trace (
      round_id     INTEGER PRIMARY KEY AUTOINCREMENT,
      ts           TEXT NOT NULL,
      session_id   TEXT NOT NULL,
      ticket       TEXT,
      agent        TEXT,
      archetype    TEXT,
      verb         TEXT NOT NULL CHECK (verb IN ('open_scope', 'find', 'fetch', 'traverse')),
      intent       TEXT NOT NULL,
      params       TEXT,
      result_count INTEGER,
      result_ids   TEXT,
      verdict      TEXT CHECK (verdict IN
                     ('FOUND-ENOUGH', 'WRONG-ENTRY', 'INSUFFICIENT-TRAVERSE',
                      'ABSENT', 'FOUND-UNLINKED')),
      budget       TEXT
    )
    """,
    "CREATE INDEX idx_trace_session ON trace (session_id)",
    """
    CREATE TABLE grants (
      grant_id             INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id           TEXT NOT NULL,
      created_at           TEXT NOT NULL,
      consumed_after_round INTEGER
    )
    """,
    "CREATE INDEX idx_grants_session ON grants (session_id)",
    """
    CREATE VIEW v_effective_status AS
    SELECT n.id,
           CASE
             WHEN n.status = 'retired' THEN 'retired'
             WHEN EXISTS (SELECT 1 FROM edges e
                          WHERE e.target = n.id AND e.type = 'supersedes')
               THEN 'superseded'
             ELSE n.status
           END AS effective_status
    FROM nodes n
    WHERE n.plane = 'n'
    """,
    """
    CREATE VIEW v_flag_status AS
    SELECT n.id,
           CASE
             WHEN EXISTS (SELECT 1 FROM edges e
                          WHERE e.target = n.id AND e.type = 'resolves')
               THEN 'resolved'
             ELSE 'open'
           END AS flag_status
    FROM nodes n
    WHERE n.plane = 'f'
    """,
]


def check_fts5():
    """Probe the runtime SQLite build for FTS5; hard-fail if it is missing.

    Owner condition on B1 question #1: init must verify FTS5 availability at
    runtime and refuse to create an instance without it.
    """
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE VIRTUAL TABLE fts5_probe USING fts5 (probe)")
    except sqlite3.OperationalError as exc:
        raise SchemaError(
            "this SQLite build has no FTS5 support; the warehouse index "
            f"cannot be created (probe failed with: {exc})"
        ) from exc
    finally:
        conn.close()


def connect(db_path):
    """Open the index with per-connection pragmas applied."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_index(db_path, project_prefix, schema_version, created_at=None, wal=True):
    """Create and seed a fresh index file; refuses to touch an existing one.

    `created_at` defaults to now; the B2 reconcile rebuild passes the value
    carried over from the previous index so that successive rebuilds stay
    byte-identical (A8 determinism criterion).

    `wal=False` creates the index in rollback-journal mode: the B2 rebuild
    builds its tmp index that way because WAL checkpoint bookkeeping bumps
    the header file-change-counter non-deterministically; the rebuild
    switches to WAL as its final canonicalization step before the rename.
    """
    db_path = Path(db_path)
    if db_path.exists():
        raise SchemaError(f"index already exists: {db_path} (the index is never overwritten in place)")
    check_fts5()
    conn = connect(db_path)
    try:
        if wal:
            conn.execute("PRAGMA journal_mode = WAL")
        with conn:
            for statement in DDL:
                conn.execute(statement)
            if created_at is None:
                created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            conn.executemany(
                "INSERT INTO meta (key, value) VALUES (?, ?)",
                [
                    ("schema_version", str(schema_version)),
                    ("project_prefix", project_prefix),
                    ("created_at", created_at),
                ],
            )
            conn.executemany(
                "INSERT INTO id_counter (plane, next_value) VALUES (?, 1)",
                [(KNOWLEDGE_PLANE,), (AUDIT_PLANE,)],
            )
    finally:
        conn.close()
