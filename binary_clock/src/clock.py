#! /usr/bin/python 3.8
import os
import time
import colorama


def int_to_binary(value: int) -> str:

    def _bin(value: int, bin_str: str) -> str:
        if not value:
            return bin_str
        return _bin(value // 2, ''.join([bin_str, str(value % 2)]))

    return _bin(value, '')[::-1]


def format_bin(seed: str, length: int = 16) -> str:
    boost = length - len(seed)
    return ''.join(["0" * boost, seed]) if boost > 0 else seed[-length:]


def print_bar(on: int, x: int, y: int, width: int, height: int) -> None:
    char = "@" * width if on else "-" * width
    for idx in range(0, height):
        print(f'{loc_cursor(x, y + idx)}{char}')
    return


def loc_cursor(x: int, y: int) -> str:
    return f"\033[{y};{x}f"


def clear_screen() -> None:
    os.system("cls||clear")


def print_timer(bin_time: str, offset: int = 1) -> None:
    segs = [bin_time[idx:idx + 4] for idx in range(0, len(bin_time), 4)]
    for col, seg in enumerate(segs):
        for row, value in enumerate(seg):
            print_bar(int(value), col * 20, row + offset, 15, 1)


if __name__ == '__main__':
    colorama.init(autoreset=True)
    clear_screen()
    count = 0
    while count < 600:
        bin_time = format_bin(int_to_binary(count), 16)
        print_timer(bin_time, 5)
        count += 1
        time.sleep(1)
