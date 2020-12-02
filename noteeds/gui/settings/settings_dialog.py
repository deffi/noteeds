import logging
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QWidget, QTreeWidgetItem, QAbstractItemView

from noteeds.engine.config import Config
from noteeds.gui.settings import ColorDelegate, PathBrowseDelegate
from noteeds.gui.settings.ui_settings_dialog import Ui_SettingsDialog

logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
class SettingsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.ui.hotkeyInput.editingFinished.connect(self.ui.hotkeyCheckbox.setFocus)
        self.ui.clearHotkeyButton.clicked.connect(self.ui.hotkeyInput.clear)

        self.ui.reposTree.setItemDelegateForColumn(1, ColorDelegate(self))
        self.ui.reposTree.setItemDelegateForColumn(2, PathBrowseDelegate(self))
        self.ui.reposTree.setEditTriggers(QAbstractItemView.AllEditTriggers & ~QAbstractItemView.CurrentChanged)
        self.ui.reposTree.insert_key.connect(self.repos_insert)
        self.ui.reposTree.delete_key.connect(self.repos_delete)
        self.ui.reposTree.itemActivated.connect(self.repos_item_activated)
        self.ui.reposTree.itemClicked.connect(self.repos_item_activated)

    def set_config(self, config: Config):
        self.ui.systrayCheckbox.setChecked(config.gui.use_systray)
        self.ui.hotkeyCheckbox.setChecked(config.gui.use_global_hotkey)
        # self.ui.hotkeyInput.setText("+".join(config.gui.global_hotkey))

        self.ui.reposTree.clear()
        for repo in config.repositories:
            item = QTreeWidgetItem()
            item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsEditable)
            item.setData(0, Qt.CheckStateRole, (Qt.Checked if repo.enabled else Qt.Unchecked))
            item.setText(0, repo.name or "")
            item.setData(1, Qt.DisplayRole, "")
            item.setData(1, Qt.DecorationRole, repo.color)
            item.setData(2, Qt.EditRole, str(repo.root))

            self.ui.reposTree.addTopLevelItem(item)

        # The "Add..." item
        item = QTreeWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled & ~Qt.ItemIsEditable & ~Qt.ItemIsUserCheckable & ~Qt.ItemIsDragEnabled)
        item.setData(0, Qt.DisplayRole, "Add...")
        self.ui.reposTree.addTopLevelItem(item)

        for column in range(self.ui.reposTree.columnCount()):
            self.ui.reposTree.resizeColumnToContents(column)

    #########
    # Repos #
    #########

    def insert_repo(self, position: int):
        item = QTreeWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsEditable)
        item.setData(0, Qt.CheckStateRole, Qt.Checked)
        item.setText(0, "")
        item.setData(1, Qt.DisplayRole, "")
        item.setData(1, Qt.DecorationRole, None)
        item.setData(2, Qt.EditRole, "")

        self.ui.reposTree.insertTopLevelItem(position, item)

        self.ui.reposTree.clearSelection()
        self.ui.reposTree.setCurrentItem(item)
        item.setSelected(True)
        self.ui.reposTree.editItem(item, 0)

    def repos_insert(self):
        selected_items = self.ui.reposTree.selectedItems()
        if selected_items:
            position = self.ui.reposTree.indexOfTopLevelItem(selected_items[0])
        else:
            position = 0

        self.insert_repo(position)

    def repos_delete(self):
        for item in self.ui.reposTree.selectedItems():
            index = self.ui.reposTree.indexOfTopLevelItem(item)
            if index != self.ui.reposTree.invisibleRootItem().childCount() - 1:
                self.ui.reposTree.invisibleRootItem().removeChild(item)

    def repos_item_activated(self, item: QTreeWidgetItem, column: int):
        index = self.ui.reposTree.indexOfTopLevelItem(item)
        if index == self.ui.reposTree.invisibleRootItem().childCount() - 1 and column == 0:
            self.insert_repo(index)
