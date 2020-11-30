import logging
from typing import Optional
from pathlib import Path

from PySide2.QtCore import Signal, Property, Qt
from PySide2.QtWidgets import QWidget, QFileDialog, QStyleOptionButton, QStyle

from noteeds.gui.settings.ui_path_browse_widget import Ui_PathBrowseWidget


logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
class PathBrowseWidget(QWidget):
    path_selected = Signal()

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.ui = Ui_PathBrowseWidget()
        self.ui.setupUi(self)

        # Set the button to the minimum size for the
        font_metrics = self.fontMetrics()
        size = font_metrics.size(Qt.TextShowMnemonic, self.ui.browseButton.text())
        option = QStyleOptionButton()
        # If we do this, we get a larger minimum size. Why? TODO
        # self.ui.browseButton.initStyleOption(option)
        min_size = self.style().sizeFromContents(QStyle.CT_PushButton, option, size, self)
        self.ui.browseButton.setFixedWidth(min_size.width())

        self.ui.browseButton.clicked.connect(self.browse)

    def browse(self):
        path = QFileDialog.getExistingDirectory(parent=self, caption="Select repository root", dir=self.get_path())

        if path:
            path = str(Path(path))
            self.set_path(path)
            self.path_selected.emit()

    def set_path(self, path: str):
        self.ui.pathInput.setText(path)

    def get_path(self) -> str:
        return self.ui.pathInput.text()
