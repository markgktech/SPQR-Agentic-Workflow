"""Instance manifest (warehouse.config.json).

The manifest is the per-instance identity of a warehouse: the project prefix
used in node IDs, the node schema version (A2 — stamped per node, bumped via
a re-fold transform in the seed), and the governed scope vocabulary (G5 —
new scope values are an owner-approved act, never free text).

It lives at the warehouse root next to the canonical markdown and is
versioned with it; the derived SQLite index is NOT part of the manifest's
scope.

Full-reset behaviour (owner condition on B1 question #5, recorded in the
B1 delivery note): `init` refuses to run on an already-initialised root.
A full reset deletes the entire warehouse root — manifest included — and
re-runs `init`, which recreates the manifest from its parameters. The scope
vocabulary is intentionally lost on reset: migration (Phase 2) re-derives
it against real content (S5 mandatory guard / G11).
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .errors import ConfigError
from .ids import PREFIX_RE

CONFIG_FILENAME = "warehouse.config.json"
SCHEMA_VERSION = 1

_SCOPE_RE = re.compile(r"^[a-z][a-z0-9-]*$")
_MANIFEST_KEYS = ("project_prefix", "schema_version", "scope_vocabulary")


@dataclass
class WarehouseConfig:
    project_prefix: str
    schema_version: int
    scope_vocabulary: list = field(default_factory=list)


def config_path(warehouse_root):
    return Path(warehouse_root) / CONFIG_FILENAME


def save_config(warehouse_root, cfg):
    _validate(cfg)
    payload = {
        "project_prefix": cfg.project_prefix,
        "schema_version": cfg.schema_version,
        "scope_vocabulary": list(cfg.scope_vocabulary),
    }
    config_path(warehouse_root).write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def load_config(warehouse_root):
    path = config_path(warehouse_root)
    if not path.exists():
        raise ConfigError(f"no manifest at {path} — not an initialised warehouse root")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"manifest is not valid JSON: {path} ({exc})") from exc
    if not isinstance(raw, dict) or set(raw) != set(_MANIFEST_KEYS):
        raise ConfigError(
            f"manifest keys must be exactly {_MANIFEST_KEYS}, got: {sorted(raw)}"
            if isinstance(raw, dict)
            else "manifest root must be a JSON object"
        )
    cfg = WarehouseConfig(
        project_prefix=raw["project_prefix"],
        schema_version=raw["schema_version"],
        scope_vocabulary=raw["scope_vocabulary"],
    )
    _validate(cfg)
    return cfg


def _validate(cfg):
    if not isinstance(cfg.project_prefix, str) or not PREFIX_RE.match(cfg.project_prefix):
        raise ConfigError(
            f"invalid project prefix {cfg.project_prefix!r}: must match [a-z][a-z0-9]*"
        )
    if (
        not isinstance(cfg.schema_version, int)
        or isinstance(cfg.schema_version, bool)
        or cfg.schema_version < 1
    ):
        raise ConfigError(f"schema_version must be a positive integer, got {cfg.schema_version!r}")
    if not isinstance(cfg.scope_vocabulary, list):
        raise ConfigError("scope_vocabulary must be a list")
    seen = set()
    for value in cfg.scope_vocabulary:
        if not isinstance(value, str) or not _SCOPE_RE.match(value):
            raise ConfigError(f"invalid scope value {value!r}: must match [a-z][a-z0-9-]*")
        if value in seen:
            raise ConfigError(f"duplicate scope value: {value!r}")
        seen.add(value)
