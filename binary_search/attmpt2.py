from __future__ import annotations


def insert_index(ordered_list: list[int], number: int) -> int:
    """Find existing index of number or insertion index to maintain list order."""

    if number in ordered_list:
        return ordered_list.index(number)

    start, stop = 0, len(ordered_list) - 1
    point = (start + stop) // 2
    while start <= stop:
        if ordered_list[point] > number:
            stop = point - 1
        else:
            start = point + 1
        point = (start + stop) // 2

    return point + 1


assert insert_index([1, 3, 5, 7, 9], 5) == 2
assert insert_index([1, 3, 5, 7, 9], 6) == 3
assert insert_index([1], 2) == 1
assert insert_index([1], 0) == 0
assert insert_index([], 12) == 0
print("All good")
