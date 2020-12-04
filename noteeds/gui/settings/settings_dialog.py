import logging
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QDialog, QWidget, QTreeWidgetItem, QAbstractItemView

from noteeds.engine.config import Config, GuiConfig
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

    def set_config(self, config: Config):
        self.ui.systrayCheckbox.setChecked(config.gui.use_systray)
        self.ui.hotkeyCheckbox.setChecked(config.gui.use_global_hotkey)
        # self.ui.hotkeyInput.setText("+".join(config.gui.global_hotkey))

        self.ui.reposTree.set_repos(config.repositories)
        self.ui.reposTree.resize_columns_to_contents()

    def get_config(self):
        return Config(
            gui=GuiConfig(
                use_systray=self.ui.systrayCheckbox.isChecked(),
                use_global_hotkey=self.ui.hotkeyCheckbox.isChecked(),
                global_hotkey=tuple(),
            ),
            repositories=self.ui.reposTree.get_repos(),
        )
