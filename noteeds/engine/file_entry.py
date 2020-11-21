from typing import Optional
from pathlib import Path

from noteeds.util.io import read_file


class FileEntry:
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
        # # TODO make configurable for debugging purposes
        # from time import sleep
        # from random import randrange
        # if randrange(20) == 0:
        #     sleep(0.01)

        return read_file(self.absolute_path)

    def contents(self) -> str:
        if self._contents is None:
            self._contents, _ = self._read()

        return self._contents
