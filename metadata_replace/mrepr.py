import re
from typing import Dict


def mrepr(content: str, metadata: Dict[str, str]) -> str:
    """Replaces {{metadata}} by keypair: value"""
    for key, value in metadata.items():
        content = re.sub(fr"{{{{\s?{key}\s?}}}}", value, content, flags=re.I)
    return content
