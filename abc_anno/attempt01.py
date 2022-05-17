from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Parent(ABC):
    @abstractmethod
    def method_string(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def method_int(self) -> int:
        raise NotImplementedError()


class ChildOne(Parent):
    def method_string(self) -> str:
        return "hello"

    def method_int(self) -> int:
        return 0


class ChildTwo(Parent):
    def method_string(self) -> str:
        return "Goodbye"

    def method_int(self) -> int:
        return 1

    def method_bool(self) -> bool:
        return False


def getChild(number: int) -> Parent:
    return ChildTwo() if number else ChildOne()


def getChilren(number: int) -> list[Parent]:
    if number:
        return [ChildTwo() for _ in range(10)]
    return [ChildOne() for _ in range(10)]
