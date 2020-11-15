from typing import Optional
from pathlib import Path

from noteeds.util.io import read_file


class FileEntry:
    def __init__(self, path: Path):
        self._absolute_path: Path = path
        self._contents: Optional[str] = None

    def __eq__(self, other):
        return (isinstance(other, FileEntry)
                and other._absolute_path == self._absolute_path)

    def __hash__(self):
        return hash(self._absolute_path)

    def __lt__(self, other):
        return self._absolute_path.__lt__(other._absolute_path)

    @property
    def absolute_path(self):
        return self._absolute_path

    def _read(self) -> str:
        # TODO factor in?
        return read_file(self.absolute_path)

    # TODO rename to content
    def contents(self) -> str:
        if self._contents is None:
            self._contents, _ = self._read()

        return self._contents
