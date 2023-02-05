from __future__ import annotations

import re
from datetime import datetime

# Year as YYYY
YEAR = str(datetime.now().year)
BOXES = {
    # Little boxes on the hillside, little boxes made of ticky-tacky
    "about": "\n".join(
        [
            '<div class="WordBox SanSerifFonts">',
            '\t<p class="CardTitle">About</p>',
            '\t<p class="CardBody">{content}</p>',
            "</div>",
        ],
    ),
    "notes": "\n".join(
        [
            '<div class="WordBox SanSerifFonts">',
            '\t<p class="CardTitle">Author Notes</p>',
            '\t<p class="CardBody">{content}</p>',
            "</div>",
        ],
    ),
}
CONTENT_START = '<div class="WordBox SanSerifFonts">'
CONTENT_END = "</div>"
HEADER = {
    "title": '<h1 class="Center SmallCaps">{content}</h1>',
    "collection": '<h3 class="Center SmallCaps">{content}</h3>',
    "copyright": '<h4 class="Center">&copy; ' + YEAR + " - {content}</h4>",
}
SPACER = "<p><br /></p>"


def trim_spaces(text: str) -> str:
    """Remove leading and trailing spaces."""
    return text.strip()


def format_line(line: str) -> str:
    """Format a line of text."""
    return trim_spaces(line.strip("\n"))


def create_boxes(lines: list[str]) -> str:
    """Create boxes from list of lines."""
    boxes: list[str] = []
    for box, body in BOXES.items():
        for line in lines:
            if line.lower().startswith(f":{box}:"):
                clean_line = re.sub(rf":{box}:", "", line, flags=re.IGNORECASE)
                content = format_line(clean_line)
                boxes.append(body.format(content=content))
                boxes.append("\n")
    return "\n".join(boxes)


def create_header(lines: list[str]) -> str:
    """Create header of text."""
    headers: list[str] = []
    for header, body in HEADER.items():
        for line in lines:
            if line.lower().startswith(f":{header}:"):
                clean_line = re.sub(rf":{header}:", "", line, flags=re.IGNORECASE)
                content = format_line(clean_line)
                headers.append(body.format(content=content))
    return "\n".join(headers) + "\n"


def main() -> int:
    """Main function."""
    with open("in.txt", "r") as infile:
        lines = infile.readlines()

    new_lines: list[str] = []
    new_lines.append(create_boxes(lines))
    new_lines.append(CONTENT_START + "\n")
    new_lines.append(create_header(lines))
    new_lines.append(SPACER + "\n")
    for line in lines:
        if line and not line.startswith(":"):
            new_lines.append(f"<p>{format_line(line)}</p>\n")
    new_lines.append(SPACER + "\n")
    new_lines.append(CONTENT_END + "\n")

    new_lines = [line for line in new_lines if line != "<p></p>\n" and line]
    with open("out.txt", "w") as outfile:
        outfile.writelines(new_lines)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
