"""Per-call CLI entry point (G1: per-call process; G2: CLI-first binding).

The warehouse root is a mandatory parameter on every command — there is no
default and no hardcoded path (A4, B1 hard requirement). The robot writes
files; it never runs git (G3).

Usage:
    python3 -m warehouse_robot init --warehouse-root PATH --prefix PREFIX
                                    [--antechamber-root PATH]
    python3 -m warehouse_robot check --warehouse-root PATH
    python3 -m warehouse_robot reconcile --warehouse-root PATH [--fresh]
    python3 -m warehouse_robot audit --warehouse-root PATH

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

from . import audit, config, fold, query, schema, store, write_gate
from .errors import (
    BudgetExhausted, ConfigError, ProtocolError, RevisionLimitReached, RobotError,
)
from .ids import PREFIX_RE
from .policy import ARCHETYPES, VERDICTS, policy_for, tightened

# Production default (A13): a CANONICAL instance VERSIONS its node + antechamber
# markdown (it is un-ingested truth); only the derived index is gitignored.
INSTANCE_GITIGNORE = (
    "# Derived index — disposable projection of the markdown truth (S7). Never versioned.\n"
    "index.sqlite\n"
    "index.sqlite-wal\n"
    "index.sqlite-shm\n"
)

# Disposable TEST instance only (A12 ↔ A13 reconciled): node + antechamber
# markdown are test data and must never reach git. A12's "instance .gitignore
# covers node + antechamber markdown" is scoped to throwaway instances; A13
# keeps the canonical instance versioning them. Selected by `init --disposable`.
DISPOSABLE_GITIGNORE = INSTANCE_GITIGNORE + (
    "\n# Disposable test instance (A12): never commit test node/antechamber markdown.\n"
    "nodes/\n"
    "flags/\n"
)
DISPOSABLE_ANTECHAMBER_GITIGNORE = (
    "# Disposable test antechamber (A12): never commit test proposals.\n"
    "*\n"
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
    p_init.add_argument(
        "--disposable",
        action="store_true",
        help="mark this a throwaway TEST instance: gitignore node + antechamber "
        "markdown too (A12). A canonical instance versions them (A13) — never "
        "pass this for a real warehouse.",
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
    p_check.add_argument(
        "--antechamber-root", default=None,
        help="antechamber directory (default: 'antechamber' sibling, A3)",
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

    # --- B4 write path ---
    def write_cmd(name, help_text):
        p = subparsers.add_parser(name, help=help_text)
        p.add_argument("--warehouse-root", required=True,
                       help="warehouse root directory (mandatory; no default exists)")
        p.add_argument("--antechamber-root", default=None,
                       help="antechamber directory (default: 'antechamber' sibling, A3)")
        return p

    p_propose = write_cmd("propose",
                          "submit a proposal: hard-gate it, write it to the "
                          "antechamber, escalate to the Senate (S6)")
    p_propose.add_argument("--ticket", required=True,
                           help="self-declared submitter ticket (binding, L5)")
    p_propose.add_argument("--agent", required=True,
                           help="self-declared submitter agent (binding, L5)")
    p_propose.add_argument("--file", required=True, dest="proposal_file",
                           help="path to the proposal markdown, or '-' for stdin")
    p_propose.set_defaults(func=cmd_propose)

    p_revise = write_cmd("revise",
                         "resubmit revised content for a proposal the Senate "
                         "sent back (re-enters at proposed, A15)")
    p_revise.add_argument("--proposal-key", required=True, dest="proposal_key",
                          help="the proposal to revise, e.g. food-p3")
    p_revise.add_argument("--file", required=True, dest="proposal_file",
                          help="path to the revised proposal markdown, or '-' for stdin")
    p_revise.set_defaults(func=cmd_revise)

    p_resolve = write_cmd("resolve",
                          "apply a Senate verdict to a pending proposal "
                          "(robot side; the Senate wake is SAW-31)")
    p_resolve.add_argument("--proposal-key", required=True, dest="proposal_key",
                           help="the pending proposal, e.g. food-p3")
    p_resolve.add_argument("--verdict", required=True, choices=write_gate.VERDICTS,
                           dest="proposal_verdict",
                           help="ingested | rejected | revise (S6)")
    p_resolve.set_defaults(func=cmd_resolve)

    p_arecon = write_cmd("reconcile-antechamber",
                         "re-derive the antechamber mirror from the antechamber "
                         "dir (recovery after index loss, L4)")
    p_arecon.set_defaults(func=cmd_reconcile_antechamber)

    # --- list-pending (read-only antechamber listing; the Senate-wake backing) ---
    p_list = subparsers.add_parser(
        "list-pending",
        help="read-only list of live antechamber proposals (the Senate-wake's "
        "backing, SAW-31); --state filters to one lifecycle state",
    )
    p_list.add_argument("--warehouse-root", required=True,
                        help="warehouse root directory (mandatory; no default exists)")
    p_list.add_argument("--antechamber-root", default=None,
                        help="antechamber directory (default: 'antechamber' sibling, A3)")
    p_list.add_argument("--state", default=None,
                        help="filter to exactly one lifecycle state, e.g. "
                        "pending-senate (default: the live queue, non-terminal)")
    p_list.set_defaults(func=cmd_list_pending)

    # --- B5 audit ---
    p_audit = subparsers.add_parser(
        "audit",
        help="run the deterministic graph-structural tripwires (orphan / "
        "relates-to overuse / missing recommended edge); flag-only, never "
        "mutates a target (S6 Cluster B)",
    )
    p_audit.add_argument("--warehouse-root", required=True,
                         help="warehouse root directory (mandatory; no default exists)")
    p_audit.set_defaults(func=cmd_audit)
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
    gitignore = DISPOSABLE_GITIGNORE if args.disposable else INSTANCE_GITIGNORE
    (warehouse_root / ".gitignore").write_text(gitignore, encoding="utf-8")
    if args.disposable:
        (antechamber_root / ".gitignore").write_text(
            DISPOSABLE_ANTECHAMBER_GITIGNORE, encoding="utf-8"
        )
    schema.create_index(index_path, args.prefix, config.SCHEMA_VERSION)

    print("initialised warehouse instance")
    print(f"  warehouse root : {warehouse_root}")
    print(f"  antechamber    : {antechamber_root}")
    print(f"  project prefix : {args.prefix}")
    print(f"  schema version : {config.SCHEMA_VERSION}")
    print(f"  derived index  : {index_path} (disposable, gitignored)")


def _antechamber_root(args):
    """Resolve the antechamber dir: explicit override, else the A3 sibling
    (which equals the canonical project_memory/ layout — no manifest field
    needed for the default)."""
    if args.antechamber_root:
        return Path(args.antechamber_root)
    return Path(args.warehouse_root).parent / "antechamber"


def cmd_check(args):
    report = fold.check(Path(args.warehouse_root))
    for line in report.lines():
        print(line)
    ante = write_gate.check_antechamber(Path(args.warehouse_root), _antechamber_root(args))
    for line in ante.lines():
        print(f"antechamber: {line}")
    return 0 if (report.clean and ante.clean) else 1


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


def _read_proposal_text(args):
    if args.proposal_file == "-":
        return sys.stdin.read()
    return Path(args.proposal_file).read_text(encoding="utf-8")


# Exit 1 = a recorded REJECTION (the gate did its job; not a robot fault),
# the write-path analogue of B3's budget-refusal exit 1.
_REJECTED_STATES = (write_gate.STATE_REJECTED_MALFORMED, write_gate.STATE_REJECTED)


def cmd_propose(args):
    result = write_gate.propose(
        Path(args.warehouse_root), _antechamber_root(args),
        _read_proposal_text(args), args.ticket, args.agent,
    )
    _emit(result)
    return 1 if result["state"] in _REJECTED_STATES else 0


def cmd_revise(args):
    result = write_gate.revise(
        Path(args.warehouse_root), _antechamber_root(args),
        args.proposal_key, _read_proposal_text(args),
    )
    _emit(result)
    return 1 if result["state"] in _REJECTED_STATES else 0


def cmd_resolve(args):
    result = write_gate.resolve(
        Path(args.warehouse_root), _antechamber_root(args),
        args.proposal_key, args.proposal_verdict,
    )
    _emit(result)
    return 1 if result["state"] in _REJECTED_STATES else 0


def cmd_reconcile_antechamber(args):
    rebuilt = write_gate.reconcile_antechamber(
        Path(args.warehouse_root), _antechamber_root(args)
    )
    print(f"antechamber mirror re-derived: {rebuilt} proposal(s)")


def cmd_list_pending(args):
    # Read-only: list the live antechamber queue (or one --state). A list, even
    # empty, is success (exit 0); an uninitialised root raises a RobotError that
    # main() turns into exit 2.
    pending = write_gate.list_pending(
        Path(args.warehouse_root), _antechamber_root(args), state=args.state
    )
    _emit({"verb": "list-pending", "count": len(pending), "pending": pending})
    return 0


def cmd_audit(args):
    # Like the query verbs, warn (never refuse) if the index lags the markdown:
    # the audit reads the derived projection, and a stale read is degraded, not
    # dangerous (B2 #1). The audit then emits any new flags and reports.
    _warn_if_divergent(args.warehouse_root)
    result = audit.audit(Path(args.warehouse_root))
    _emit(result)
    # Exit 1 = open flags exist (findings present) — the audit analogue of a
    # divergent `check`; exit 0 = a clean graph. Emission itself is a normal,
    # idempotent success, so the code reflects the standing condition, not the
    # act of writing.
    return 1 if result["open_flag_count"] else 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except RevisionLimitReached as exc:
        # Exit 1 = halt-and-escalate (S4/A15): the packet is what the agent
        # surfaces to the owner, mirroring the budget consent-gate.
        print(json.dumps(
            {"error": "revise-limit-reached", "message": str(exc),
             "packet": exc.packet},
            indent=2,
        ))
        return 1
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
