from PySide2.QtCore import Qt
from PySide2.QtWidgets import QKeySequenceEdit
from PySide2.QtGui import QKeyEvent, QKeySequence


class KeySequenceEdit(QKeySequenceEdit):
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [Qt.Key_Escape, Qt.Key_Enter, Qt.Key_Tab]:
            # Ignore Escape, Enter, and Tab
            event.ignore()
        else:
            super().keyPressEvent(event)

            # Stop editing
            self.setKeySequence(self.keySequence())
