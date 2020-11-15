def map_lines(function, text: str) -> str:
    lines = text.splitlines()
    lines = map(function, lines)
    return "\n".join(lines)


def strip_lines(text: str) -> str:
    return map_lines(str.strip, text)


def box(text: str, character: str, border_width: int = 2) -> str:
    border = character * border_width
    text_line = f"{border} {text} {border}"
    border_line = character * len(text_line)
    return "\n".join([border_line, text_line, border_line])
