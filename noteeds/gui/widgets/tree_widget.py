from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QTreeWidget
from PySide2.QtGui import QDragMoveEvent


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

    def _drop_index(self, event: QDragMoveEvent) -> int:
        index = self.indexAt(event.pos())

        if self.dropIndicatorPosition() == self.OnViewport:
            return self.topLevelItemCount()
        elif not index.isValid():
            return self.topLevelItemCount()
        elif self.dropIndicatorPosition() == self.BelowItem:
            return index.row() + 1
        else:
            return index.row()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        # TODO that does not belong in a generic tree widget, refactor to ReposTreeWidget
        # Update dropIndicatorPosition
        self.setDropIndicatorShown(True)
        super().dragMoveEvent(event)

        # Prevent dropping below the last item
        if self._drop_index(event) >= self.topLevelItemCount():
            # No dropping here
            self.setDropIndicatorShown(False)
            event.setDropAction(Qt.IgnoreAction)
            event.accept()
