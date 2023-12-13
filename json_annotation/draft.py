from __future__ import annoations

from collections.abc import Iterable
from collections.abc import Mapping
from typing import Union

_JsonTypes = Union[
    str, int, float, bool, None, "Iterable[_JsonTypes]", "Mapping[str, _JsonTypes]"
]
JSONType = Union["Mapping[str, _JsonTypes]", "Iterable[_JsonTypes]"]

