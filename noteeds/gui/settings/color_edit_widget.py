import logging
from pathlib import Path
from typing import Optional

from PySide2.QtCore import Qt, Signal, Property, Slot
from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QWidget, QColorDialog
from PySide2.QtCore import QTimer

from noteeds.gui.settings.ui_color_edit_widget import Ui_ColorEditWidget


logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
class ColorEditWidget(QWidget):
    color_picked = Signal()

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.ui = Ui_ColorEditWidget()
        self.ui.setupUi(self)

        self.ui.colorButton.clicked.connect(self.pick_color)
        self.ui.clearButton.setFixedWidth(self.ui.clearButton.height())
        self.ui.clearButton.clicked.connect(self.clear_color)

        self._color: Optional[QColor] = None
        self._color_set: bool = False

    def pick_color(self):
        color = QColorDialog.getColor(initial=self._color, parent=self)
        if color.isValid():
            self._apply_color(color)
            self.color_picked.emit()

    def clear_color(self):
        self._apply_color(None)
        self.color_picked.emit()

    def _apply_color(self, color: Optional[QColor]):
        if color == self._color:
            return

        if color:
            palette: QPalette = self.ui.colorButton.palette()
            palette.setColor(QPalette.Button, QColor(color))
            self.ui.colorButton.setPalette(palette)
        else:
            self.ui.colorButton.setPalette(QPalette())

        self._color = color

    def set_color(self, color: Optional[QColor]):
        self._apply_color(color)
        if color is None and not self._color_set:
            QTimer.singleShot(0, self.pick_color)

        self._color_set = True

    def get_color(self) -> Optional[QColor]:
        return self._color

    color = Property(QColor, get_color, set_color, user=True)
