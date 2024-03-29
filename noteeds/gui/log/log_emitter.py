import logging
from typing import Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication


class _Handler(logging.Handler):
    def __init__(self, signal: Signal):
        super().__init__()
        self._signal = signal

    def emit(self, log_record: logging.LogRecord) -> None:
        self._signal.emit(log_record)
        QApplication.processEvents()


class LogEmitter(QObject):
    """The handler is implemented as a separate class instead of using multiple
    inheritance because both logging.Handler and QObject define an emit
    method."""
    log = Signal(logging.LogRecord)

    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)
        self.handler = _Handler(self.log)
