from typing import Optional
from pathlib import Path
import logging

from noteeds.util.io import read_file

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, path: Path):
        self._path: Path = path
        self._files: Optional[list[str]] = None
        self._file_contents = {}

        if not path.is_dir():
            logger.error("%s is not a directory", (path, ))

    @property
    def path(self) -> Path:
        return self._path

    @staticmethod
    def accept_file(path: Path) -> bool:
        if not path.is_file():
            return False
        if path.name[0] == ".":
            return False
        else:
            return True

    def list_files(self):
        if self._files is None:
            # TODO walk subdirectories ("**/*"), but make sure to exclude
            # directories starting with ".".
            all_files = self._path.glob("*")
            self._files = [file for file in all_files if self.accept_file(file)]

        return self._files
