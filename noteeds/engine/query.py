import re
from dataclasses import dataclass, field
from typing import Optional, Pattern


@dataclass(frozen=True)
class Query:
    """
    Case sensitivity can be True, False, or None. None means automatic - true if
    text contains an uppercase letter, false otherwise. If flags includes
    re.IGNORECASE, it will be ignored.
    """

    text: str
    is_regex: bool
    case_sensitive: Optional[bool]
    flags: int = 0

    effective_regex: str           = field(init=False, compare=False)
    effective_case_sensitive: bool = field(init=False, compare=False)
    effective_flags: int           = field(init=False, compare=False)

    anywhere_pattern:    Pattern = field(init=False, compare=False)
    beginning_pattern:   Pattern = field(init=False, compare=False)
    word_pattern:        Pattern = field(init=False, compare=False)
    word_prefix_pattern: Pattern = field(init=False, compare=False)

    def __post_init__(self):
        sa = object.__setattr__

        if self.is_regex:
            effective_regex = self.text
        else:
            effective_regex = re.escape(self.text)

        if self.case_sensitive is None:
            effective_case_sensitive = any(character.isupper() for character in self.text)
        else:
            effective_case_sensitive = self.case_sensitive

        effective_flags = self.flags & ~re.IGNORECASE
        if not effective_case_sensitive:
            effective_flags = effective_flags | re.IGNORECASE

        sa(self, "effective_regex",          effective_regex)
        sa(self, "effective_case_sensitive", effective_case_sensitive)
        sa(self, "effective_flags",          effective_flags)

        sa(self, "anywhere_pattern"   , re.compile(        effective_regex,         effective_flags))
        sa(self, "beginning_pattern"  , re.compile("^"   + effective_regex,         effective_flags))
        sa(self, "word_pattern"       , re.compile("\\b" + effective_regex + "\\b", effective_flags))
        sa(self, "word_prefix_pattern", re.compile("\\b" + effective_regex,         effective_flags))
