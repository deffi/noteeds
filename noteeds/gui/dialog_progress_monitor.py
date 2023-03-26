from typing import Optional

from PySide6.QtWidgets import QProgressDialog, QWidget, QApplication

from noteeds.util.progress import Monitor, CancelException


class DialogProgressMonitor(Monitor):
    def __init__(self, label_text: str, parent: QWidget):
        self._label_text = label_text
        self._parent = parent
        self._dialog: Optional[QProgressDialog] = None

    def start(self, total: int) -> None:
        self._dialog = QProgressDialog(self._label_text, "Cancel", 0, total, self._parent)
        self._dialog.show()

    def progress(self, value: int) -> None:
        self._dialog.setValue(value)
        QApplication.instance().processEvents()
        if self._dialog.wasCanceled():
            raise CancelException

    def done(self) -> None:
        self._dialog.close()
