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

        for column in range(self.ui.reposTree.columnCount()):
            self.ui.reposTree.resizeColumnToContents(column)

    #########
    # Repos #
    #########

    def repos_insert(self):
        item = QTreeWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsEditable)
        item.setData(0, Qt.CheckStateRole, Qt.Checked)
        item.setText(0, "")
        item.setData(1, Qt.DisplayRole, "")
        item.setData(1, Qt.DecorationRole, None)
        item.setData(2, Qt.EditRole, "")

        selected = (self.ui.reposTree.selectedItems() or [0])[0]
        if selected:
            selected = self.ui.reposTree.indexOfTopLevelItem(selected)

        self.ui.reposTree.insertTopLevelItem(selected, item)
        item.setSelected(True)
        self.ui.reposTree.editItem(item, 0)

    def repos_delete(self):
        for item in self.ui.reposTree.selectedItems():
            self.ui.reposTree.invisibleRootItem().removeChild(item)
