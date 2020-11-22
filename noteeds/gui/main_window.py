import logging
from pathlib import Path
from typing import Optional

from PySide2.QtCore import QSettings, Signal, Slot, QModelIndex
from PySide2.QtGui import QCloseEvent, QDragEnterEvent, QDropEvent
from PySide2.QtWidgets import QMainWindow, QMessageBox, QApplication, QWidget

from noteeds.engine import Repository, Query, Engine, SearchResult
from noteeds.gui import SearchResultModel, Highlighter, DialogProgressMonitor
from noteeds.gui.ui_main_window import Ui_MainWindow
from noteeds.gui.log_table import LogTable
from noteeds.util.progress import Tracker, CancelException

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    value_changed = Signal(int)

    ##########
    # Window #
    ##########

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # *** Data
        self._repository: Optional[Repository] = None
        self._engine: Optional[Engine] = None

        # *** Models
        self._search_result_model = SearchResultModel(self)
        self._log_model = LogTable(self)
        self._highlighter = Highlighter(self.ui.textView.document())

        # *** Menu
        self.ui.exitAction.triggered.connect(self.close)
        self.ui.viewMenu.addAction(self.ui.dock.toggleViewAction())

        # *** Widgets ***
        self.ui.splitter.setStretchFactor(0, 0)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.resultsTree.setModel(self._search_result_model)
        self.ui.resultsTree.selectionModel().currentChanged.connect(self.file_selection_changed)
        self.ui.logTable.setModel(self._log_model)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.confirm_close():
            event.accept()
            super().closeEvent(event)
        else:
            event.ignore()

    ##############
    # Properties #
    ##############

    def set_root(self, root: Path) -> None:
        self.ui.rootLabel.setText(f"Root: {root}")
        self._repository = Repository(root, hue=None)
        self._engine = Engine([self._repository])
        tracker = Tracker(DialogProgressMonitor("Loading", self), delta_t=1/25)
        self._engine.load_all(tracker)

    def set_text(self, text: str) -> None:
        self.ui.textInput.setText(text)

    ############
    # Settings #
    ############

    def store_settings(self) -> None:
        settings = QSettings()
        settings.beginGroup("main_window")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())
        settings.setValue("splitter_state", self.ui.splitter.saveState())
        settings.setValue("log_table_header_state", self.ui.logTable.header().saveState())
        settings.endGroup()

    def load_settings(self) -> None:
        # TODO errors here should be caught (individually) and logged
        settings = QSettings()
        settings.beginGroup("main_window")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("window_state"))
        self.ui.splitter.restoreState(settings.value("splitter_state"))
        self.ui.logTable.header().restoreState(settings.value("log_table_header_state"))
        settings.endGroup()

    ######
    # UI #
    ######

    def confirm_close(self) -> bool:
        result = QMessageBox.question(self, self.windowTitle(), "Really exit?")
        return result == QMessageBox.Yes

    @Slot(logging.LogRecord)
    def log_message(self, log_record: logging.LogRecord) -> None:
        scroll_bar = self.ui.logTable.verticalScrollBar()
        at_end = (scroll_bar.value() == scroll_bar.maximum())

        self._log_model.append(log_record)

        if at_end:
            self.ui.logTable.scrollToBottom()

    @Slot(str)
    def on_textInput_textChanged(self, text: str) -> None:
        if self._engine is None:
            return

        query = Query(text, False, None, 0)
        result = self._engine.find(query)
        self._result = result
        self._search_result_model.set_result(result)
        self.ui.resultsTree.expandAll()

        if self._highlighter is not None:
            self._highlighter.set_search_term(text)

    # noinspection PyUnusedLocal
    @Slot(QModelIndex, QModelIndex)
    def file_selection_changed(self, index: QModelIndex, previous_index: QModelIndex) -> None:
        # Get the file entry from the model; if the selected index does not
        # represent a file, this will be None.
        file_entry = self._search_result_model.file_entry(index)

        if file_entry is None:
            self.ui.textView.clear()
        else:
            self.ui.textView.setPlainText(file_entry.contents())
