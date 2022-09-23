from __future__ import annotations

import pytest
from stringutil import StringUtils


@pytest.mark.parametrize(
    ("text", "expected"),
    (
        ("1, 2,\t 3", ["1", "2", "3"]),
        ("1,2,3", ["1", "2", "3"]),
        ("", []),
    ),
)
def test_clean_split(text: str, expected: list[str]) -> None:
    result = StringUtils.clean_split(text)
    assert result == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    (
        (" The egg\t rolls  awkwardly  ", "The egg rolls awkwardly"),
        ("", ""),
    ),
)
def test_clean_space(text: str, expected: str) -> None:
    result = StringUtils.clean_space(text)

    assert result == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    (
        (" The egg\t rolls  awkwardly  ", "The-egg-rolls-awkwardly"),
        ("This has a - dash - in it", "This-has-a-dash-in-it"),
        ("", ""),
    ),
)
def test_to_dash(text: str, expected: str) -> None:
    result = StringUtils.to_dash(text)

    assert result == expected
