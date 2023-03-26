import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor

from noteeds.engine import FileEntry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    name: Optional[str]
    root: Optional[Path]
    color: Optional[QColor]
    enabled: bool

    def store(self, settings: QSettings):
        settings.setValue("name", self.name)
        settings.setValue("root", str(self.root) if self.root else "")
        settings.setValue("color", self.color if self.color and self.color.isValid() else "")
        settings.setValue("enabled", self.enabled)

    @classmethod
    def load(cls, settings: QSettings):
        name = settings.value("name", None)
        root = settings.value("root", None)
        color = settings.value("color", None)
        enabled = settings.value("enabled", True, bool)

        if root:
            root = Path(root)
        if color:
            color = QColor(color)

        return cls(name, root, color, enabled)


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
