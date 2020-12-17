#!/usr/bin/env python3.8
import unittest

from egg_afk_clock import eggclock
from egg_afk_clock import fonts


class TestMainFunctions(unittest.TestCase):
    def test_print_block(self):
        with self.assertRaises(Exception):
            eggclock.print_block(93, 0, "TEST")
            eggclock.print_block(0, 30, "TEST\nTEST")
        self.assertIsNone(eggclock.print_block(0, 0, "TEST"))

    def test_print_centered(self):
        badsegments = [
            fonts.CHAR_,
        ] * 12
        goodsegments = [
            fonts.CHAR_,
            fonts.CHAR_,
        ]
        with self.assertRaises(Exception):
            eggclock.print_centered_blocks(badsegments, 8, 0)
            eggclock.print_centered_blocks(goodsegments, 8, 20)
        self.assertIsNone(eggclock.print_centered_blocks(goodsegments, 8, 0))

    def test_out_of_bounds(self):
        self.assertFalse(eggclock.out_of_bounds(0, 0))
        self.assertFalse(eggclock.out_of_bounds(0, 30))
        self.assertFalse(eggclock.out_of_bounds(96, 0))
        self.assertFalse(eggclock.out_of_bounds(96, 30))

        self.assertTrue(eggclock.out_of_bounds(97, 0))
        self.assertTrue(eggclock.out_of_bounds(0, 31))

    def test_loc_cursor(self):
        self.assertEqual(eggclock.loc_cursor(1, 2), "\033[2;1f")


class TestConverts(unittest.TestCase):
    def test_single_cli_arguement(self):
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    359999,
                ]
            ),
            359999,
        )
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    360000,
                ]
            ),
            0,
        )
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    -1,
                ]
            ),
            0,
        )

    def test_double_cli_argument(self):
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    5999,
                    59,
                ]
            ),
            359999,
        )
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    6000,
                    15,
                ]
            ),
            15,
        )
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    5999,
                    60,
                ]
            ),
            359940,
        )
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    -1,
                    -1,
                ]
            ),
            0,
        )

    def test_triple_cli_argument(self):
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    99,
                    59,
                    59,
                ]
            ),
            359999,
        )
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    100,
                    59,
                    15,
                ]
            ),
            3555,
        )
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    99,
                    60,
                    15,
                ]
            ),
            356415,
        )
        self.assertEqual(
            eggclock.args_to_seconds(
                [
                    -1,
                    -1,
                    -1,
                ]
            ),
            0,
        )

    def test_args_convert_to_int(self):
        self.assertEqual(eggclock.args_to_int(["12", 12]), (12, 12))
        self.assertEqual(eggclock.args_to_int([12, 12]), (12, 12))
        self.assertEqual(eggclock.args_to_int(args=["12", "Clock"]), ())

    def test_int_to_font(self):
        self.assertEqual(
            eggclock.int_to_font(1),
            [
                fonts.NUM_0,
                fonts.NUM_1,
            ],
        )
        self.assertEqual(
            eggclock.int_to_font(10),
            [
                fonts.NUM_1,
                fonts.NUM_0,
            ],
        )

    def test_assemble_time_block(self):
        self.assertEqual(
            eggclock.assemble_time_block(1),
            (
                fonts.NUM_0,
                fonts.NUM_0,
                fonts.CHAR_,
                fonts.NUM_0,
                fonts.NUM_0,
                fonts.CHAR_,
                fonts.NUM_0,
                fonts.NUM_1,
            ),
        )
        self.assertEqual(
            eggclock.assemble_time_block(38715),
            (
                fonts.NUM_1,
                fonts.NUM_0,
                fonts.CHAR_,
                fonts.NUM_4,
                fonts.NUM_5,
                fonts.CHAR_,
                fonts.NUM_1,
                fonts.NUM_5,
            ),
        )
