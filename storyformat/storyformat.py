from __future__ import annotations

import argparse
import re
from datetime import datetime

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


def create_text_header(lines: list[str]) -> list[str]:
    """Create header for plain text."""
    headers: list[str] = []
    for line in lines:
        match = re.match(r"^(:.+:).*$", line)
        if match:
            label = match.group(1).lstrip(":")
            content = format_line(line.replace(match.group(1), "").strip())
            if label == "copyright:":
                headers.append(f"{label:<12}{content} ©{YEAR}\n")
            else:
                headers.append(f"{label:<12}{content}\n")
    return headers


def read_file(filename: str) -> list[str]:
    """Read a file and return its lines."""
    with open(filename, "r") as infile:
        return infile.readlines()


def save_file(filename: str, lines: list[str]) -> None:
    """Save a file."""
    with open(filename, "w") as outfile:
        outfile.writelines(lines)


def format_ao3(lines: list[str]) -> list[str]:
    """Format a story for AO3."""
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

    return [line for line in new_lines if line != "<p></p>\n" and line]


def format_txt(lines: list[str]) -> list[str]:
    """Format a story as plain text."""
    new_lines: list[str] = []
    new_lines.extend(create_text_header(lines))
    new_lines.append("\n***\n\n")
    for line in lines:
        if line.strip() and not line.startswith(":"):
            new_lines.append(f"{format_line(line)}\n\n")
    return new_lines


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="name of file to format", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    lines = read_file(args.filename)

    filestem = args.filename.split(".")[0]

    # Save Ao3 file
    save_file(f"{filestem}_ao3.txt", format_ao3(lines))

    # Save txt file
    save_file(f"{filestem}_txt.txt", format_txt(lines))

    raise SystemExit(0)
