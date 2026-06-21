"""The write gate — the only legal way knowledge ENTERS the warehouse.

Session 6 Cluster A, ticket B4. Two-stage write path: a cheap deterministic
robot hard-gate (well-formedness) followed by escalation to the Senate
(semantic judgment) only when needed. This module builds the ROBOT side +
the state machine up to `pending-senate` + verdict application. The Senate
WAKE itself is SAW-31, not here.

Proposal state machine (S6):

    proposed --[robot hard-gate]--> rejected-malformed
                                |-> validated --[pre-check + escalation]-->
                                       auto-ingested (reachable, empty policy)
                                       pending-senate --[resolve verdict]-->
                                              ingested | rejected | revise

  - `revise` is NOT a stored state: the proposal re-enters at `proposed`
    (awaiting the agent's revised resubmit) and is bounded to N rounds (A15).
  - `auto-ingested` is reachable but its promotion POLICY is empty here
    (Cluster C / SAW-31): `_NEVER_AUTO` always escalates. A test injects a
    promoting predicate to prove the path ingests with no Senate verdict —
    no dead DDL state (L6/R9).

Invariants honoured:
  - Append-only store: a node is never mutated after birth. Proposal CONTENT
    is append-only too (a revision is a NEW file `<key>.rN.md`). Only the
    per-proposal lifecycle (the `.state.json` sidecar) is mutable — the
    antechamber is a queue, not canonical knowledge.
  - ID allocation is the robot's monopoly: at ingest, inside the serialized
    gate, the node id is burned from `id_counter` (never markdown-max, A15).
    A crash after the burn leaves a gap, never a collision (S7: unique, not
    gapless). The fold's `max()` guard keeps the re-touch idempotent.
  - The antechamber lives OUTSIDE the warehouse dir (G6/A3) and survives an
    index rebuild AND an index loss: the SQLite `antechamber` table is a
    disposable MIRROR, re-derivable from the dir via `reconcile_antechamber`
    (L4/R3 — A8 named this "B4's concern").
  - The robot writes files, never runs git (G3).

The proposal file format (a node file MINUS the three robot-stamped keys
`id` / `timestamp` / `schema_version`, which the gate stamps at ingest) is
specified in docs/WRITE_PROTOCOL.md.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from . import config, fold, schema, store
from .errors import (
    AntechamberError, CodecError, GateError, MalformedProposal,
    RevisionLimitReached, RobotError,
)
from .ids import AUDIT_PLANE, KNOWLEDGE_PLANE, format_id

# --- states (mirror the B1 antechamber CHECK enum; no schema change in B4) ---
STATE_PROPOSED = "proposed"
STATE_REJECTED_MALFORMED = "rejected-malformed"
STATE_VALIDATED = "validated"
STATE_PENDING_SENATE = "pending-senate"
STATE_AUTO_INGESTED = "auto-ingested"
STATE_INGESTED = "ingested"
STATE_REJECTED = "rejected"

VERDICTS = ("ingested", "rejected", "revise")

# Terminal lifecycle states: the proposal is closed, nothing further happens to
# it. The complement — {proposed, validated, pending-senate} — is the LIVE queue
# that `list_pending` surfaces by default (the Senate-wake's backing, SAW-31).
TERMINAL_STATES = (
    STATE_REJECTED_MALFORMED, STATE_AUTO_INGESTED, STATE_INGESTED, STATE_REJECTED,
)

# Proposal frontmatter: the node spine MINUS the robot-stamped keys.
ROBOT_STAMPED_KEYS = ("id", "timestamp", "schema_version")
PROPOSAL_KEY_ORDER = (
    "kind", "status", "title", "scope", "verdict", "flag_type",
    "origin", "ticket", "agent", "source",
)
PROPOSAL_REQUIRED_KEYS = ("kind", "status", "title", "origin")

# Per-kind required fields (S3 Cluster 2). The hard-gate addition over the
# structural codec, which deliberately omits these (B1 note §5).
PER_KIND_REQUIRED = {
    "decision": ("scope",),
    "constraint": ("source",),
    "lesson": ("agent", "ticket"),
    "flag": (),  # flag GENERATION is B5; the gate only accepts a well-formed flag
}

# Allowed SOURCE kind per edge type (S3 Cluster 3 + S6 audit edges), verified
# against the B1 fixtures: `relates-to` is any->any; `resolves` is emitted by
# the resolver (any knowledge node OR a flag) and targets a flag (demo-n7).
EDGE_SOURCE_KINDS = {
    "supersedes": {"decision"},
    "derived-from": {"decision"},
    "constrains": {"constraint"},
    "about": {"lesson"},
    "flags": {"flag"},
    "relates-to": {"decision", "constraint", "lesson", "flag"},
    "resolves": {"decision", "constraint", "lesson", "flag"},
}

DEFAULT_REVISE_LIMIT = 3  # placeholder dial (B3 budget-dial precedent), retro-calibrated

SIDECAR_SUFFIX = ".state.json"
_PROPOSAL_KEY_RE = re.compile(r"^(?P<prefix>[a-z][a-z0-9]*)-p(?P<number>[1-9][0-9]*)$")
_KEY_LINE_RE = re.compile(r"^([a-z][a-z0-9_]*): (.*)$")
_EDGE_TYPE_LINE_RE = re.compile(r"^  - type: (.*)$")
_EDGE_TARGET_LINE_RE = re.compile(r"^    target: (.*)$")

_MIRROR_COLUMNS = (
    "proposal_key", "state", "ticket", "agent", "created_at", "updated_at",
    "content_hash", "file_path", "node_id",
)

_PLACEHOLDER_TS = "2000-01-01T00:00:00Z"  # only to satisfy the codec format check


def _NEVER_AUTO(draft):
    """The empty promotion gate (Cluster C / SAW-31): nothing auto-ingests."""
    return False


def _utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Proposal codec + hard-schema gate
# ---------------------------------------------------------------------------

class ProposalDraft:
    """A candidate node WITHOUT identity — the robot stamps id/timestamp/
    schema_version at ingest. All fields default None so the hard-gate, not
    the constructor, reports a missing required field."""

    __slots__ = (
        "kind", "status", "title", "origin", "body", "scope", "verdict",
        "flag_type", "ticket", "agent", "source", "edges",
    )

    def __init__(self, body, edges=None, **fields):
        for name in self.__slots__:
            setattr(self, name, None)
        self.body = body
        self.edges = list(edges or [])
        for key, value in fields.items():
            setattr(self, key, value)

    @property
    def plane(self):
        return AUDIT_PLANE if self.kind == "flag" else KNOWLEDGE_PLANE


def parse_proposal_text(text):
    """Parse a proposal file into a ProposalDraft.

    This is the STRUCTURAL gate: it raises MalformedProposal (→ never
    persisted, CLI exit 2) when the input is not proposal-shaped — bad fence,
    a non `key: value` line, an unknown key, a key out of canonical order, or
    one of the robot-stamped keys (id/timestamp/schema_version) the proposer
    must not set. Deep field VALIDITY (scalars, edge types, per-kind required
    fields) is the hard-gate's job and yields the persisted 'rejected-malformed'
    state, not an exception.
    """
    if not isinstance(text, str) or not text.startswith("---\n"):
        raise MalformedProposal("proposal must start with a '---' fence line")
    fence_at = text.find("\n---\n", 3)
    if fence_at == -1:
        raise MalformedProposal("closing '---' fence not found")
    fm_block = text[4:fence_at]
    rest = text[fence_at + 5:]
    if not rest.startswith("\n"):
        raise MalformedProposal("exactly one blank line is required after the closing fence")
    body = rest[1:]

    fields = {}
    edges = []
    last_idx = -1
    lines = fm_block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == "edges:":
            edges = _parse_edges(lines, i + 1)
            break
        m = _KEY_LINE_RE.match(line)
        if not m:
            raise MalformedProposal(f"frontmatter line outside the proposal subset: {line!r}")
        key, value = m.group(1), m.group(2)
        if key in ROBOT_STAMPED_KEYS:
            raise MalformedProposal(
                f"key {key!r} is stamped by the robot at ingest and must not "
                "appear in a proposal"
            )
        if key not in PROPOSAL_KEY_ORDER:
            raise MalformedProposal(f"unknown proposal key: {key!r}")
        idx = PROPOSAL_KEY_ORDER.index(key)
        if idx <= last_idx:
            raise MalformedProposal(f"proposal key {key!r} is duplicated or out of canonical order")
        last_idx = idx
        fields[key] = value
        i += 1
    return ProposalDraft(body, edges=edges, **fields)


def _parse_edges(lines, start):
    if start >= len(lines):
        raise MalformedProposal("'edges:' block must contain at least one entry")
    edges = []
    i = start
    while i < len(lines):
        m = _EDGE_TYPE_LINE_RE.match(lines[i])
        if not m:
            raise MalformedProposal(f"expected edge entry '  - type: <type>', got: {lines[i]!r}")
        edge_type = m.group(1)
        i += 1
        if i >= len(lines):
            raise MalformedProposal("edge entry is missing its '    target: <id>' line")
        m = _EDGE_TARGET_LINE_RE.match(lines[i])
        if not m:
            raise MalformedProposal(f"expected '    target: <id>', got: {lines[i]!r}")
        edges.append(store.Edge(type=edge_type, target=m.group(1)))
        i += 1
    return edges


def hard_gate(draft, prefix):
    """The hard-schema gate (S6): well-formedness, no Senate cost.

    Raises MalformedProposal on the first violation. Three layers:
    1. required spine keys present;
    2. full node-format validity, reused from the B1 codec via a placeholder
       node (scalars, status/origin enums, verdict-on-lesson, flag_type/scope
       slugs, edge-type legality, body shape) — zero duplication, zero churn
       to the GREEN store;
    3. per-kind required fields (scope/source/agent+ticket) and per-edge
       source-kind legality (S3) — exactly what the codec leaves to B4.
    """
    missing_spine = [k for k in PROPOSAL_REQUIRED_KEYS if getattr(draft, k) is None]
    if missing_spine:
        raise MalformedProposal(f"missing required field(s): {', '.join(missing_spine)}")

    plane = draft.plane
    placeholder = store.Node(
        id=format_id(prefix, plane, 1), kind=draft.kind, status=draft.status,
        title=draft.title, origin=draft.origin, timestamp=_PLACEHOLDER_TS,
        schema_version=1, body=draft.body, scope=draft.scope,
        verdict=draft.verdict, flag_type=draft.flag_type, ticket=draft.ticket,
        agent=draft.agent, source=draft.source, edges=list(draft.edges),
    )
    try:
        store.serialize_node(placeholder)  # runs the codec's full semantic check
    except CodecError as exc:
        raise MalformedProposal(str(exc)) from exc

    for required in PER_KIND_REQUIRED.get(draft.kind, ()):
        if getattr(draft, required) is None:
            raise MalformedProposal(
                f"a {draft.kind} proposal requires {required!r} (S3)"
            )

    for edge in draft.edges:
        allowed = EDGE_SOURCE_KINDS.get(edge.type)
        if allowed is not None and draft.kind not in allowed:
            raise MalformedProposal(
                f"a {draft.kind} may not emit a {edge.type!r} edge "
                f"(S3: only {sorted(allowed)} may)"
            )


# ---------------------------------------------------------------------------
# Antechamber: sidecar (mutable lifecycle) + content files (append-only)
# ---------------------------------------------------------------------------

def _sidecar_path(antechamber_root, key):
    return Path(antechamber_root) / f"{key}{SIDECAR_SUFFIX}"


def _write_sidecar(antechamber_root, key, sidecar):
    _sidecar_path(antechamber_root, key).write_text(
        json.dumps(sidecar, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _read_sidecar(antechamber_root, key):
    path = _sidecar_path(antechamber_root, key)
    if not path.exists():
        raise AntechamberError(f"no such proposal: {key}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AntechamberError(f"corrupt sidecar for {key}: {exc}") from exc


def _read_content(antechamber_root, sidecar):
    return (Path(antechamber_root) / sidecar["content_file"]).read_text(encoding="utf-8")


def _iter_sidecars(antechamber_root):
    antechamber_root = Path(antechamber_root)
    if not antechamber_root.is_dir():
        return
    for path in sorted(antechamber_root.glob("*" + SIDECAR_SUFFIX)):
        key = path.name[: -len(SIDECAR_SUFFIX)]
        if not _PROPOSAL_KEY_RE.match(key):
            raise AntechamberError(f"sidecar name is not a proposal key: {path.name}")
        try:
            sidecar = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise AntechamberError(f"corrupt sidecar {path.name}: {exc}") from exc
        yield key, sidecar


def _allocate_key(antechamber_root, prefix):
    """Allocate the next `<prefix>-p<n>` from the antechamber dir (max+1).

    Proposal keys are a separate namespace from node IDs — the A15 id_counter
    monopoly governs NODE ids, which collide; proposal keys do not enter the
    knowledge graph and are derived from their own truth (the dir)."""
    highest = 0
    for key, _ in _iter_sidecars(antechamber_root):
        m = _PROPOSAL_KEY_RE.match(key)
        if m and m.group("prefix") == prefix:
            highest = max(highest, int(m.group("number")))
    return format_proposal_key(prefix, highest + 1)


def format_proposal_key(prefix, number):
    return f"{prefix}-p{number}"


# ---------------------------------------------------------------------------
# Mirror (the disposable SQLite projection of the antechamber dir)
# ---------------------------------------------------------------------------

def _mirror_row(sidecar):
    return (
        sidecar["proposal_key"], sidecar["state"], sidecar["ticket"],
        sidecar["agent"], sidecar["created_at"], sidecar["updated_at"],
        sidecar["content_hash"], sidecar["content_file"], sidecar.get("node_id"),
    )


def _upsert_mirror(conn, sidecar):
    conn.execute("DELETE FROM antechamber WHERE proposal_key = ?", (sidecar["proposal_key"],))
    conn.execute(
        "INSERT INTO antechamber (" + ", ".join(_MIRROR_COLUMNS) + ") VALUES ("
        + ", ".join("?" for _ in _MIRROR_COLUMNS) + ")",
        _mirror_row(sidecar),
    )


def _mirror(warehouse_root, sidecar):
    conn = schema.connect(Path(warehouse_root) / schema.INDEX_FILENAME)
    try:
        with conn:
            _upsert_mirror(conn, sidecar)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# The write path: propose -> evaluate -> (auto-ingest | pending-senate)
# ---------------------------------------------------------------------------

def propose(warehouse_root, antechamber_root, text, ticket, agent, *,
            now=None, auto_ingest=_NEVER_AUTO):
    """Submit a proposal. Writes the content + sidecar to the antechamber as
    `proposed`, then runs the hard-gate and the pre-check/escalation decision.

    `ticket`+`agent` are the self-declared submitter BINDING (L5/A15) — the
    revise-wake handle — distinct from the node's provenance fields (a
    `constraint` has no provenance agent but still has a submitter). Logged,
    not enforced (G8 posture).
    """
    cfg = config.load_config(warehouse_root)  # also asserts an initialised root
    now = now or _utc_now()
    if not ticket or not agent:
        raise AntechamberError("a proposal must carry a self-declared ticket and agent (binding)")

    draft = parse_proposal_text(text)  # structural; raises -> never persisted

    antechamber_root = Path(antechamber_root)
    antechamber_root.mkdir(parents=True, exist_ok=True)
    key = _allocate_key(antechamber_root, cfg.project_prefix)
    content_file = f"{key}.md"
    (antechamber_root / content_file).write_text(text, encoding="utf-8")  # append-only

    sidecar = {
        "proposal_key": key, "state": STATE_PROPOSED, "ticket": ticket,
        "agent": agent, "created_at": now, "updated_at": now, "round": 1,
        "content_file": content_file, "content_hash": store.content_hash(text),
        "node_id": None,
    }
    _write_sidecar(antechamber_root, key, sidecar)
    _mirror(warehouse_root, sidecar)
    return _evaluate(warehouse_root, antechamber_root, key, draft, sidecar, now, auto_ingest)


def revise(warehouse_root, antechamber_root, key, text, *, now=None,
           auto_ingest=_NEVER_AUTO):
    """Resubmit revised content for a proposal the Senate sent back (A15).

    The revised content is a NEW append-only file `<key>.rN.md`; the round
    counter advances; the proposal re-runs the hard-gate and re-enters the
    escalation decision. Bounded by `resolve(..., 'revise')`, not here.
    """
    now = now or _utc_now()
    sidecar = _read_sidecar(antechamber_root, key)
    if sidecar["state"] != STATE_PROPOSED:
        raise AntechamberError(
            f"proposal {key} is {sidecar['state']!r}; revise applies only to a "
            "proposal the Senate sent back (state 'proposed')"
        )
    draft = parse_proposal_text(text)  # structural; raises -> never persisted
    new_round = sidecar["round"] + 1
    content_file = f"{key}.r{new_round}.md"
    (Path(antechamber_root) / content_file).write_text(text, encoding="utf-8")
    sidecar = dict(sidecar, round=new_round, content_file=content_file,
                   content_hash=store.content_hash(text), updated_at=now)
    sidecar.pop("reason", None)
    _write_sidecar(antechamber_root, key, sidecar)
    _mirror(warehouse_root, sidecar)
    return _evaluate(warehouse_root, antechamber_root, key, draft, sidecar, now, auto_ingest)


def _evaluate(warehouse_root, antechamber_root, key, draft, sidecar, now, auto_ingest):
    cfg = config.load_config(warehouse_root)
    try:
        hard_gate(draft, cfg.project_prefix)
    except MalformedProposal as exc:
        sidecar = dict(sidecar, state=STATE_REJECTED_MALFORMED, updated_at=now,
                       reason=str(exc))
        _write_sidecar(antechamber_root, key, sidecar)
        _mirror(warehouse_root, sidecar)
        return {"proposal_key": key, "state": STATE_REJECTED_MALFORMED,
                "reason": str(exc), "round": sidecar["round"]}

    # validated — a real, observable transition (the escalation predicate runs
    # while the proposal rests here, so the state is exercised, not dead).
    sidecar = dict(sidecar, state=STATE_VALIDATED, updated_at=now)
    _write_sidecar(antechamber_root, key, sidecar)
    _mirror(warehouse_root, sidecar)

    report = _connection_report(warehouse_root, draft)
    if auto_ingest(draft):
        node_id, sidecar = _ingest(warehouse_root, antechamber_root, key, draft,
                                   sidecar, now=now, final_state=STATE_AUTO_INGESTED)
        return {"proposal_key": key, "state": STATE_AUTO_INGESTED,
                "node_id": node_id, "connection_report": report,
                "round": sidecar["round"]}

    sidecar = dict(sidecar, state=STATE_PENDING_SENATE, updated_at=now)
    _write_sidecar(antechamber_root, key, sidecar)
    _mirror(warehouse_root, sidecar)
    return {"proposal_key": key, "state": STATE_PENDING_SENATE,
            "round": sidecar["round"], "connection_report": report,
            "escalation_packet": _escalation_packet(key, draft, sidecar, report)}


def resolve(warehouse_root, antechamber_root, key, verdict, *, now=None,
            revise_limit=DEFAULT_REVISE_LIMIT):
    """Apply a Senate verdict to a pending proposal (the robot side; WHO issues
    the verdict — the Senate wake — is SAW-31).

    ingested -> allocate id, append the node, fold, mirror -> ingested.
    rejected -> mirror -> rejected.
    revise   -> re-enter at proposed (await resubmit), bounded to N rounds;
                at the bound, raise RevisionLimitReached with an owner packet.
    """
    now = now or _utc_now()
    if verdict not in VERDICTS:
        raise AntechamberError(f"unknown verdict {verdict!r} (expected one of {VERDICTS})")
    sidecar = _read_sidecar(antechamber_root, key)
    if sidecar["state"] != STATE_PENDING_SENATE:
        raise AntechamberError(
            f"proposal {key} is {sidecar['state']!r}; only a 'pending-senate' "
            "proposal can be resolved"
        )

    if verdict == "ingested":
        draft = parse_proposal_text(_read_content(antechamber_root, sidecar))
        node_id, sidecar = _ingest(warehouse_root, antechamber_root, key, draft,
                                   sidecar, now=now, final_state=STATE_INGESTED)
        return {"proposal_key": key, "state": STATE_INGESTED, "node_id": node_id,
                "round": sidecar["round"]}

    if verdict == "rejected":
        sidecar = dict(sidecar, state=STATE_REJECTED, updated_at=now)
        _write_sidecar(antechamber_root, key, sidecar)
        _mirror(warehouse_root, sidecar)
        return {"proposal_key": key, "state": STATE_REJECTED, "round": sidecar["round"]}

    # verdict == "revise"
    if sidecar["round"] >= revise_limit:
        packet = {"proposal_key": key, "round": sidecar["round"],
                  "revise_limit": revise_limit,
                  "binding": {"ticket": sidecar["ticket"], "agent": sidecar["agent"]},
                  "reason": "revise loop exhausted — owner must ingest, reject, "
                            "or raise the limit"}
        raise RevisionLimitReached(
            f"proposal {key} has used its {revise_limit} revise round(s); "
            "escalating to the owner", packet)
    sidecar = dict(sidecar, state=STATE_PROPOSED, updated_at=now)
    _write_sidecar(antechamber_root, key, sidecar)
    _mirror(warehouse_root, sidecar)
    return {"proposal_key": key, "state": STATE_PROPOSED, "awaiting": "revision",
            "round": sidecar["round"]}


def _burn_id(conn, prefix, plane):
    """Allocate the next id on `plane` from id_counter, in its own committed
    txn (S7: a crash now skips an id — a gap — but never reuses one).
    SELECT+UPDATE (not RETURNING) for portability; atomic under the
    single-writer serialized gate (A15 intent, A19 syntax)."""
    with conn:
        row = conn.execute(
            "SELECT next_value FROM id_counter WHERE plane = ?", (plane,)
        ).fetchone()
        if row is None:
            raise GateError(f"id_counter has no row for plane {plane!r}")
        number = row[0]
        conn.execute(
            "UPDATE id_counter SET next_value = ? WHERE plane = ?",
            (number + 1, plane),
        )
    return format_id(prefix, plane, number)


def append_node(conn, warehouse_root, cfg, *, kind, status, title, origin, body,
                now, scope=None, verdict=None, flag_type=None, ticket=None,
                agent=None, source=None, edges=()):
    """Mint a node and commit it to the warehouse: burn an id from the counter,
    write the canonical markdown (truth first, append-only), then fold it.

    This is the SINGLE node-id allocation path — the ID monopoly (A15). Both
    the B4 write gate (`_ingest`, knowledge proposals on the `n` plane) and the
    B5 audit (flag emission on the `f` plane) mint here, never markdown-max.
    The plane is derived from `kind` so it can never disagree with the id.
    It is a library primitive, NOT a CLI surface — there is no gate-bypassing
    write command (B2's concern); the gate hard-checks proposals before they
    reach here, and the audit only ever emits deterministic flags.
    """
    plane = AUDIT_PLANE if kind == "flag" else KNOWLEDGE_PLANE
    node_id = _burn_id(conn, cfg.project_prefix, plane)
    node = store.Node(
        id=node_id, kind=kind, status=status, title=title, origin=origin,
        timestamp=now, schema_version=cfg.schema_version, body=body, scope=scope,
        verdict=verdict, flag_type=flag_type, ticket=ticket, agent=agent,
        source=source, edges=list(edges),
    )
    node_path = store.write_node_file(warehouse_root, node)
    # Fold into the index (B2 hot path; its max() guard keeps the counter
    # advance idempotent — G11 / B3 open-Q#2).
    fold.upsert_node_file(conn, warehouse_root, node_path,
                          expected_prefix=cfg.project_prefix)
    return node_id, node_path


def _ingest(warehouse_root, antechamber_root, key, draft, sidecar, *, now, final_state):
    """The serializing gate: mint the node via the shared `append_node`
    primitive, then advance the proposal to its terminal state."""
    cfg = config.load_config(warehouse_root)
    conn = schema.connect(Path(warehouse_root) / schema.INDEX_FILENAME)
    try:
        node_id, _ = append_node(
            conn, warehouse_root, cfg, kind=draft.kind, status=draft.status,
            title=draft.title, origin=draft.origin, body=draft.body, now=now,
            scope=draft.scope, verdict=draft.verdict, flag_type=draft.flag_type,
            ticket=draft.ticket, agent=draft.agent, source=draft.source,
            edges=draft.edges,
        )
        sidecar = dict(sidecar, state=final_state, node_id=node_id, updated_at=now)
        _write_sidecar(antechamber_root, key, sidecar)
        with conn:
            _upsert_mirror(conn, sidecar)
    finally:
        conn.close()
    return node_id, sidecar


def _connection_report(warehouse_root, draft):
    """Pre-check (S6): are the proposal's edge targets present in the index?
    A dangling target is a B5 audit signal, NEVER a gate block (consistent
    with the fold being a mechanism, not a gate, and B3's {missing:true})."""
    if not draft.edges:
        return {"edges": [], "missing_targets": []}
    conn = schema.connect(Path(warehouse_root) / schema.INDEX_FILENAME)
    try:
        present = {row[0] for row in conn.execute("SELECT id FROM nodes")}
    finally:
        conn.close()
    edges = [{"type": e.type, "target": e.target, "present": e.target in present}
             for e in draft.edges]
    missing = sorted({e.target for e in draft.edges if e.target not in present})
    return {"edges": edges, "missing_targets": missing}


def _escalation_packet(key, draft, sidecar, report):
    """The pre-assembled packet the Senate wake (SAW-31) consumes."""
    return {
        "proposal_key": key,
        "round": sidecar["round"],
        "binding": {"ticket": sidecar["ticket"], "agent": sidecar["agent"]},
        "proposal": {
            "kind": draft.kind, "status": draft.status, "title": draft.title,
            "scope": draft.scope, "origin": draft.origin,
            "ticket": draft.ticket, "agent": draft.agent, "source": draft.source,
            "edges": [{"type": e.type, "target": e.target} for e in draft.edges],
        },
        "connection_report": report,
    }


# ---------------------------------------------------------------------------
# Antechamber reconcile + divergence (L4/R3; the B2-analogue for the mirror)
# ---------------------------------------------------------------------------

def reconcile_antechamber(warehouse_root, antechamber_root):
    """Re-derive the disposable mirror from the antechamber dir (the truth).

    This is what makes the mirror survive an index LOSS, not just a rebuild
    (A8 carries it over verbatim; this rebuilds it from scratch). Content
    hashes are recomputed from the content files so a stale sidecar hash
    cannot poison the mirror."""
    antechamber_root = Path(antechamber_root)
    conn = schema.connect(Path(warehouse_root) / schema.INDEX_FILENAME)
    rebuilt = 0
    try:
        with conn:
            conn.execute("DELETE FROM antechamber")
            for key, sidecar in _iter_sidecars(antechamber_root):
                content = (antechamber_root / sidecar["content_file"]).read_text(encoding="utf-8")
                sidecar = dict(sidecar, content_hash=store.content_hash(content))
                _upsert_mirror(conn, sidecar)
                rebuilt += 1
    finally:
        conn.close()
    return rebuilt


class AntechamberDivergenceReport:
    """markdown-dir (truth) vs SQLite mirror (projection) — the write-path
    analogue of B2's DivergenceReport."""

    def __init__(self):
        self.index_missing = False
        self.missing_in_mirror = []   # keys with a sidecar but no mirror row
        self.missing_in_dir = []      # mirror rows with no sidecar
        self.state_mismatch = []      # (key, dir_state, mirror_state)
        self.hash_mismatch = []       # keys whose content diverged
        self.node_id_mismatch = []    # (key, dir_node_id, mirror_node_id)
        self.unreadable = []          # (name, reason)

    @property
    def clean(self):
        return not (
            self.index_missing or self.missing_in_mirror or self.missing_in_dir
            or self.state_mismatch or self.hash_mismatch
            or self.node_id_mismatch or self.unreadable
        )

    def lines(self):
        if self.clean:
            return ["clean: antechamber dir and mirror agree"]
        if self.index_missing:
            return ["index file is missing — run reconcile to rebuild it"]
        out = []
        for key in self.missing_in_mirror:
            out.append(f"missing in mirror: {key} (sidecar exists, no mirror row)")
        for key in self.missing_in_dir:
            out.append(f"missing in dir: {key} (mirror row exists, no sidecar)")
        for key, ds, ms in self.state_mismatch:
            out.append(f"state mismatch: {key} dir={ds!r} mirror={ms!r}")
        for key in self.hash_mismatch:
            out.append(f"hash mismatch: {key} (content diverged from mirror)")
        for key, dn, mn in self.node_id_mismatch:
            out.append(f"node_id mismatch: {key} dir={dn!r} mirror={mn!r}")
        for name, reason in self.unreadable:
            out.append(f"unreadable: {name} ({reason})")
        return out


def check_antechamber(warehouse_root, antechamber_root):
    """Cheap divergence check: antechamber dir vs the SQLite mirror."""
    antechamber_root = Path(antechamber_root)
    report = AntechamberDivergenceReport()
    index_path = Path(warehouse_root) / schema.INDEX_FILENAME
    if not index_path.exists():
        report.index_missing = True
        return report

    on_disk = {}
    if antechamber_root.is_dir():
        for path in sorted(antechamber_root.glob("*" + SIDECAR_SUFFIX)):
            key = path.name[: -len(SIDECAR_SUFFIX)]
            try:
                if not _PROPOSAL_KEY_RE.match(key):
                    raise AntechamberError("sidecar name is not a proposal key")
                sidecar = json.loads(path.read_text(encoding="utf-8"))
                content = (antechamber_root / sidecar["content_file"]).read_text(encoding="utf-8")
            except (RobotError, OSError, json.JSONDecodeError, KeyError) as exc:
                report.unreadable.append((path.name, str(exc)))
                continue
            on_disk[key] = (sidecar, store.content_hash(content))

    conn = schema.connect(index_path)
    try:
        mirror = {row[0]: row for row in conn.execute(
            "SELECT proposal_key, state, content_hash, node_id FROM antechamber"
        )}
    finally:
        conn.close()

    report.missing_in_mirror = sorted(set(on_disk) - set(mirror))
    report.missing_in_dir = sorted(set(mirror) - set(on_disk))
    for key in sorted(set(on_disk) & set(mirror)):
        sidecar, content_hash = on_disk[key]
        _, m_state, m_hash, m_node = mirror[key]
        if sidecar["state"] != m_state:
            report.state_mismatch.append((key, sidecar["state"], m_state))
        if content_hash != m_hash:
            report.hash_mismatch.append(key)
        if sidecar.get("node_id") != m_node:
            report.node_id_mismatch.append((key, sidecar.get("node_id"), m_node))
    return report


# ---------------------------------------------------------------------------
# Read-only listing (the Senate-wake's backing — SAW-31 F5/#1)
# ---------------------------------------------------------------------------

_LIST_FIELDS = ("proposal_key", "state", "ticket", "agent", "created_at", "content_file")


def _proposal_key_sort(key):
    """Numeric sort key for a proposal key, so `food-p2` precedes `food-p10`
    (a lexical sort would not). `_iter_sidecars` has already validated the key
    against `_PROPOSAL_KEY_RE`, so the match is guaranteed present."""
    m = _PROPOSAL_KEY_RE.match(key)
    return (m.group("prefix"), int(m.group("number")))


def list_pending(warehouse_root, antechamber_root=None, state=None):
    """List antechamber proposals from the SIDECARS (the truth, not the
    disposable mirror) — the backing the Senate session-start wake needs.

    Default returns the LIVE queue: every proposal NOT in a terminal state
    (the complement of `TERMINAL_STATES`). `state=<X>` filters to exactly one
    lifecycle state (the wake passes 'pending-senate'). Order is deterministic
    by proposal-key number. Read-only — never writes, never mints anything.

    `warehouse_root` is loaded first purely to assert an initialised root (an
    uninitialised root is a robot error → CLI exit 2), mirroring the rest of
    the surface; the listing itself is derived only from the antechamber dir.
    `antechamber_root` defaults to the A3 sibling of the warehouse root.
    """
    config.load_config(warehouse_root)  # asserts an initialised root
    if antechamber_root is None:
        antechamber_root = Path(warehouse_root).parent / "antechamber"
    rows = []
    for _key, sidecar in _iter_sidecars(antechamber_root):
        current = sidecar["state"]
        if state is not None:
            if current != state:
                continue
        elif current in TERMINAL_STATES:
            continue
        rows.append({field: sidecar.get(field) for field in _LIST_FIELDS})
    rows.sort(key=lambda row: _proposal_key_sort(row["proposal_key"]))
    return rows
