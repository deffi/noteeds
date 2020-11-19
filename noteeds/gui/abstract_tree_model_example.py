from typing import Any

from PySide2.QtCore import Qt

from noteeds.gui import AbstractTreeModel


class AbstractTreeModelExample(AbstractTreeModel):
    def __init__(self, parent, top_level_entries: int, columns: int):
        super().__init__(parent)
        self._top_level_entries = top_level_entries
        self._columns = columns

    def tree_column_count(self, location: tuple[int]) -> int:
        return self._columns

    def tree_child_count(self, location: tuple[int]) -> int:
        if len(location) < self._top_level_entries:
            return self._top_level_entries - len(location)
        else:
            return 0

    def tree_data(self, location: tuple[int], column: int, role: int = Qt.DisplayRole) -> Any:
        if role == Qt.DisplayRole:
            return f"{location} / {column}"

    def tree_header_data(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if role == Qt.DisplayRole:
            return str(section)
