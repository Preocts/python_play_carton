from __future__ import annotations

import re


class StringUtils:
    @staticmethod
    def clean_split(text: str, delimiter: str = ",") -> list[str]:
        """Split text on delimeter, strips leading/trailing whitespace."""
        return [seg.strip() for seg in text.split(delimiter)] if text else []

    @staticmethod
    def clean_space(text: str) -> str:
        """Remove extra whitespace throughout the string."""
        return re.sub(r"\s+", " ", text.strip())

    @staticmethod
    def to_dash(text: str) -> str:
        """Replace spaces with dashes, trim leading/trailing whitespace."""
        text = re.sub(r"\s+", "-", text.strip())
        return re.sub("--+", "-", text)
