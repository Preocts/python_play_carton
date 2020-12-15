#!/usr/bin/env python3.8
import unittest

from egg_afk_clock import eggclock


class TestConverts(unittest.TestCase):

    def test_single_cli_arguement(self):
        self.assertEqual(eggclock.args_to_seconds([359999, ]), 359999)
        self.assertEqual(eggclock.args_to_seconds([360000, ]), 0)
        self.assertEqual(eggclock.args_to_seconds([-1, ]), 0)

    def test_double_cli_argument(self):
        self.assertEqual(eggclock.args_to_seconds([5999, 59, ]), 359999)
        self.assertEqual(eggclock.args_to_seconds([6000, 15, ]), 15)
        self.assertEqual(eggclock.args_to_seconds([5999, 60, ]), 359940)
        self.assertEqual(eggclock.args_to_seconds([-1, -1, ]), 0)

    def test_triple_cli_argument(self):
        self.assertEqual(eggclock.args_to_seconds([99, 59, 59, ]), 359999)
        self.assertEqual(eggclock.args_to_seconds([100, 59, 15, ]), 3555)
        self.assertEqual(eggclock.args_to_seconds([99, 60, 15, ]), 356415)
        self.assertEqual(eggclock.args_to_seconds([-1, -1, -1, ]), 0)

    def test_args_convert_to_int(self):
        self.assertEqual(eggclock.args_to_int(["12", 12]), (12, 12))
        self.assertEqual(eggclock.args_to_int([12, 12]), (12, 12))
        self.assertEqual(eggclock.args_to_int(args=["12", "Clock"]), ())
