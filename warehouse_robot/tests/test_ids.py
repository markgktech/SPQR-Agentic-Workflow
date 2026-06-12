import unittest

from warehouse_robot.errors import IdError
from warehouse_robot.ids import format_id, parse_id


class ParseIdTests(unittest.TestCase):
    def test_round_trip(self):
        for node_id, parts in [
            ("food-n23", ("food", "n", 23)),
            ("demo-f1", ("demo", "f", 1)),
            ("a1-n999", ("a1", "n", 999)),
        ]:
            self.assertEqual(parse_id(node_id), parts)
            self.assertEqual(format_id(*parts), node_id)

    def test_rejects_malformed_ids(self):
        for bad in [
            "food-x23",      # unknown plane marker
            "food-n0",       # numbers start at 1
            "food-n01",      # no leading zeros
            "Food-n23",      # uppercase prefix
            "food_n23",      # wrong separator
            "foodn23",       # missing separator
            "food-n23 ",     # trailing space
            "food-d23",      # kind is never encoded in the ID (S3)
            "",
            "n23",
        ]:
            with self.assertRaises(IdError, msg=bad):
                parse_id(bad)

    def test_format_rejects_bad_parts(self):
        with self.assertRaises(IdError):
            format_id("Food", "n", 1)
        with self.assertRaises(IdError):
            format_id("food", "d", 1)
        with self.assertRaises(IdError):
            format_id("food", "n", 0)
        with self.assertRaises(IdError):
            format_id("food", "n", True)


if __name__ == "__main__":
    unittest.main()
