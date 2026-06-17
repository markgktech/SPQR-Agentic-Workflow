"""Per-archetype query policy (S4 Cluster 6, G8; ticket B3).

Budget is the "how much" dial; DENY is the "what not" dial. The robot is the
authoritative enforcer — the v1.5 per-archetype policy blocks in agent files
are usage instructions for the agent, never the enforcement source.

The dial numbers below are placeholders awaiting retro calibration (owner
decision, B3 planning question #3). They live in code so a calibration is one
edit plus a reconcile away; per-call overrides may only tighten them — a
loosened budget is exactly what the continuation grant exists for.

Identity is self-declared (G8): the archetype is logged in the trace, so a
bypass is visible in retro even if not prevented. The same honour-system rule
applies to the session id (owner decision, B3 planning question #1).

The single true DENY (S4): SCRUTINIZE (Tribunus, Probator, Curator) must be
blind to the reasoning chain it is meant to re-derive — lineage traversal
(`supersedes`, `derived-from`) and journey memory (`about`-linked lessons).
Every other archetype's restriction is economy-driven scope-shaping already
handled by the budget dials and the agent's own filters.
"""

from dataclasses import dataclass, replace

from .errors import PolicyDenied, ProtocolError

ARCHETYPES = ("deliberate", "execute", "synthesize", "consult", "scrutinize")

TERMINAL_VERDICTS = ("FOUND-ENOUGH", "ABSENT", "FOUND-UNLINKED")
NONTERMINAL_VERDICTS = ("WRONG-ENTRY", "INSUFFICIENT-TRAVERSE")
VERDICTS = TERMINAL_VERDICTS + NONTERMINAL_VERDICTS

LINEAGE_EDGE_TYPES = ("supersedes", "derived-from", "about")

_NUMERIC_DIALS = (
    "altitude_ceiling", "wrong_entry_cap", "traverse_cap", "max_depth",
    "body_fetch_ceiling",
)


@dataclass(frozen=True)
class QueryPolicy:
    archetype: str
    altitude_ceiling: int     # max skeleton rows one open_scope may return
    wrong_entry_cap: int      # max rounds ending WRONG-ENTRY per budget window
    traverse_cap: int         # max rounds ending INSUFFICIENT-TRAVERSE per window
    max_depth: int            # max depth of a single traverse call
    body_fetch_ceiling: int   # max bodies fetched per budget window
    denied_edge_types: tuple = ()
    include_inactive_allowed: bool = True


_BASE_DIALS = dict(
    altitude_ceiling=50,
    wrong_entry_cap=3,
    traverse_cap=3,
    max_depth=3,
    body_fetch_ceiling=10,
)

DEFAULT_POLICIES = {
    "deliberate": QueryPolicy("deliberate", **_BASE_DIALS),
    "execute": QueryPolicy("execute", **_BASE_DIALS),
    "synthesize": QueryPolicy("synthesize", **_BASE_DIALS),
    "consult": QueryPolicy(
        "consult", **dict(_BASE_DIALS, body_fetch_ceiling=3)
    ),
    "scrutinize": QueryPolicy(
        "scrutinize",
        **dict(_BASE_DIALS, body_fetch_ceiling=5),
        denied_edge_types=LINEAGE_EDGE_TYPES,
        include_inactive_allowed=False,
    ),
}


def policy_for(archetype):
    """Resolve the default policy for a self-declared archetype."""
    if archetype not in DEFAULT_POLICIES:
        raise ProtocolError(
            f"unknown archetype {archetype!r} (expected one of {ARCHETYPES})"
        )
    return DEFAULT_POLICIES[archetype]


def tightened(base, **overrides):
    """Per-call dial overrides; tightening only (S4 — loosening is a grant)."""
    for name, value in overrides.items():
        if name not in _NUMERIC_DIALS:
            raise ProtocolError(
                f"unknown budget dial {name!r} (expected one of {_NUMERIC_DIALS})"
            )
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ProtocolError(f"budget dial {name!r} must be a positive integer, got {value!r}")
        if value > getattr(base, name):
            raise PolicyDenied(
                f"cannot loosen {name} from {getattr(base, name)} to {value} — "
                "a larger budget requires an owner-issued continuation grant"
            )
    return replace(base, **overrides)
