from typing import Dict

import pytest

import mrepr


@pytest.mark.parametrize(
    ("in_", "keypairs", "expected"),
    (
        ("{{metatag}}", {"metatag": "replaced"}, "replaced"),
        ("{{metaTag }}", {"metatag": "replaced"}, "replaced"),
        ("{{ metaTag}}", {"metatag": "replaced"}, "replaced"),
        ("{{ metaTag }}", {"metatag": "replaced"}, "replaced"),
        ("{{metatag}} ", {"metatag": "replaced"}, "replaced "),
        (" {{Metatag}}", {"metatag": "replaced"}, " replaced"),
        (" {{ metatag }} ", {"metatag": "replaced"}, " replaced "),
        ("This{{metatag}}sentence", {"metatag": "replaced"}, "Thisreplacedsentence"),
        (
            "This {{ metatag }} sentence",
            {"metatag": "replaced"},
            "This replaced sentence",
        ),
        (
            "This {{ metatag }} sentence",
            {"metatag": "replaced"},
            "This replaced sentence",
        ),
        (
            "This {{ newtag }} sentence",
            {"metatag": "replaced"},
            "This {{ newtag }} sentence",
        ),
        (
            "This {{ newtag }}{{metatag}} sentence",
            {"metatag": "replaced", "newtag": "swapped"},
            "This swappedreplaced sentence",
        ),
    ),
)
def test_mrepr(in_: str, keypairs: Dict[str, str], expected: str) -> None:
    """Test metatag repr"""
    assert mrepr.mrepr(in_, keypairs) == expected
