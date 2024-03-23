from __future__ import annotations

import re
import pytest
from collections.abc import Sequence


def parse_range(range_string: str) -> Sequence[int]:
    """
    Parse a range of numbers (inclusive) and provide a sorted sequence of ints.

    Valid ranges include:

    - Whole numbers only
    - Single values comma or space separated (1, 2, 3 4 5)
    - Range values using `-` or `to` (1-5 6 to 10)

    Underscore can be used for readability of large numbers. e.g. 1_000_000

    Args:
        range_string: A string of valid ranges.

    Raises:
        ValueError: When input provided cannot be parsed correctly
    """
    range_string = range_string.replace("_", "")
    range_string = range_string.replace(",", " ")
    range_string = range_string.replace("to", "-")
    range_string = re.sub(r"\s+", " ", range_string)
    range_string = re.sub(r"(\s+)?-(\s+)?", "-", range_string)

    sequence: list[int] = []

    for value in range_string.split():
        if "-" in value:
            start, stop = map(int, value.split("-"))
            step = 1 if start <= stop else -1
            sequence.extend(range(start, stop + step, step))

        else:
            sequence.append(int(value))

    return sorted(list(set(sequence)))


@pytest.mark.parametrize(
    "input, expected",
    [
        ("1", [1]),
        ("1, 2 ,4 5", [1, 2, 4, 5]),
        ("1-5", [1, 2, 3, 4, 5]),
        ("1-5, 8", [1, 2, 3, 4, 5, 8]),
        ("1-5, 8 to 10", [1, 2, 3, 4, 5, 8, 9, 10]),
        ("1-2,3,4,5,8   - 10, 11", [1, 2, 3, 4, 5, 8, 9, 10, 11]),
        ("1-5, 8,9,10, 11-15", [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15]),
        ("10-15, 1, 5, 2", [1, 2, 5, 10, 11, 12, 13, 14, 15]),
        ("1, 1, 1, 1, 1, 1, 1, 1", [1]),
        ("10-5, 1", [1, 5, 6, 7, 8, 9, 10]),
    ],
)
def test_parse_range(input, expected):
    assert parse_range(input) == expected


def test_parse_raises_on_real_number_input() -> None:
    with pytest.raises(ValueError):
        parse_range("1.1")
