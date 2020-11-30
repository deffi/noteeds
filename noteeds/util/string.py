from textwrap import fill
from typing import Optional, Pattern, Iterator


def map_lines(function, text: str) -> str:
    lines = text.splitlines()
    lines = map(function, lines)
    return "\n".join(lines)


def strip_lines(text: str) -> str:
    return map_lines(str.strip, text)


def box(text: str, character: str, border_width: int = 2) -> list[str]:
    border = character * border_width
    text_line = f"{border} {text} {border}"
    border_line = character * len(text_line)
    return [border_line, text_line, border_line]


# def find_occurrences(self, text, file_name):
#     file_contents = self.get_file_contents(file_name)
#     p = re.compile(re.escape(text), re.IGNORECASE)
#     return [m.span() for m in p.finditer(file_contents)]


def join_lines(lines: Iterator[str], width: Optional[int] = None) -> str:
    if width:
        lines = (fill(line, width=width) for line in lines)
    return "\n".join(lines)


def prefix_lines(lines: Iterator[str], prefix: str) -> Iterator[str]:
    return (prefix + line for line in lines)


def grep(pattern: Pattern, lines: list[str]) -> Iterator[str]:
    return (line for line in lines if pattern.search(line))
