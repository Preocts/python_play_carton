""" Tests for Parsers

Author: Preocts <preocts@gmail.com>
Discord: Preocts#8196
Git: https://www.github.com/Preocts
"""
import unittest
from eggdo import parser


class TestParsers(unittest.TestCase):

    def test_remove_lines(self):
        """ Max of 1 new line between lines """
        mock_input = "title\n\n\nword\nmorewords\n\neven more words"
        expected_output = "title\nword\nmorewords\neven more words"

        self.assertEqual(parser.remove_lines(mock_input), expected_output)

        mock_input = "\nThis is just a really long sentence with no \n"
        expected_output = "This is just a really long sentence with no"
        self.assertEqual(parser.remove_lines(mock_input), expected_output)

        mock_input = ("\n\n\n\n\n\n\n\n\n\n\n\n\n")
        expected_output = ""
        self.assertEqual(parser.remove_lines(mock_input), expected_output)

    def test_remove_extra_dashes(self):
        """ Max of 2 dashes, min of 0 """
        mock_input = "the\n-\ntest\n-\nis\n-\nhere"
        expected_output = "the\n-\ntest\n-\nis\n\nhere"
        self.assertEqual(parser.remove_dashes(mock_input), expected_output)

        mock_input = "the\ntest\nis\nhere"
        expected_output = "the\ntest\nis\nhere"
        self.assertEqual(parser.remove_dashes(mock_input), expected_output)
