import logging
from pathlib import Path
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QMessageBox, QWidget, QTreeWidgetItem, QAbstractItemView

from noteeds.engine.config import Config
from noteeds.engine.repository import Config as RepositoryConfig
from noteeds.gui.settings.ui_settings_dialog import Ui_SettingsDialog
from noteeds.gui.settings import ColorDelegate

logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
class SettingsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.ui.reposTree.setItemDelegateForColumn(2, ColorDelegate(self))
        self.ui.reposTree.setEditTriggers(QAbstractItemView.AllEditTriggers & ~QAbstractItemView.CurrentChanged)

    def set_config(self, config: Config):
        self.ui.systrayCheckbox.setChecked(config.gui.use_systray)
        self.ui.hotkeyCheckbox.setChecked(config.gui.use_global_hotkey)
        # self.ui.hotkeyInput.setText("+".join(config.gui.global_hotkey))

        self.ui.reposTree.clear()
        for repo in config.repositories:
            item = QTreeWidgetItem()
            item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsEditable)
            item.setCheckState(0, (Qt.Checked if repo.enabled else Qt.Unchecked))
            item.setText(1, repo.name or "")
            item.setData(2, Qt.DisplayRole, "")
            item.setData(2, Qt.DecorationRole, repo.color)
            item.setText(3, str(repo.root))

            self.ui.reposTree.addTopLevelItem(item)

        for column in range(self.ui.reposTree.columnCount()):
            self.ui.reposTree.resizeColumnToContents(column)
