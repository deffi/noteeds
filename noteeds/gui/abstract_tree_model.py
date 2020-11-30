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

    This model doesn't currently support model changes apart from resetModel.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._internal_values: dict[tuple, tuple] = {}

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

    # *** Location bookkeeping

    # noinspection PyMethodMayBeStatic
    def location(self, index: QModelIndex) -> tuple[int]:
        if index.isValid():
            return index.internalPointer()
        else:
            return tuple()

    # noinspection PyMethodOverriding
    def createIndex(self, row: int, column: int, ptr: Any) -> QModelIndex:
        # As stated by the QAbstractItemModel.createIndex documentation, we must
        # keep the value use for the internal pointer alive, because the
        # QModelIndex won't do it.
        # The way we do this is to store all values ever created. Obviously, we
        # don't want to store multiple copies of a given value, so we could use
        # a set. HOWEVER, we will be creating the same values over and over
        # again, and we must not use a value we're not storing. So we use a dict
        # that maps each value to itself, and when we created a value that we
        # already have, we use the original instance of that value.

        if ptr in self._internal_values:
            ptr = self._internal_values[ptr]
        else:
            self._internal_values[ptr] = ptr

        return super().createIndex(row, column, ptr)

    # *** QAbstractItemModel methods

    def columnCount(self, index: QModelIndex = QModelIndex()) -> int:
        location = self.location(index)
        return self.tree_column_count(location)

    def rowCount(self, index: QModelIndex = QModelIndex()):
        location = self.location(index)
        return self.tree_child_count(index.internalPointer() or location)

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()):
        parent_location = self.location(parent)
        child_location = parent_location + (row, )
        return self.createIndex(row, column, child_location)

    # noinspection PyMethodOverriding
    def parent(self, child: QModelIndex) -> QModelIndex:
        location = self.location(child)
        if len(location) < 2:
            return QModelIndex()
        else:
            parent_location = location[:-1]
            return self.createIndex(location[-2], 0, parent_location)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        location = self.location(index)
        return self.tree_data(location, index.column(), role)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None) -> Any:
        return self.tree_header_data(section, orientation, role)
