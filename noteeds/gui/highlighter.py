from typing import Union, Optional

from PySide2.QtCore import Qt, QObject
from PySide2.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QTextDocument


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent: Union[QObject, QTextDocument]):
        super().__init__(parent)
        
        self._search_term: Optional[str] = None
        
    def set_search_term(self, search_term: str) -> None:
        self._search_term = search_term
        
    def highlightBlock(self, text: str) -> None:
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
