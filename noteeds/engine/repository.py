from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import logging

from PySide2.QtGui import QColor

from noteeds.engine import FileEntry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    name: Optional[str]
    root: Optional[Path]
    color: Optional[QColor]
    enabled: bool


class Repository:
    def __init__(self, config: Config):
        self._config: Config = config

        self._entries: Optional[set[FileEntry]] = None

        if not config.root.is_dir():
            logger.error("%s is not a directory", (config.root,))

    @property
    def config(self):
        return self._config

    @staticmethod
    def _accept(path: Path) -> bool:
        if not path.is_file():
            return False
        if path.name[0] == ".":
            return False
        else:
            return True

    def _read(self) -> set[FileEntry]:
        # TODO walk subdirectories ("**/*"), but make sure to exclude
        # directories starting with ".".
        paths = self.config.root.glob("*")
        return set(FileEntry(path, self) for path in paths if self._accept(path))

    def entries(self) -> set[FileEntry]:
        if self._entries is None:
            self._entries = self._read()

        return self._entries
