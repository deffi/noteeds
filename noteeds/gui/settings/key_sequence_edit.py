from PySide2.QtCore import Qt
from PySide2.QtWidgets import QKeySequenceEdit
from PySide2.QtGui import QKeyEvent, QKeySequence


class KeySequenceEdit(QKeySequenceEdit):
    def keyPressEvent(self, event: QKeyEvent):
        print(f"KeySequenceEdit received a {event.key()} event")
        if event.key() in [Qt.Key_Escape, Qt.Key_Enter]:
            # Ignore Escape and Enter to let the dialog receive them. We don't
            # need to ignore tab; presumable, this is event-filtered by the
            # dialog.
            event.ignore()
        else:
            super().keyPressEvent(event)

            # Stop editing
            self.setKeySequence(self.keySequence())
