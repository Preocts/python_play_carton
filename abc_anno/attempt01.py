from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Parent(ABC):
    @abstractmethod
    def method_string(self) -> str:
        raise NotImplementedError()


class ChildOne(Parent):
    def method_string(self) -> str:
        return "hello"


class ChildTwo(Parent):
    def method_string(self) -> str:
        return "Goodbye"


def getChild(number: int) -> Parent:
    return ChildTwo() if number else ChildOne()


def getChilren(number: int) -> list[Parent]:
    if number:
        return [ChildTwo() for _ in range(10)]
    return [ChildOne() for _ in range(10)]
