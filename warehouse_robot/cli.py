"""Per-call CLI entry point (G1: per-call process; G2: CLI-first binding).

The warehouse root is a mandatory parameter on every command — there is no
default and no hardcoded path (A4, B1 hard requirement). The robot writes
files; it never runs git (G3).

Usage:
    python3 -m warehouse_robot init --warehouse-root PATH --prefix PREFIX
                                    [--antechamber-root PATH]
    python3 -m warehouse_robot check --warehouse-root PATH
    python3 -m warehouse_robot reconcile --warehouse-root PATH [--fresh]

    # B3 query verbs (S4 contract; JSON on stdout, agents are the consumer):
    python3 -m warehouse_robot open-scope --warehouse-root PATH
        --archetype A --session S --intent "..." [--scope X] [--kind K]
        [--include-inactive] [--ticket T] [--agent NAME] [--tighten K=V]...
    python3 -m warehouse_robot find ... --text "..." [--scope X] [--kind K]
        [--top-n N] [--include-inactive]
    python3 -m warehouse_robot fetch ... --ids id1,id2
    python3 -m warehouse_robot traverse ... --id ID --edge-type T [--depth N]
    python3 -m warehouse_robot verdict --warehouse-root PATH --session S
        --verdict V
    python3 -m warehouse_robot grant --warehouse-root PATH --session S

Exit codes: 0 success · 1 non-fatal condition (divergent `check`, or a
budget-exhausted query — the escalation packet is printed as JSON) ·
2 error (protocol violation, policy DENY, malformed input).

Every query verb runs the cheap divergence check first and warns on stderr
if the index lags the markdown — it never refuses for it (B2 open question
#1, owner-approved): a stale index degrades a read, the reconcile heals it.

The incremental upsert (the fold's hot path) has NO CLI command by design —
it is a library API consumed by the B4 serializing gate; a public fold
command would open a gate-bypassing write path.
"""

import argparse
import json
import sys
from pathlib import Path

from . import config, fold, query, schema, store
from .errors import BudgetExhausted, ConfigError, ProtocolError, RobotError
from .ids import PREFIX_RE
from .policy import ARCHETYPES, VERDICTS, policy_for, tightened

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

    def query_verb(name, help_text):
        p = subparsers.add_parser(name, help=help_text)
        p.add_argument("--warehouse-root", required=True,
                       help="warehouse root directory (mandatory; no default exists)")
        p.add_argument("--archetype", required=True, choices=ARCHETYPES,
                       help="self-declared archetype (G8) — logged in the trace")
        p.add_argument("--session", required=True,
                       help="self-declared query-session id — the budget accounting unit")
        p.add_argument("--intent", required=True,
                       help="what this round is looking for (K9; logged in the trace)")
        p.add_argument("--ticket", default=None, help="originating ticket (trace)")
        p.add_argument("--agent", default=None, help="calling agent name (trace)")
        p.add_argument("--tighten", action="append", default=[], metavar="DIAL=N",
                       help="tighten a budget dial for this call (e.g. "
                       "body_fetch_ceiling=2); loosening is refused — that is "
                       "what a continuation grant is for")
        return p

    p_open = query_verb("open-scope",
                        "deterministic scope/kind feed: complete skeleton slice, "
                        "facets on overflow (S4)")
    p_open.add_argument("--scope", default=None, help="scope slice to open")
    p_open.add_argument("--kind", default=None,
                        help="kind filter; 'flag' addresses the audit plane")
    p_open.add_argument("--include-inactive", action="store_true",
                        help="also show retired/superseded (resolved) nodes")
    p_open.set_defaults(func=cmd_open_scope)

    p_find = query_verb("find",
                        "FTS5/BM25 finder side-door: ranked skeleton top-N")
    p_find.add_argument("--text", required=True, help="search text")
    p_find.add_argument("--kind", default=None,
                        help="kind filter; 'flag' addresses the audit plane")
    p_find.add_argument("--scope", default=None, help="scope filter")
    p_find.add_argument("--top-n", type=int, default=None,
                        help=f"ranked result bound (default {query.DEFAULT_TOP_N})")
    p_find.add_argument("--include-inactive", action="store_true",
                        help="also show retired/superseded (resolved) nodes")
    p_find.set_defaults(func=cmd_find)

    p_fetch = query_verb("fetch",
                         "bodies + edge TOC for explicitly selected ids")
    p_fetch.add_argument("--ids", required=True,
                         help="comma-separated node ids to fetch")
    p_fetch.set_defaults(func=cmd_fetch)

    p_traverse = query_verb("traverse",
                            "bounded typed-edge neighborhood expansion")
    p_traverse.add_argument("--id", required=True, dest="node_id",
                            help="origin node id")
    p_traverse.add_argument("--edge-type", required=True,
                            help="edge type to follow (both directions)")
    p_traverse.add_argument("--depth", type=int, default=1,
                            help="expansion depth (policy-capped)")
    p_traverse.set_defaults(func=cmd_traverse)

    p_verdict = subparsers.add_parser(
        "verdict", help="close the session's open round (the bracket's second half)"
    )
    p_verdict.add_argument("--warehouse-root", required=True,
                           help="warehouse root directory (mandatory; no default exists)")
    p_verdict.add_argument("--session", required=True, help="query-session id")
    p_verdict.add_argument("--verdict", required=True, choices=VERDICTS,
                           dest="verdict_value", help="per-round verdict (S4)")
    p_verdict.set_defaults(func=cmd_verdict)

    p_grant = subparsers.add_parser(
        "grant", help="owner-issued one-shot continuation grant (consent-gate)"
    )
    p_grant.add_argument("--warehouse-root", required=True,
                         help="warehouse root directory (mandatory; no default exists)")
    p_grant.add_argument("--session", required=True,
                         help="session the grant applies to")
    p_grant.set_defaults(func=cmd_grant)
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


