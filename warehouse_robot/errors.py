"""Error hierarchy for the warehouse robot.

Every robot-raised error derives from RobotError so the CLI can convert any
of them into a clean non-zero exit with a message, while genuine bugs
(unexpected exceptions) surface as tracebacks.
"""


class RobotError(Exception):
    """Base class for all warehouse-robot errors."""


class IdError(RobotError):
    """Malformed node ID, project prefix, or plane marker."""


class CodecError(RobotError):
    """Input outside the canonical markdown subset. The codec never guesses."""


class ConfigError(RobotError):
    """Invalid or missing instance manifest (warehouse.config.json)."""


class SchemaError(RobotError):
    """SQLite index bootstrap failure (including a missing FTS5 module)."""


class FoldError(RobotError):
    """Fold failure — a node file that cannot be mirrored into the index,
    or an unreadable previous index during reconcile carry-over."""


class QueryError(RobotError):
    """Query-path failure (B3) — protocol, policy, or budget."""


class ProtocolError(QueryError):
    """Intent/verdict bracket violation or malformed query parameters."""


class PolicyDenied(QueryError):
    """The archetype's query policy forbids the request (S4 structural DENY)."""


class BudgetExhausted(QueryError):
    """A budget dial is exhausted (S4 consent-gate). Carries the owner
    escalation packet: the refused call, window usage, and the session trace."""

    def __init__(self, message, packet):
        super().__init__(message)
        self.packet = packet
