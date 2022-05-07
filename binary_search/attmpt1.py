"""https://leetcode.com/problems/first-bad-version/"""
from random import randint


def isBadVersion(version: int) -> bool:
    return version >= BAD_VERSION


def firstBadVersion(upper_limit: int) -> int:

    lower_limit = 1
    middle = upper_limit // 2

    while upper_limit >= lower_limit:
        if isBadVersion(middle):
            upper_limit = middle - 1
        else:
            lower_limit = middle + 1

        middle = (upper_limit + lower_limit) // 2

    return middle + 1


BAD_VERSION = 1
assert firstBadVersion(1) == BAD_VERSION
BAD_VERSION = 1
assert firstBadVersion(2) == BAD_VERSION
BAD_VERSION = 1
assert firstBadVersion(1_000) == BAD_VERSION
BAD_VERSION = 1_000
assert firstBadVersion(1_000) == BAD_VERSION
BAD_VERSION = randint(1, 2 ** 32)
assert firstBadVersion(2 ** 32) == BAD_VERSION
print("All good")
