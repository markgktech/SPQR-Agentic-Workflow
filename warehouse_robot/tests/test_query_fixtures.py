"""The fixture query set (A4) — the golden-set / IR-harness seed.

Drives every entry in warehouse_robot/fixtures/queries.json against one
disposable instance built from the versioned fixtures, and asserts that each
query surfaces exactly the expected set of node ids. Order is the unit tests'
job; this set guards end-to-end recall and precision across the four verbs.
"""

import json
import tempfile
import unittest
from pathlib import Path

from . import _query_helpers as q

QUERIES_FILE = (
    Path(__file__).resolve().parent.parent / "fixtures" / "queries.json"
)


def _surfaced_ids(verb, response):
    key = "candidates" if verb in ("open_scope", "find") else "nodes"
    return [item["id"] for item in response.get(key, [])]


def _run(wroot, session, spec):
    verb, intent, params = spec["verb"], spec["intent"], spec["params"]
    if verb == "open_scope":
        return q.q_open(wroot, session=session, intent=intent, **params)
    if verb == "find":
        text = dict(params)
        return q.q_find(wroot, text.pop("text"), session=session,
                        intent=intent, **text)
    if verb == "fetch":
        return q.q_fetch(wroot, params["ids"], session=session, intent=intent)
    if verb == "traverse":
        rest = dict(params)
        node_id, edge_type = rest.pop("id"), rest.pop("edge_type")
        return q.q_traverse(wroot, node_id, edge_type, session=session,
                            intent=intent, **rest)
    raise AssertionError(f"unknown verb in fixture query set: {verb!r}")


class FixtureQuerySetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.wroot = q.build_instance(cls._tmp.name)
        cls.specs = json.loads(QUERIES_FILE.read_text())["queries"]

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_query_set_is_non_trivial(self):
        # Guards against an empty/parse-broken fixture file silently passing.
        self.assertGreaterEqual(len(self.specs), 20)
        verbs = {s["verb"] for s in self.specs}
        self.assertEqual(verbs, {"open_scope", "find", "fetch", "traverse"})

    def test_every_fixture_query_surfaces_its_expected_ids(self):
        for i, spec in enumerate(self.specs):
            with self.subTest(query=spec["name"]):
                session = f"fx-{i}"
                response = _run(self.wroot, session, spec)

                self.assertCountEqual(
                    _surfaced_ids(spec["verb"], response),
                    spec["expect_ids"],
                    f"{spec['name']}: surfaced id set mismatch",
                )
                if "expect_not_found" in spec:
                    self.assertCountEqual(
                        response.get("not_found", []), spec["expect_not_found"]
                    )
                if "expect_auto_broadened" in spec:
                    self.assertEqual(
                        response.get("auto_broadened"),
                        spec["expect_auto_broadened"],
                    )
                if "expect_view" in spec:
                    self.assertEqual(response.get("view"), spec["expect_view"])

                q.q_verdict(self.wroot, "FOUND-ENOUGH", session=session)


if __name__ == "__main__":
    unittest.main()
