import logging
import time
import traceback
from typing import Any, List, Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject


class LogTable(QAbstractTableModel):
    """Collects log records and provides a table model for them.

    Note that this class is a container and an item model at the same time
    (that's why it is called LogTable rather than LogTableModel).
    """

    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)
        self._records: List[logging.LogRecord] = []

    def append(self, record: logging.LogRecord) -> None:
        row = len(self._records)
        self.beginInsertRows(QModelIndex(), row, row)
        self._records.append(record)
        self.endInsertRows()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._records)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 4

    @staticmethod
    def _format_log_record_time(record: logging.LogRecord) -> str:
        # "%Y-%m-%d %H:%M:%S"
        return time.strftime("%H:%M:%S", time.localtime(record.created))

    @staticmethod
    def _format_log_record(record: logging.LogRecord) -> str:
        text = record.msg % record.args

        if record.exc_info:
            exception_type, value, tb = record.exc_info
            text = f"{text}:\n{''.join(traceback.format_exception(exception_type, value, tb)).strip()}"

        return text

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        record = self._records[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if   column == 0: return self._format_log_record_time(record)
            elif column == 1: return record.levelname
            elif column == 2: return record.name
            elif column == 3: return self._format_log_record(record)

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignTop

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if   section == 0: return "Time"
                elif section == 1: return "Level"
                elif section == 2: return "Source"
                elif section == 3: return "Message"
