from PySide2.QtGui import QSyntaxHighlighter, QTextCharFormat
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        
        self._search_term = None
        
    def set_search_term(self, search_term):
        self._search_term = search_term
        
    def highlightBlock(self, text):
        if self._search_term is None:
            return        
        
        text_format = QTextCharFormat()
        text_format.setFontWeight(QFont.Bold)
        text_format.setForeground(Qt.darkMagenta)
        text_format.setBackground(Qt.yellow)

        text = text.lower()

        length = len(self._search_term)

        index = text.find(self._search_term.lower())
        while index >= 0:
            self.setFormat(index, length, text_format)
            index = text.find(self._search_term, index + length)
