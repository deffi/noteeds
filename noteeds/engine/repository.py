from typing import Optional
from pathlib import Path
import logging

from noteeds.engine import FileEntry

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, root: Path):
        self._root: Path = root
        self._entries: Optional[list[FileEntry]] = None

        if not root.is_dir():
            logger.error("%s is not a directory", (root,))

    @property
    def root(self) -> Path:
        return self._root

    @staticmethod
    def _accept(path: Path) -> bool:
        if not path.is_file():
            return False
        if path.name[0] == ".":
            return False
        else:
            return True

    def _read(self) -> list[FileEntry]:
        # TODO walk subdirectories ("**/*"), but make sure to exclude
        # directories starting with ".".
        paths = self._root.glob("*")
        return [FileEntry(path) for path in paths if self._accept(path)]

    def entries(self) -> list[FileEntry]:
        if self._entries is None:
            self._entries = self._read()

        return self._entries
