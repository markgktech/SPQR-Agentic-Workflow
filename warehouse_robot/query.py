"""The query interface — four verbs, the intent/verdict bracket, budget dials
and the consent-gate (S4 contract, S7 Cluster 4 signatures; ticket B3).

Read path only: the verbs read the derived index and write nothing but trace
rounds (and grant consumption) into it — never markdown, never git (G3).

Contract realized here (S4):

- Two phases. Disambiguation: `open_scope` (deterministic kind+scope feed,
  scope-bounded — the complete slice or a facet breakdown, never truncation)
  and `find` (the FTS5/BM25 finder side-door, rank-bounded top-N). Retrieval:
  `fetch` (bodies + edge TOC for explicitly selected IDs) and `traverse`
  (bounded typed-edge neighborhood expansion).

- Intent before / verdict after. Every verb call opens a trace round carrying
  the declared intent; `verdict` closes it. A new round is refused while the
  session has an open round — the bracket is enforced, not advisory. An open
  round only ever blocks its own session, and `verdict` itself is always
  allowed, so no deadlock state exists.

- Sessions and archetypes are self-declared (G8 honour-system): abuse is
  visible in the trace — a retro watchpoint, not a prevented act.

- Budget windows. Usage is counted over the session's current window: all
  rounds after the boundary set by the last consumed grant. Exhaustion (or a
  session closed by a terminal verdict) refuses the round and raises an
  escalation packet — trace, usage, refused call — for the owner. A fresh
  window requires a one-shot owner grant, consumed by the robot on the next
  round (consent-gate, never a cooldown). A refused round is NOT a trace row;
  the packet is the record the agent must surface (flagged for retro).

- Auto-broaden, the only robot-triggered round event, is strictly ONE
  deterministic step: only in `find`, only by dropping the scope filter.
  Dropping a kind filter changes the meaning of the question — that is agent
  judgment, an explicit re-query (owner decision, B3 planning #7). An empty
  `open_scope` slice is legitimate ABSENT evidence and is never broadened.

- Status is the derived status (S3/S6 views). Default visibility is
  active/open only; `include_inactive` is the explicit opt-in (denied to
  SCRUTINIZE — the superseded chain is lineage). `fetch` by explicit ID and
  `traverse` ignore the status filter by design: explicit selection and edge
  walking are deliberate acts, and the chain is the point of a traversal.

- Plane rule: queries address the knowledge plane unless `kind` is `flag`,
  which addresses the audit plane explicitly.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from . import config, schema, store
from .errors import BudgetExhausted, PolicyDenied, ProtocolError
from .ids import AUDIT_PLANE, KNOWLEDGE_PLANE, parse_id
from .policy import TERMINAL_VERDICTS, VERDICTS, policy_for

DEFAULT_TOP_N = 8

_ALL_KINDS = store.KNOWLEDGE_KINDS + store.AUDIT_KINDS
_WORD_RE = re.compile(r"\w+", re.UNICODE)

_SKELETON_SQL = (
    "SELECT n.id, n.title, n.kind, n.scope, n.plane, "
    "COALESCE(es.effective_status, fs.flag_status) AS status "
    "FROM nodes n "
    "LEFT JOIN v_effective_status es ON es.id = n.id "
    "LEFT JOIN v_flag_status fs ON fs.id = n.id "
)
_ACTIVE_COND = (
    "((n.plane = 'n' AND es.effective_status = 'active') "
    "OR (n.plane = 'f' AND fs.flag_status = 'open'))"
)


# ---------------------------------------------------------------------------
# Common plumbing
# ---------------------------------------------------------------------------

def _utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _open_index(warehouse_root):
    warehouse_root = Path(warehouse_root)
    config.load_config(warehouse_root)  # asserts an initialised root
    index_path = warehouse_root / schema.INDEX_FILENAME
    if not index_path.exists():
        raise ProtocolError(f"no derived index at {index_path} — run reconcile first")
    return schema.connect(index_path)


def _validate_common(session_id, intent):
    if not isinstance(session_id, str) or not session_id.strip():
        raise ProtocolError("session id must be a non-empty string")
    if not isinstance(intent, str) or not intent.strip():
        raise ProtocolError("intent must be declared before every round (K9)")


def _check_inactive(pol, include_inactive):
    if include_inactive and not pol.include_inactive_allowed:
        raise PolicyDenied(
            f"archetype {pol.archetype!r} may not see inactive nodes — the "
            "superseded chain is lineage (S4 SCRUTINIZE DENY)"
        )


def _id_sort_key(node_id):
    _, plane, number = parse_id(node_id)
    return (0 if plane == KNOWLEDGE_PLANE else 1, number)


def _skeleton(row):
    return {
        "id": row[0], "title": row[1], "kind": row[2],
        "scope": row[3], "status": row[5],
    }


# ---------------------------------------------------------------------------
# Budget window
# ---------------------------------------------------------------------------

def _window_start(conn, session_id):
    row = conn.execute(
        "SELECT max(consumed_after_round) FROM grants "
        "WHERE session_id = ? AND consumed_after_round IS NOT NULL",
        (session_id,),
    ).fetchone()
    return row[0] or 0


def _window_usage(conn, session_id):
    start = _window_start(conn, session_id)
    rounds = conn.execute(
        "SELECT round_id, verb, result_count, verdict FROM trace "
        "WHERE session_id = ? AND round_id > ? ORDER BY round_id",
        (session_id, start),
    ).fetchall()
    usage = {
        "window_start": start,
        "rounds": len(rounds),
        "wrong_entry": sum(1 for r in rounds if r[3] == "WRONG-ENTRY"),
        "traverse": sum(1 for r in rounds if r[3] == "INSUFFICIENT-TRAVERSE"),
        "bodies": sum(r[2] or 0 for r in rounds if r[1] == "fetch"),
        "last_verdict": rounds[-1][3] if rounds else None,
    }
    return usage


def _budget_snapshot(conn, session_id, pol):
    usage = _window_usage(conn, session_id)
    return {
        "wrong_entry": f"{usage['wrong_entry']}/{pol.wrong_entry_cap}",
        "traverse": f"{usage['traverse']}/{pol.traverse_cap}",
        "bodies": f"{usage['bodies']}/{pol.body_fetch_ceiling}",
    }


def _consume_grant_if_any(conn, session_id):
    row = conn.execute(
        "SELECT grant_id FROM grants "
        "WHERE session_id = ? AND consumed_after_round IS NULL "
        "ORDER BY grant_id LIMIT 1",
        (session_id,),
    ).fetchone()
    if row is None:
        return False
    boundary = conn.execute(
        "SELECT COALESCE(max(round_id), 0) FROM trace WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0]
    with conn:
        conn.execute(
            "UPDATE grants SET consumed_after_round = ? WHERE grant_id = ?",
            (boundary, row[0]),
        )
    return True


def _escalation_packet(conn, session_id, reason, refused_call):
    usage = _window_usage(conn, session_id)
    columns = (
        "round_id", "ts", "session_id", "ticket", "agent", "archetype",
        "verb", "intent", "params", "result_count", "result_ids", "verdict",
        "budget",
    )
    rows = conn.execute(
        "SELECT " + ", ".join(columns) + " FROM trace "
        "WHERE session_id = ? ORDER BY round_id",
        (session_id,),
    ).fetchall()
    return {
        "reason": reason,
        "refused": refused_call,
        "window_usage": usage,
        "session_trace": [dict(zip(columns, row)) for row in rows],
    }


def _gate_new_round(conn, session_id, pol, refused_call, bodies_requested=0):
    """Admit or refuse a new round (bracket + budget + consent-gate)."""
    open_row = conn.execute(
        "SELECT round_id, verb FROM trace "
        "WHERE session_id = ? AND verdict IS NULL",
        (session_id,),
    ).fetchone()
    if open_row is not None:
        raise ProtocolError(
            f"round {open_row[0]} ({open_row[1]}) is still open in session "
            f"{session_id!r} — close it with a verdict before the next round "
            "(intent-before/verdict-after bracket)"
        )

    if bodies_requested > pol.body_fetch_ceiling:
        raise ProtocolError(
            f"{bodies_requested} bodies requested in one fetch exceeds the "
            f"body-fetch ceiling ({pol.body_fetch_ceiling}) outright — narrow "
            "the selection; a grant cannot help here"
        )

    usage = _window_usage(conn, session_id)
    blocked = None
    last = usage["last_verdict"]
    if last in TERMINAL_VERDICTS:
        blocked = (
            f"session closed by terminal verdict {last} — a new round "
            "requires an owner-issued continuation grant"
        )
    elif last == "WRONG-ENTRY" and usage["wrong_entry"] >= pol.wrong_entry_cap:
        blocked = (
            f"WRONG-ENTRY retry cap reached ({usage['wrong_entry']}/"
            f"{pol.wrong_entry_cap}) — issue a terminal verdict with what "
            "was gathered, or obtain a continuation grant"
        )
    elif last == "INSUFFICIENT-TRAVERSE" and usage["traverse"] >= pol.traverse_cap:
        blocked = (
            f"INSUFFICIENT-TRAVERSE depth cap reached ({usage['traverse']}/"
            f"{pol.traverse_cap}) — issue a terminal verdict with what was "
            "gathered, or obtain a continuation grant"
        )
    elif bodies_requested and usage["bodies"] + bodies_requested > pol.body_fetch_ceiling:
        blocked = (
            f"body-fetch ceiling would be exceeded ({usage['bodies']} used + "
            f"{bodies_requested} requested > {pol.body_fetch_ceiling})"
        )

    if blocked is None:
        return
    if _consume_grant_if_any(conn, session_id):
        return  # fresh window opened by the consumed one-shot grant
    raise BudgetExhausted(
        blocked, _escalation_packet(conn, session_id, blocked, refused_call)
    )


# ---------------------------------------------------------------------------
# Trace writing (the intent/verdict bracket)
# ---------------------------------------------------------------------------

def _write_round(conn, *, session_id, ticket, agent, archetype, verb, intent,
                 params, result_count, result_ids, pol):
    with conn:
        cur = conn.execute(
            "INSERT INTO trace (ts, session_id, ticket, agent, archetype, "
            "verb, intent, params, result_count, result_ids, verdict, budget) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?)",
            (
                _utc_now(), session_id, ticket, agent, archetype, verb,
                intent.strip(),
                json.dumps(params, sort_keys=True, separators=(",", ":")),
                result_count,
                json.dumps(result_ids, separators=(",", ":")),
                None,  # budget snapshot is set right below, post-insert
            ),
        )
        round_id = cur.lastrowid
        snapshot = _budget_snapshot(conn, session_id, pol)
        conn.execute(
            "UPDATE trace SET budget = ? WHERE round_id = ?",
            (json.dumps(snapshot, sort_keys=True, separators=(",", ":")), round_id),
        )
    return round_id, snapshot


# ---------------------------------------------------------------------------
# Verb: open_scope — the deterministic feed (scope-bounded, faceted overflow)
# ---------------------------------------------------------------------------

def open_scope(warehouse_root, archetype, session_id, intent, scope=None,
               kind=None, include_inactive=False, ticket=None, agent=None,
               policy=None):
    pol = policy or policy_for(archetype)
    _validate_common(session_id, intent)
    _check_inactive(pol, include_inactive)
    if kind is not None and kind not in _ALL_KINDS:
        raise ProtocolError(f"unknown kind {kind!r} (expected one of {_ALL_KINDS})")

    params = {"scope": scope, "kind": kind, "include_inactive": include_inactive}
    refused_call = {"verb": "open_scope", "params": params}
    conn = _open_index(warehouse_root)
    try:
        _gate_new_round(conn, session_id, pol, refused_call)
        common = dict(session_id=session_id, ticket=ticket, agent=agent,
                      archetype=archetype, verb="open_scope", intent=intent,
                      params=params, pol=pol)

        if scope is None and kind is None:
            facets = _scope_facets(conn, include_inactive)
            round_id, snapshot = _write_round(
                conn, result_count=len(facets), result_ids=[], **common
            )
            return {
                "verb": "open_scope", "round_id": round_id,
                "view": "scope-facets", "facets": facets, "budget": snapshot,
            }

        rows = _slice_rows(conn, scope, kind, include_inactive)
        if len(rows) > pol.altitude_ceiling:
            kind_facets = None if kind is not None else _kind_facets(rows)
            round_id, snapshot = _write_round(
                conn, result_count=len(rows), result_ids=[], **common
            )
            return {
                "verb": "open_scope", "round_id": round_id,
                "overflow": True, "count": len(rows),
                "ceiling": pol.altitude_ceiling, "facets": kind_facets,
                "guidance": (
                    "slice exceeds the altitude ceiling — narrow by kind"
                    if kind is None
                    else "slice exceeds the altitude ceiling even with a kind "
                         "filter — use find, or ask the owner to raise the dial"
                ),
                "budget": snapshot,
            }

        candidates = [_skeleton(r) for r in
                      sorted(rows, key=lambda r: _id_sort_key(r[0]))]
        round_id, snapshot = _write_round(
            conn, result_count=len(candidates),
            result_ids=[c["id"] for c in candidates], **common
        )
        return {
            "verb": "open_scope", "round_id": round_id,
            "scope": scope, "kind": kind, "candidates": candidates,
            "count": len(candidates), "budget": snapshot,
        }
    finally:
        conn.close()


def _slice_rows(conn, scope, kind, include_inactive):
    conds, args = [], []
    if kind is not None:
        conds.append("n.kind = ?")
        args.append(kind)
        conds.append("n.plane = ?")
        args.append(AUDIT_PLANE if kind == "flag" else KNOWLEDGE_PLANE)
    else:
        conds.append("n.plane = ?")
        args.append(KNOWLEDGE_PLANE)
    if scope is not None:
        conds.append("n.scope = ?")
        args.append(scope)
    if not include_inactive:
        conds.append(_ACTIVE_COND)
    sql = _SKELETON_SQL + "WHERE " + " AND ".join(conds)
    return conn.execute(sql, args).fetchall()


def _scope_facets(conn, include_inactive):
    cond = "" if include_inactive else " AND " + _ACTIVE_COND
    rows = conn.execute(
        "SELECT n.scope, count(*) FROM nodes n "
        "LEFT JOIN v_effective_status es ON es.id = n.id "
        "LEFT JOIN v_flag_status fs ON fs.id = n.id "
        "WHERE n.plane = 'n'" + cond +
        " GROUP BY n.scope ORDER BY n.scope IS NULL, n.scope"
    ).fetchall()
    return [{"scope": scope, "count": count} for scope, count in rows]


def _kind_facets(rows):
    counts = {}
    for row in rows:
        counts[row[2]] = counts.get(row[2], 0) + 1
    return [{"kind": k, "count": counts[k]} for k in sorted(counts)]


# ---------------------------------------------------------------------------
# Verb: find — the FTS5/BM25 finder side-door (rank-bounded)
# ---------------------------------------------------------------------------

def find(warehouse_root, archetype, session_id, intent, text, kind=None,
         scope=None, top_n=None, include_inactive=False, ticket=None,
         agent=None, policy=None):
    pol = policy or policy_for(archetype)
    _validate_common(session_id, intent)
    _check_inactive(pol, include_inactive)
    if kind is not None and kind not in _ALL_KINDS:
        raise ProtocolError(f"unknown kind {kind!r} (expected one of {_ALL_KINDS})")
    if top_n is None:
        top_n = DEFAULT_TOP_N
    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n < 1:
        raise ProtocolError(f"top_n must be a positive integer, got {top_n!r}")
    if top_n > pol.altitude_ceiling:
        raise ProtocolError(
            f"top_n {top_n} exceeds the altitude ceiling ({pol.altitude_ceiling})"
        )
    fts_query = _fts_query(text)

    params = {
        "text": text, "kind": kind, "scope": scope, "top_n": top_n,
        "include_inactive": include_inactive,
    }
    refused_call = {"verb": "find", "params": params}
    conn = _open_index(warehouse_root)
    try:
        _gate_new_round(conn, session_id, pol, refused_call)
        rows = _find_rows(conn, fts_query, kind, scope, include_inactive, top_n)
        auto_broadened = False
        if not rows and scope is not None:
            # The only robot-triggered broaden: one step, scope drop only.
            rows = _find_rows(conn, fts_query, kind, None, include_inactive, top_n)
            auto_broadened = True
            params["auto_broadened"] = True  # retro-visible in the trace
        candidates = [_skeleton(r) for r in rows]  # rank order, not ID order
        round_id, snapshot = _write_round(
            conn, session_id=session_id, ticket=ticket, agent=agent,
            archetype=archetype, verb="find", intent=intent, params=params,
            result_count=len(candidates),
            result_ids=[c["id"] for c in candidates], pol=pol,
        )
        return {
            "verb": "find", "round_id": round_id, "query": text,
            "auto_broadened": auto_broadened,
            "dropped_filter": "scope" if auto_broadened else None,
            "candidates": candidates, "count": len(candidates),
            "budget": snapshot,
        }
    finally:
        conn.close()


def _fts_query(text):
    if not isinstance(text, str):
        raise ProtocolError("find text must be a string")
    tokens = _WORD_RE.findall(text)
    if not tokens:
        raise ProtocolError(f"find text contains no searchable tokens: {text!r}")
    # Quoted tokens joined with OR: the finder's job is recall (a foot in the
    # door, S7); BM25 ranks the union. Quoting disarms FTS5 query syntax.
    return " OR ".join(f'"{t}"' for t in tokens)


def _find_rows(conn, fts_query, kind, scope, include_inactive, top_n):
    conds = ["nodes_fts MATCH ?"]
    args = [fts_query]
    if kind is not None:
        conds.append("n.kind = ?")
        args.append(kind)
        conds.append("n.plane = ?")
        args.append(AUDIT_PLANE if kind == "flag" else KNOWLEDGE_PLANE)
    else:
        conds.append("n.plane = ?")
        args.append(KNOWLEDGE_PLANE)
    if scope is not None:
        conds.append("n.scope = ?")
        args.append(scope)
    if not include_inactive:
        conds.append(_ACTIVE_COND)
    sql = (
        "SELECT n.id, n.title, n.kind, n.scope, n.plane, "
        "COALESCE(es.effective_status, fs.flag_status) AS status "
        "FROM nodes_fts "
        "JOIN nodes n ON n.rowid = nodes_fts.rowid "
        "LEFT JOIN v_effective_status es ON es.id = n.id "
        "LEFT JOIN v_flag_status fs ON fs.id = n.id "
        "WHERE " + " AND ".join(conds) +
        " ORDER BY bm25(nodes_fts), n.id LIMIT ?"
    )
    args.append(top_n)
    return conn.execute(sql, args).fetchall()


# ---------------------------------------------------------------------------
# Verb: fetch — bodies + edge TOC for explicitly selected IDs
# ---------------------------------------------------------------------------

def fetch(warehouse_root, archetype, session_id, intent, ids, ticket=None,
          agent=None, policy=None):
    pol = policy or policy_for(archetype)
    _validate_common(session_id, intent)
    if not isinstance(ids, (list, tuple)) or not ids:
        raise ProtocolError("fetch requires a non-empty list of node ids")
    seen = set()
    for node_id in ids:
        try:
            parse_id(node_id)
        except Exception as exc:
            raise ProtocolError(f"fetch id invalid: {exc}") from exc
        if node_id in seen:
            raise ProtocolError(f"duplicate id in fetch selection: {node_id!r}")
        seen.add(node_id)
    ids = list(ids)

    params = {"ids": ids}
    refused_call = {"verb": "fetch", "params": params}
    conn = _open_index(warehouse_root)
    try:
        _gate_new_round(conn, session_id, pol, refused_call,
                        bodies_requested=len(ids))
        nodes, not_found = [], []
        for node_id in ids:
            entry = _fetch_one(conn, node_id, pol)
            if entry is None:
                not_found.append(node_id)
            else:
                nodes.append(entry)
        found_ids = [n["id"] for n in nodes]
        round_id, snapshot = _write_round(
            conn, session_id=session_id, ticket=ticket, agent=agent,
            archetype=archetype, verb="fetch", intent=intent, params=params,
            result_count=len(found_ids), result_ids=found_ids, pol=pol,
        )
        response = {
            "verb": "fetch", "round_id": round_id, "nodes": nodes,
            "not_found": not_found, "budget": snapshot,
        }
        if pol.denied_edge_types:
            response["hidden_edge_types"] = sorted(pol.denied_edge_types)
        return response
    finally:
        conn.close()


_FETCH_COLUMNS = (
    "id", "kind", "title", "scope", "verdict", "flag_type", "origin",
    "timestamp", "ticket", "agent", "source", "schema_version", "body",
    "file_path",
)


def _fetch_one(conn, node_id, pol):
    row = conn.execute(
        "SELECT " + ", ".join("n." + c for c in _FETCH_COLUMNS) + ", "
        "COALESCE(es.effective_status, fs.flag_status) AS status "
        "FROM nodes n "
        "LEFT JOIN v_effective_status es ON es.id = n.id "
        "LEFT JOIN v_flag_status fs ON fs.id = n.id "
        "WHERE n.id = ?",
        (node_id,),
    ).fetchone()
    if row is None:
        return None
    entry = dict(zip(_FETCH_COLUMNS, row[:-1]))
    entry["status"] = row[-1]
    entry["edges"] = {
        "out": _edge_toc(conn, pol, "out", node_id),
        "in": _edge_toc(conn, pol, "in", node_id),
    }
    return entry


def _edge_toc(conn, pol, direction, node_id):
    if direction == "out":
        rows = conn.execute(
            "SELECT type, target FROM edges WHERE src = ? ORDER BY type, target",
            (node_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT type, src FROM edges WHERE target = ? ORDER BY type, src",
            (node_id,),
        ).fetchall()
    toc = []
    for edge_type, other_id in rows:
        if edge_type in pol.denied_edge_types:
            continue  # S4 SCRUTINIZE DENY — noted in the response, not silent
        toc.append({"type": edge_type, "id": other_id,
                    **_neighbor_skeleton(conn, other_id)})
    return toc


def _neighbor_skeleton(conn, node_id):
    row = conn.execute(
        _SKELETON_SQL + "WHERE n.id = ?", (node_id,)
    ).fetchone()
    if row is None:
        return {"missing": True}  # dangling edge target — B5 audit territory
    return {"title": row[1], "kind": row[2], "status": row[5]}


# ---------------------------------------------------------------------------
# Verb: traverse — bounded typed-edge neighborhood expansion
# ---------------------------------------------------------------------------

def traverse(warehouse_root, archetype, session_id, intent, node_id,
             edge_type, depth=1, ticket=None, agent=None, policy=None):
    pol = policy or policy_for(archetype)
    _validate_common(session_id, intent)
    if edge_type not in store.EDGE_TYPES:
        raise ProtocolError(
            f"unknown edge type {edge_type!r} (expected one of {store.EDGE_TYPES})"
        )
    if edge_type in pol.denied_edge_types:
        raise PolicyDenied(
            f"archetype {pol.archetype!r} may not traverse {edge_type!r} edges "
            "(S4 SCRUTINIZE DENY: lineage and journey memory stay blind)"
        )
    if not isinstance(depth, int) or isinstance(depth, bool) or depth < 1:
        raise ProtocolError(f"depth must be a positive integer, got {depth!r}")
    if depth > pol.max_depth:
        raise ProtocolError(
            f"depth {depth} exceeds the policy maximum ({pol.max_depth})"
        )
    try:
        parse_id(node_id)
    except Exception as exc:
        raise ProtocolError(f"traverse origin invalid: {exc}") from exc

    params = {"id": node_id, "edge_type": edge_type, "depth": depth}
    refused_call = {"verb": "traverse", "params": params}
    conn = _open_index(warehouse_root)
    try:
        _gate_new_round(conn, session_id, pol, refused_call)
        origin = _neighbor_skeleton(conn, node_id)
        if origin.get("missing"):
            raise ProtocolError(f"traverse origin not found in index: {node_id!r}")

        steps, discovered = _walk(conn, node_id, edge_type, depth)
        round_id, snapshot = _write_round(
            conn, session_id=session_id, ticket=ticket, agent=agent,
            archetype=archetype, verb="traverse", intent=intent, params=params,
            result_count=len(discovered), result_ids=discovered, pol=pol,
        )
        return {
            "verb": "traverse", "round_id": round_id,
            "origin": {"id": node_id, **origin}, "edge_type": edge_type,
            "depth": depth, "steps": steps,
            "nodes": [{"id": d, **_neighbor_skeleton(conn, d)} for d in discovered],
            "budget": snapshot,
        }
    finally:
        conn.close()


def _walk(conn, origin, edge_type, depth):
    visited = {origin}
    frontier = [origin]
    seen_edges = set()
    steps, discovered = [], []
    for level in range(1, depth + 1):
        next_frontier = []
        for node_id in sorted(frontier, key=_id_sort_key):
            neighbors = []
            for _, target in conn.execute(
                "SELECT type, target FROM edges WHERE src = ? AND type = ? "
                "ORDER BY target", (node_id, edge_type)
            ):
                neighbors.append(("out", node_id, target, target))
            for _, src in conn.execute(
                "SELECT type, src FROM edges WHERE target = ? AND type = ? "
                "ORDER BY src", (node_id, edge_type)
            ):
                neighbors.append(("in", src, node_id, src))
            for direction, edge_src, edge_target, other in neighbors:
                if (edge_src, edge_target) in seen_edges:
                    continue
                seen_edges.add((edge_src, edge_target))
                steps.append({
                    "level": level, "from": node_id,
                    "direction": direction, "to": other,
                })
                if other not in visited:
                    visited.add(other)
                    discovered.append(other)
                    next_frontier.append(other)
        frontier = next_frontier
        if not frontier:
            break
    return steps, discovered


# ---------------------------------------------------------------------------
# Verdict — closing half of the bracket; always allowed (no deadlock state)
# ---------------------------------------------------------------------------

def verdict(warehouse_root, session_id, verdict_value):
    _validate_common(session_id, "close")
    if verdict_value not in VERDICTS:
        raise ProtocolError(
            f"unknown verdict {verdict_value!r} (expected one of {VERDICTS})"
        )
    conn = _open_index(warehouse_root)
    try:
        row = conn.execute(
            "SELECT round_id, verb FROM trace "
            "WHERE session_id = ? AND verdict IS NULL",
            (session_id,),
        ).fetchone()
        if row is None:
            raise ProtocolError(
                f"no open round in session {session_id!r} — nothing to close"
            )
        with conn:
            conn.execute(
                "UPDATE trace SET verdict = ? WHERE round_id = ?",
                (verdict_value, row[0]),
            )
        return {
            "verb": "verdict", "round_id": row[0], "closed_verb": row[1],
            "verdict": verdict_value,
            "session_closed": verdict_value in TERMINAL_VERDICTS,
        }
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Grant — owner-issued one-shot consent (issuance mechanism is owner-side)
# ---------------------------------------------------------------------------

def issue_grant(warehouse_root, session_id):
    _validate_common(session_id, "grant")
    conn = _open_index(warehouse_root)
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO grants (session_id, created_at) VALUES (?, ?)",
                (session_id, _utc_now()),
            )
        return {"verb": "grant", "grant_id": cur.lastrowid,
                "session_id": session_id}
    finally:
        conn.close()