def _policy_from_args(args):
    """Resolve the archetype policy, applying --tighten overrides (if any)."""
    if not args.tighten:
        return None  # the verb resolves the default itself
    overrides = {}
    for item in args.tighten:
        name, eq, value = item.partition("=")
        if not eq or not value.lstrip("-").isdigit():
            raise ProtocolError(
                f"--tighten expects DIAL=INTEGER, got {item!r}"
            )
        overrides[name.replace("-", "_")] = int(value)
    return tightened(policy_for(args.archetype), **overrides)


def _warn_if_divergent(warehouse_root):
    """Cheap check-on-open: warn on stderr, never refuse (B2 #1, owner-approved)."""
    try:
        report = fold.check(Path(warehouse_root))
    except RobotError:
        return  # the verb itself raises the real, precise error
    if not report.clean:
        findings = report.lines()
        print(
            f"warning: index diverges from markdown ({len(findings)} finding(s)) "
            "— results may be stale; run reconcile",
            file=sys.stderr,
        )


def _common_kwargs(args):
    return dict(ticket=args.ticket, agent=args.agent,
                policy=_policy_from_args(args))


def _emit(response):
    print(json.dumps(response, indent=2))


def cmd_open_scope(args):
    _warn_if_divergent(args.warehouse_root)
    _emit(query.open_scope(
        args.warehouse_root, args.archetype, args.session, args.intent,
        scope=args.scope, kind=args.kind,
        include_inactive=args.include_inactive, **_common_kwargs(args),
    ))


def cmd_find(args):
    _warn_if_divergent(args.warehouse_root)
    _emit(query.find(
        args.warehouse_root, args.archetype, args.session, args.intent,
        args.text, kind=args.kind, scope=args.scope, top_n=args.top_n,
        include_inactive=args.include_inactive, **_common_kwargs(args),
    ))


def cmd_fetch(args):
    _warn_if_divergent(args.warehouse_root)
    ids = [part.strip() for part in args.ids.split(",") if part.strip()]
    _emit(query.fetch(
        args.warehouse_root, args.archetype, args.session, args.intent,
        ids, **_common_kwargs(args),
    ))


def cmd_traverse(args):
    _warn_if_divergent(args.warehouse_root)
    _emit(query.traverse(
        args.warehouse_root, args.archetype, args.session, args.intent,
        args.node_id, args.edge_type, depth=args.depth, **_common_kwargs(args),
    ))


def cmd_verdict(args):
    _emit(query.verdict(args.warehouse_root, args.session, args.verdict_value))


def cmd_grant(args):
    _emit(query.issue_grant(args.warehouse_root, args.session))


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
    except BudgetExhausted as exc:
        # Exit 1 = halt-and-escalate, never a silent fail (S4): the packet
        # is what the agent must surface to the owner for a grant decision.
        print(json.dumps(
            {"error": "budget-exhausted", "message": str(exc),
             "packet": exc.packet},
            indent=2,
        ))
        return 1
    except RobotError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0 if result is None else result
