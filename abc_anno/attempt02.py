from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence


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


def getChildOne(number: int) -> Sequence[ChildOne]:
    return [ChildOne() for _ in range(number)]


def getChildTwo(number: int) -> Sequence[ChildTwo]:
    return [ChildTwo() for _ in range(number)]


def get_children(number: int) -> Sequence[Parent]:
    if number:
        return [ChildTwo() for _ in range(10)]
    return [ChildOne() for _ in range(10)]


def new_children(preference: int) -> Sequence[Parent]:
    if preference == 1:
        # mypy Type error
        # Incompatible return value type (got"List[ChildOne] expected "List[Parent]")
        return getChildOne(10)
    elif preference == 2:
        # Incompatible return value type (got"List[ChildTwo] expected "List[Parent]")
        return getChildTwo(10)
    else:
        raise ValueError("Your choice isn't valid. Smile.")
