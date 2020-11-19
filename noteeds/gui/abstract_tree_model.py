from typing import Any

from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt


class AbstractTreeModel(QAbstractItemModel):
    """The location of a node in the tree is described by a tuple of indices.
    The length of the tuple corresponds to the depth of the node in the tree,
    and the tuple element corresponds to the index of the respective ancestor.

        (root)       -> ()
        |- ...       -> (0)
        |  |- ...    -> (0, 1)
        |  |  '- ... -> (0, 1, 0)
        |  '- ...    -> (0, 2)
        '- ...       -> (1)
           '- ...    -> (1, 1)
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._collection = {}

    def _collect(self, x):
        if x not in self._collection:
            self._collection[x] = x
        return self._collection[x]

    # *** Abstract methods

    def tree_column_count(self, location: tuple[int]) -> int:
        """Columns of the children"""
        raise NotImplementedError

    def tree_child_count(self, location: tuple[int]) -> int:
        raise NotImplementedError

    def tree_data(self, location: tuple[int], column: int, role: int = Qt.DisplayRole) -> Any:
        raise NotImplementedError

    def tree_header_data(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        return None

    # *** QAbstractItemModel methods

    def location(self, index: QModelIndex) -> tuple[int]:
        if index.isValid():
            return index.internalPointer()
        else:
            return tuple()

    def columnCount(self, index: QModelIndex = QModelIndex()) -> int:
        location = self.location(index)
        return self.tree_column_count(location)

    def rowCount(self, index: QModelIndex = QModelIndex()):
        location = self.location(index)
        return self.tree_child_count(index.internalPointer() or location)

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()):
        parent_location = self.location(parent)
        child_location = self._collect(parent_location + (row, ))
        return self.createIndex(row, column, child_location)

    def parent(self, child: QModelIndex) -> QModelIndex:
        location = self.location(child)
        if len(location) < 2:
            return QModelIndex()
        else:
            parent_location = self._collect(location[:-1])
            return self.createIndex(location[-2], 0, parent_location)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        location = self.location(index)
        return self.tree_data(location, index.column(), role)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None):
        return self.tree_header_data(section, orientation, role)
