import logging
from typing import Optional

from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QTextDocument, QFont, QKeyEvent, QTextCursor, QTextCharFormat, QGuiApplication
from PySide2.QtWidgets import QPlainTextEdit, QWidget

logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
class TextView(QPlainTextEdit):
    progress_maximum = Signal(int)
    progress_value = Signal(int)

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

        self.setTabChangesFocus(True)
        self.setReadOnly(True)
        self.setCenterOnScroll(True)

        self._progress_steps = 1000
        self._search_term = None

        self._text_format = QTextCharFormat()
        self._text_format.setFontWeight(QFont.Bold)
        self._text_format.setForeground(Qt.darkMagenta)
        self._text_format.setBackground(Qt.yellow)

    def clear(self):
        super().clear()

    def set_text(self, text: Optional[str]):
        super().setPlainText(text)
        self.highlight()

    def set_search_term(self, search_term: Optional[str]):
        self._search_term = search_term
        self.unhighlight()
        self.highlight()

    def unhighlight(self):
        cursor = QTextCursor (self.document())
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.setCharFormat(QTextCharFormat())

    def highlight(self):
        document = self.document()
        document_length = document.characterCount()
        first_location: Optional[QTextCursor] = None

        self.progress_maximum.emit(self._progress_steps)
        self.progress_value.emit(0)

        cursor = QTextCursor (document)
        while not (cursor := document.find(self._search_term, cursor)).isNull():
            if not first_location:
                first_location = cursor

            cursor.setCharFormat(self._text_format)

            progress = cursor.selectionStart() / document_length
            self.progress_value.emit(int(progress * self._progress_steps))

            QGuiApplication.processEvents()

        if first_location:
            self.setTextCursor(first_location)
            self.ensureCursorVisible()
            self.setTextCursor(QTextCursor())
