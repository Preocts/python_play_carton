from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

HERE = Path(__file__)
FILE = HERE.parent / Path("test_logs.log")
# FILE = HERE.parent / Path("test_simple.log")


def read(filepath: Path) -> list[str]:
    with open(filepath) as infile:
        return [line for line in infile.read().split("\n") if line]


def print_logs() -> int:
    lines = read(FILE)

    for line in lines:
        print(line)

    return 0


def test_print_logs() -> None:
    expected_lines = read(FILE)

    with redirect_stdout(StringIO()) as con_capture:

        print_logs()

        clean_capture = [line for line in con_capture.getvalue().split("\n") if line]
        assert clean_capture == expected_lines


if __name__ == "__main__":
    raise SystemExit(print_logs())
