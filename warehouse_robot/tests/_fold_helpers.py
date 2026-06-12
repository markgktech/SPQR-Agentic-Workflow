"""Shared helpers for the B2 fold/reconcile tests.

Every helper works against a disposable instance under the system tmp
directory (A4 discipline) — the caller owns the TemporaryDirectory.
Fixtures are copied in sorted-glob order (demo-n1, demo-n10, demo-n11, ...),
which deliberately differs from the rebuild's (plane, number) order, so the
live-vs-rebuild digest tests exercise order independence for real.
"""

import contextlib
import hashlib
import io
import shutil
from pathlib import Path

from warehouse_robot import cli, fold, schema

FIXTURES_ROOT = Path(__file__).resolve().parent.parent / "fixtures"
FIXTURE_PREFIX = "demo"


def quiet_cli(argv):
    """Run the CLI quietly; return (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


def init_instance(parent, prefix=FIXTURE_PREFIX):
    """`init` a disposable instance; return the warehouse root."""
    wroot = Path(parent) / "project_memory" / "warehouse"
    code, _, err = quiet_cli(["init", "--warehouse-root", str(wroot), "--prefix", prefix])
    assert code == 0, err
    return wroot


def copy_fixtures(wroot):
    """Copy the versioned fixture files into the instance; return the copies."""
    copies = []
    for sub in ("nodes", "flags"):
        for src in sorted((FIXTURES_ROOT / sub).glob("*.md")):
            dst = Path(wroot) / sub / src.name
            shutil.copyfile(src, dst)
            copies.append(dst)
    return copies


def fold_fixtures(wroot):
    """Copy fixtures in and fold each incrementally (the hot path)."""
    copies = copy_fixtures(wroot)
    conn = schema.connect(Path(wroot) / schema.INDEX_FILENAME)
    try:
        for path in copies:
            fold.upsert_node_file(conn, wroot, path, expected_prefix=FIXTURE_PREFIX)
    finally:
        conn.close()
    return copies


def index_path(wroot):
    return Path(wroot) / schema.INDEX_FILENAME


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def query_one(wroot, sql, params=()):
    conn = schema.connect(index_path(wroot))
    try:
        return conn.execute(sql, params).fetchone()
    finally:
        conn.close()


def query_all(wroot, sql, params=()):
    conn = schema.connect(index_path(wroot))
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def execute(wroot, sql, params=()):
    conn = schema.connect(index_path(wroot))
    try:
        with conn:
            conn.execute(sql, params)
    finally:
        conn.close()
