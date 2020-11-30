from pathlib import Path
from random import uniform
from time import sleep
from typing import Optional

from noteeds.util.io import read_file


class FileEntry:
    load_delay: Optional[float] = None
    load_delay_probability: float = 1

    def __init__(self, path: Path, repository: "Repository"):
        self._absolute_path: Path = path
        self._repository: "Repository" = repository

        self._contents: Optional[str] = None

    def __eq__(self, other):
        return (isinstance(other, FileEntry)
                and other._absolute_path == self._absolute_path)

    def __hash__(self):
        return hash(self._absolute_path)

    def __lt__(self, other):
        # noinspection PyProtectedMember
        return self._absolute_path.__lt__(other._absolute_path)

    @property
    def absolute_path(self):
        return self._absolute_path

    @property
    def repository(self) -> "Repository":
        return self._repository

    def _read(self) -> str:
        if self.load_delay:
            if uniform(0, 1) <= self.load_delay_probability:
                sleep(self.load_delay)

        return read_file(self.absolute_path)

    def contents(self) -> str:
        if self._contents is None:
            self._contents, _ = self._read()

        return self._contents
