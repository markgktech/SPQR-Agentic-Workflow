"""Per-call CLI entry point (G1: per-call process; G2: CLI-first binding).

The warehouse root is a mandatory parameter on every command — there is no
default and no hardcoded path (A4, B1 hard requirement). The robot writes
files; it never runs git (G3).

Usage:
    python3 -m warehouse_robot init --warehouse-root PATH --prefix PREFIX
                                    [--antechamber-root PATH]
    python3 -m warehouse_robot check --warehouse-root PATH
    python3 -m warehouse_robot reconcile --warehouse-root PATH [--fresh]

The incremental upsert (the fold's hot path) has NO CLI command by design —
it is a library API consumed by the B4 serializing gate; a public fold
command would open a gate-bypassing write path.
"""

import argparse
import sys
from pathlib import Path

from . import config, fold, schema, store
from .errors import ConfigError, RobotError
from .ids import PREFIX_RE

INSTANCE_GITIGNORE = (
    "# Derived index — disposable projection of the markdown truth (S7). Never versioned.\n"
    "index.sqlite\n"
    "index.sqlite-wal\n"
    "index.sqlite-shm\n"
)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="warehouse_robot",
        description="Deterministic storage robot for the SPQR knowledge warehouse.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser(
        "init", help="create an empty warehouse instance at the given root"
    )
    p_init.add_argument(
        "--warehouse-root",
        required=True,
        help="warehouse root directory (mandatory; no default exists)",
    )
    p_init.add_argument(
        "--prefix",
        required=True,
        help="project prefix for node IDs, e.g. 'food' ([a-z][a-z0-9]*)",
    )
    p_init.add_argument(
        "--antechamber-root",
        default=None,
        help="antechamber directory (default: 'antechamber' sibling of the warehouse root, A3)",
    )
    p_init.set_defaults(func=cmd_init)

    p_check = subparsers.add_parser(
        "check", help="cheap divergence check: markdown vs derived index, per file"
    )
    p_check.add_argument(
        "--warehouse-root",
        required=True,
        help="warehouse root directory (mandatory; no default exists)",
    )
    p_check.set_defaults(func=cmd_check)

    p_reconcile = subparsers.add_parser(
        "reconcile",
        help="full rebuild of the derived index from markdown (cold reconcile path)",
    )
    p_reconcile.add_argument(
        "--warehouse-root",
        required=True,
        help="warehouse root directory (mandatory; no default exists)",
    )
    p_reconcile.add_argument(
        "--fresh",
        action="store_true",
        help="discard trace/antechamber carry-over (recovery from a corrupt "
        "index; the trace is lost — A8 accepted cost)",
    )
    p_reconcile.set_defaults(func=cmd_reconcile)
    return parser


def cmd_init(args):
    if not PREFIX_RE.match(args.prefix):
        raise ConfigError(f"invalid project prefix {args.prefix!r}: must match [a-z][a-z0-9]*")
    schema.check_fts5()

    warehouse_root = Path(args.warehouse_root)
    manifest_path = config.config_path(warehouse_root)
    index_path = warehouse_root / schema.INDEX_FILENAME
    if manifest_path.exists() or index_path.exists():
        raise ConfigError(
            f"warehouse root already initialised: {warehouse_root} — init never "
            "overwrites an instance; a full reset deletes the warehouse root "
            "and re-runs init"
        )

    antechamber_root = (
        Path(args.antechamber_root)
        if args.antechamber_root
        else warehouse_root.parent / "antechamber"
    )
    for directory in (
        warehouse_root / store.NODES_DIR,
        warehouse_root / store.FLAGS_DIR,
        antechamber_root,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    config.save_config(
        warehouse_root,
        config.WarehouseConfig(project_prefix=args.prefix, schema_version=config.SCHEMA_VERSION),
    )
    (warehouse_root / ".gitignore").write_text(INSTANCE_GITIGNORE, encoding="utf-8")
    schema.create_index(index_path, args.prefix, config.SCHEMA_VERSION)

    print("initialised warehouse instance")
    print(f"  warehouse root : {warehouse_root}")
    print(f"  antechamber    : {antechamber_root}")
    print(f"  project prefix : {args.prefix}")
    print(f"  schema version : {config.SCHEMA_VERSION}")
    print(f"  derived index  : {index_path} (disposable, gitignored)")


def cmd_check(args):
    report = fold.check(Path(args.warehouse_root))
    for line in report.lines():
        print(line)
    return 0 if report.clean else 1


def cmd_reconcile(args):
    result = fold.rebuild(Path(args.warehouse_root), fresh=args.fresh)
    print("reconcile rebuild complete")
    print(f"  nodes folded        : {result.node_count}")
    print(f"  edges folded        : {result.edge_count}")
    print(f"  trace rows carried  : {result.carried_trace}")
    print(f"  antechamber carried : {result.carried_antechamber}")
    print(f"  logical digest      : {result.digest}")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except RobotError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0 if result is None else result
