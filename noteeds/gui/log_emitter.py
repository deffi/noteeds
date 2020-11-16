import logging

from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QApplication


class _Handler(logging.Handler):
    def __init__(self, signal: Signal):
        super().__init__()
        self._signal = signal

    def emit(self, log_record: logging.LogRecord):
        self._signal.emit(log_record)
        QApplication.processEvents()


class LogEmitter(QObject):
    """The handler is implemented as a separate class instead of using multiple
    inheritance because both logging.Handler and QObject define an emit
    method."""
    log = Signal(logging.LogRecord)

    def __init__(self, parent):
        super().__init__(parent)
        self.handler = _Handler(self.log)
