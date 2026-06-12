import json
import tempfile
import unittest
from pathlib import Path

from warehouse_robot.config import WarehouseConfig, load_config, save_config
from warehouse_robot.errors import ConfigError


class ConfigTests(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = WarehouseConfig("demo", 1, ["architecture", "data-layer"])
            save_config(tmp, cfg)
            self.assertEqual(load_config(tmp), cfg)

    def test_missing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ConfigError):
                load_config(tmp)

    def test_rejects_bad_manifests(self):
        cases = [
            '{"project_prefix": "demo"}',                       # missing keys
            '{"project_prefix": "demo", "schema_version": 1, '
            '"scope_vocabulary": [], "extra": 1}',              # extra key
            '{"project_prefix": "Demo", "schema_version": 1, '
            '"scope_vocabulary": []}',                          # bad prefix
            '{"project_prefix": "demo", "schema_version": 0, '
            '"scope_vocabulary": []}',                          # bad version
            '{"project_prefix": "demo", "schema_version": 1, '
            '"scope_vocabulary": ["A"]}',                       # bad scope value
            '{"project_prefix": "demo", "schema_version": 1, '
            '"scope_vocabulary": ["a", "a"]}',                  # duplicate scope
            "not json",
            "[]",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "warehouse.config.json"
            for raw in cases:
                path.write_text(raw, encoding="utf-8")
                with self.assertRaises(ConfigError, msg=raw):
                    load_config(tmp)

    def test_save_rejects_invalid_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ConfigError):
                save_config(tmp, WarehouseConfig("BAD", 1, []))
            self.assertFalse((Path(tmp) / "warehouse.config.json").exists())

    def test_manifest_is_stable_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_config(tmp, WarehouseConfig("demo", 1, []))
            raw = json.loads((Path(tmp) / "warehouse.config.json").read_text(encoding="utf-8"))
            self.assertEqual(
                raw,
                {"project_prefix": "demo", "schema_version": 1, "scope_vocabulary": []},
            )


if __name__ == "__main__":
    unittest.main()
