from typing import Optional, List

from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QTreeWidget
from PySide2.QtGui import QDragMoveEvent
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget, QTreeWidgetItem, QAbstractItemView

from noteeds.engine.repository import Config as RepoConfig
from noteeds.gui.settings import ColorDelegate, PathBrowseDelegate


class ReposTreeWidget(QTreeWidget):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

        self._add_repo_item: Optional[QTreeWidgetItem] = None

        # Settings
        self.setEditTriggers(QAbstractItemView.AllEditTriggers & ~QAbstractItemView.CurrentChanged)

        # Item delegates
        self.setItemDelegateForColumn(1, ColorDelegate(self))
        self.setItemDelegateForColumn(2, PathBrowseDelegate(self))

        # Item signal
        self.itemActivated.connect(self._item_activated)
        self.itemClicked.connect(self._item_activated)

    ##########
    # Widget #
    ##########

    def resize_columns_to_contents(self):
        for column in range(self.columnCount()):
            self.resizeColumnToContents(column)

    def selection_index(self):
        selected_items = self.selectedItems()
        if selected_items:
            return self.indexOfTopLevelItem(selected_items[0])
        else:
            return 0

    #########
    # Items #
    #########

    @staticmethod
    def _create_repo_item(repo: RepoConfig) -> QTreeWidgetItem:
        item = QTreeWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsEditable)

        item.setData(0, Qt.CheckStateRole, (Qt.Checked if repo.enabled else Qt.Unchecked))
        item.setText(0, repo.name or "")
        item.setData(1, Qt.DisplayRole, "")
        item.setData(1, Qt.DecorationRole, repo.color)
        item.setData(2, Qt.EditRole, str(repo.root))

        return item

    @staticmethod
    def _create_new_repo_item() -> QTreeWidgetItem:
        item = QTreeWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable | Qt.ItemIsUserCheckable
                      | Qt.ItemIsDragEnabled & ~Qt.ItemIsDropEnabled )

        item.setData(0, Qt.CheckStateRole, Qt.Checked)
        item.setText(0, "")
        item.setData(1, Qt.DisplayRole, "")
        item.setData(1, Qt.DecorationRole, None)
        item.setData(2, Qt.EditRole, "")

        return item

    @staticmethod
    def _create_add_item() -> QTreeWidgetItem:
        item = QTreeWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsUserCheckable
                      & ~Qt.ItemIsDragEnabled & ~Qt.ItemIsDropEnabled )

        item.setData(0, Qt.DisplayRole, "Add...")
        item.setData(0, Qt.TextColorRole, QColor (127, 127, 127))

        return item

    #########
    # Repos #
    #########

    def set_repos(self, repos: List[RepoConfig]) -> None:
        self.clear()
        for repo in repos:
            self.addTopLevelItem(self._create_repo_item(repo))

        self._add_repo_item = self._create_add_item()
        self.addTopLevelItem(self._add_repo_item)

    def get_repos(self) -> List[RepoConfig]:
        return []

    def add_repo(self, position: int):
        item = self._create_new_repo_item()
        self.insertTopLevelItem(position, item)

        self.clearSelection()
        self.setCurrentItem(item)
        item.setSelected(True)
        self.editItem(item, 0)

    def delete_selected_repos(self):
        for item in self.selectedItems():
            if item != self._add_repo_item:
                self.invisibleRootItem().removeChild(item)

    ####################
    # User interaction #
    ####################

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            self.delete_selected_repos()
            event.accept()
        elif event.key() == Qt.Key_Insert:
            self.add_repo(self.selection_index())
            event.accept()
        else:
            super().keyPressEvent(event)

    def _item_activated(self, item: QTreeWidgetItem, column: int):
        # If the add-repo item was activated, add a new repository before that
        # item.
        if item == self._add_repo_item and column == 0:
            self.add_repo(self.indexOfTopLevelItem(item))

    #################
    # Drag and drop #
    #################

    def _drop_index(self, event: QDragMoveEvent) -> int:
        index = self.indexAt(event.pos())

        if self.dropIndicatorPosition() == self.OnViewport:
            return self.topLevelItemCount()
        elif not index.isValid():
            return self.topLevelItemCount()
        elif self.dropIndicatorPosition() == self.BelowItem:
            return index.row() + 1
        else:
            return index.row()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        # Update dropIndicatorPosition
        self.setDropIndicatorShown(True)
        super().dragMoveEvent(event)

        # Prevent dropping below the last item
        if self._drop_index(event) >= self.topLevelItemCount():
            # No dropping here
            self.setDropIndicatorShown(False)
            event.setDropAction(Qt.IgnoreAction)
            event.accept()