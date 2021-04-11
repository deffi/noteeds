import logging
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QTextCursor, QTextCharFormat
from PySide2.QtWidgets import QPlainTextEdit, QWidget

logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
class TextView(QPlainTextEdit):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

        self.setTabChangesFocus(True)
        self.setReadOnly(False)
        self.setCenterOnScroll(True)

        self.verticalScrollBar().valueChanged.connect(self.highlight_visible)

        self._search_term = None

        self._text_format = QTextCharFormat()
        self._text_format.setFontWeight(QFont.Bold)
        self._text_format.setForeground(Qt.darkMagenta)
        self._text_format.setBackground(Qt.yellow)

    def clear(self):
        super().clear()

    def set_text(self, text: Optional[str]):
        super().setPlainText(text)
        self.scroll_to_first_location()
        self.highlight_visible()

    def set_search_term(self, search_term: Optional[str]):
        self._search_term = search_term
        self.unhighlight()
        self.highlight_visible()

    def unhighlight(self):
        cursor = QTextCursor (self.document())
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.setCharFormat(QTextCharFormat())

    def scroll_to_first_location(self):
        cursor = self.document().find(self._search_term)
        if not cursor.isNull():
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
            self.setTextCursor(QTextCursor())

    def start_cursor(self):
        return self.cursorForPosition(self.viewport().rect().topLeft())

    def end_cursor(self):
        return self.cursorForPosition(self.viewport().rect().bottomRight())

    def highlight_visible(self):
        # Might not work with RTL text
        document = self.document()
        end = self.end_cursor()

        # Highlighting is a little slow for large documents, so we limit
        # highlighting to the visible range.
        # We should be searching in the visible range (start to end), but it
        # seems like we can't do that. So we search as long as we find anything,
        # and stop when it is beyond the visible range. This means that we might
        # be searching more text than we need to.
        cursor = self.start_cursor()
        while not (cursor := document.find(self._search_term, cursor)).isNull():
            if cursor.position() > end.position():
                break

            cursor.setCharFormat(self._text_format)
