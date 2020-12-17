#!/usr/bin/env python3.8
""" Something to keep my terminal busy
Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts

TODO:
- Don't use fixed width screen.
- Add a clock
"""
import os
import time
import argparse

from egg_afk_clock import fonts


def loc_cursor(x: int, y: int) -> str:
    return f"\033[{y};{x}f"


def out_of_bounds(x: int, y: int) -> bool:
    horz = 0 <= x <= 96
    vert = 0 <= y <= 30
    return not (horz and vert)


def print_block(x: int, y: int, block: str) -> None:
    for idx, row in enumerate(block.split("\n")):
        if out_of_bounds(x + len(row), y):
            raise Exception(f"Printing out of bounds; {x}, {y}")
        print(f"{loc_cursor(x, y + idx)}{row}")
    return None


def print_centered_blocks(
    segments: str, segment_length: int, row_start: int
) -> None:
    col_max = 96
    space = 3 * (len(segments) - 1)
    total_space = (len(segments) * segment_length) + (space)
    col_start = (col_max - total_space) // 2
    col_size = segment_length + 3

    for block_col, block in enumerate(segments):
        col = col_start + (col_size * block_col)
        print_block(col, row_start, block)

    return None


def args_to_seconds(args: list) -> int:
    """Converts command line args to total seconds

    Min return is 0, defaults to this on any issues.
    Max seconds is 359,999 (99 hours, 59 minutes, 59 seconds)
    If minutes are provided, seconds are limited to max 59
    if hours are provided, minutes and seconds are limited to max 59
    """
    args_list = [
        0,
        0,
        0,
    ] + args

    hours = args_list[-3] * 3600 if 0 < args_list[-3] < 100 else 0

    max_minutes = 60 if hours else 6000
    minutes = args_list[-2] * 60 if 0 < args_list[-2] < max_minutes else 0

    max_seconds = 60 if hours or minutes else 360_000
    seconds = args_list[-1] if 0 < args_list[-1] < max_seconds else 0

    return hours + minutes + seconds


def args_to_int(args: list) -> tuple:
    """ Convert augs to int or return empty """
    try:
        return tuple([int(i) for i in args])
    except ValueError:
        return ()


def int_to_font(number: int) -> list:
    """ Translate number to a group of fonts """
    if number < 10:
        blocks = [
            fonts.NUM_0,
            fonts.FONT_ENUM[str(number)],
        ]
    else:
        blocks = [
            fonts.FONT_ENUM[str(number)[0]],
            fonts.FONT_ENUM[str(number)[-1]],
        ]
    return blocks


def assemble_time_block(total_seconds: int) -> tuple:
    spacer = [
        fonts.CHAR_,
    ]
    hours = int_to_font(total_seconds // 3600)
    minutes = int_to_font((total_seconds % 3600) // 60)
    seconds = int_to_font((total_seconds % 3600) % 60)
    return tuple(hours + spacer + minutes + spacer + seconds)


def display_clock(seconds: int) -> None:
    block = assemble_time_block(seconds)
    print_centered_blocks(block, 8, 19)
    return None


def print_egg() -> None:
    block = [
        fonts.CHAR_E,
        fonts.CHAR_G,
        fonts.CHAR_G,
    ]
    print_centered_blocks(block, 8, 12)
    return None


def count_down(seconds: int) -> None:
    while seconds:
        display_clock(seconds)
        seconds -= 1
        time.sleep(1)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set a countdown timer by SS, MM SS, or HH MM SS."
    )
    parser.add_argument("inputs", metavar="N", type=int, nargs="+")

    args = parser.parse_args()

    seconds = args_to_seconds(args.inputs)

    os.system("cls||clear")
    print_egg()

    if seconds:
        count_down(seconds)

    return None


if __name__ == "__main__":
    main()
