import logging
from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget

from noteeds.engine.config import Config, GuiConfig
from noteeds.gui.settings.ui_settings_dialog import Ui_SettingsDialog

logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
class SettingsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.ui.clearHotkeyButton.clicked.connect(self.ui.hotkeyInput.clear)

    #################
    # Configuration #
    #################

    def set_config(self, config: Config):
        self.ui.systrayCheckbox.setChecked(config.gui.close_to_systray)
        self.ui.hotkeyCheckbox.setChecked(config.gui.use_global_hotkey)
        self.ui.hotkeyInput.setKeySequence(config.gui.global_hotkey)
        self.ui.externalEditorInput.setText(config.gui.external_editor)

        self.ui.reposTree.set_repos(config.repositories)
        self.ui.reposTree.resize_columns_to_contents()

    def get_config(self):
        return Config(
            gui=GuiConfig(
                close_to_systray=self.ui.systrayCheckbox.isChecked(),
                use_global_hotkey=self.ui.hotkeyCheckbox.isChecked(),
                global_hotkey=self.ui.hotkeyInput.keySequence(),
                external_editor=self.ui.externalEditorInput.text(),
            ),
            repositories=self.ui.reposTree.get_repos(),
        )
