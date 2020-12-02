from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QTreeWidget


class TreeWidget(QTreeWidget):
    delete_key = Signal()
    insert_key = Signal()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            self.delete_key.emit()
            event.accept()
        elif event.key() == Qt.Key_Insert:
            self.insert_key.emit()
            event.accept()
        else:
            super().keyPressEvent(event)
