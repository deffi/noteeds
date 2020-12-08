from typing import Optional, Any

from PySide2.QtCore import Qt, QModelIndex, QObject
from PySide2.QtGui import QFont

from noteeds.engine import SearchResult, FileEntry
from noteeds.util import AbstractTreeModel


class SearchResultModel(AbstractTreeModel):
    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)

        self._name_prefix         : Optional[list[FileEntry]] = []
        self._name_anywhere       : Optional[list[FileEntry]] = []
        self._contents_word       : Optional[list[FileEntry]] = []
        self._contents_word_prefix: Optional[list[FileEntry]] = []
        self._contents_anywhere   : Optional[list[FileEntry]] = []

        self._lists: list[list[FileEntry]] = [
            self._name_prefix,
            self._name_anywhere,
            self._contents_word,
            self._contents_word_prefix,
            self._contents_anywhere,
        ]

        self._list_descriptions: list[str] = [
            "Name prefix",
            "Name anywhere",
            "Contents word",
            "Contents word prefix",
            "Contents anywhere",
        ]

        self._list_description_font = QFont()
        self._list_description_font.setBold(True)

    def set_result(self, result: SearchResult) -> None:
        self.beginResetModel()

        self._name_prefix         [:] = list(sorted(result.name_prefix))
        self._name_anywhere       [:] = list(sorted(result.name_anywhere))
        self._contents_word       [:] = list(sorted(result.contents_word))
        self._contents_word_prefix[:] = list(sorted(result.contents_word_prefix))
        self._contents_anywhere   [:] = list(sorted(result.contents_anywhere))

        self.endResetModel()

    ##########
    # Access #
    ##########

    def file_entry(self, index: QModelIndex) -> Optional[FileEntry]:
        location = self.location(index)
        if len(location) == 2:
            return self._lists[location[0]][location[1]]
        else:
            return None

    ##############################
    # QAbstractItemModel methods #
    ##############################

    def tree_column_count(self, location: tuple[int]) -> int:
        return 1

    def tree_child_count(self, location: tuple[int]) -> int:
        if len(location) == 0:
            # Root index -> number of lists
            return len(self._lists)
        elif len(location) == 1:
            # List -> number of items in that list
            return len(self._lists[location[0]])
        else:
            # File -> 0
            return 0

    def tree_data(self, location: tuple[int], column: int, role: int = Qt.DisplayRole) -> Any:
        if role == Qt.DisplayRole:
            if len(location) == 1:
                # List -> list description
                return self._list_descriptions[location[0]]
            elif len(location) == 2:
                # Entry -> file name
                return self._lists[location[0]][location[1]].absolute_path.name
        elif role == Qt.FontRole:
            if len(location) == 1:
                return self._list_description_font

        elif role == Qt.BackgroundColorRole:
            if len(location) == 2:
                return self._lists[location[0]][location[1]].repository.config.color

    def tree_header_data(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "File"
