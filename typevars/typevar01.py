from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TypeVar

ConfigBase = TypeVar("ConfigBase", bound="Base")


class Base(ABC):
    @abstractmethod
    def foo(self) -> None:
        pass


class Derived(Base):
    def foo(self) -> None:
        pass

    def bar(self) -> None:
        pass


class Provider:
    def __init__(self, class_type: type) -> None:
        self.class_type = class_type
        self.bar: dict[str, Base] = {}

    def get(self) -> ConfigBase:
        return self.class_type()


if __name__ == "__main__":
    provider = Provider(Derived)

    # Incompatible types in assignment
    # (expression has type "Base", variable has type "Derived")
    my_class: Derived = provider.get()
    my_class.bar()
