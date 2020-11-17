import logging
from pathlib import Path
from typing import Optional

from PySide2.QtCore import QSettings, Signal, Slot, QModelIndex
from PySide2.QtGui import QCloseEvent, QDragEnterEvent, QDropEvent
from PySide2.QtWidgets import QMainWindow, QMessageBox

from noteeds.engine import Repository, Query, Engine, SearchResult
from noteeds.gui import SearchResultModel, Highlighter
from noteeds.gui.ui_main_window import Ui_MainWindow
from noteeds.gui.log_table import LogTable

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    value_changed = Signal(int)

    ##########
    # Window #
    ##########

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.splitter.setStretchFactor(0, 0)
        self.ui.splitter.setStretchFactor(1, 1)

        # Log model
        self._log_model = LogTable(self)

        # Set up UI elements
        self.ui.exitAction.triggered.connect(self.close)
        self.ui.logTable.setModel(self._log_model)
        self.ui.viewLogAction.toggled.connect(self.ui.dock.setVisible)

        self.ui.viewMenu.addAction(self.ui.dock.toggleViewAction())

        self._repository: Optional[Repository] = None
        self._engine: Optional[Engine] = None
        self._result: Optional[SearchResult] = None

        self._search_result_model = SearchResultModel(self)

        # Setup the results tree view
        self.ui.resultsTree.setModel(self._search_result_model)

        # Setup the document
        self._highlighter = Highlighter(self.ui.textView.document())

        self.ui.resultsTree.selectionModel().currentChanged.connect(self.file_selection_changed)

    def closeEvent(self, event: QCloseEvent):
        if self.confirm_close():
            event.accept()
            super().closeEvent(event)
        else:
            event.ignore()

    ##############
    # Properties #
    ##############

    def set_root(self, root: Path):
        self.ui.rootLabel.setText(f"Root: {root}")
        self._repository = Repository(root)
        self._engine = Engine([self._repository])
        self._engine.load_all(None)

    def set_text(self, text: str):
        self.ui.textInput.setText(text)

    ############
    # Settings #
    ############

    def store_settings(self):
        settings = QSettings()
        settings.beginGroup("main_window")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())
        settings.setValue("splitter_state", self.ui.splitter.saveState())
        settings.setValue("log_table_header_state", self.ui.logTable.header().saveState())
        settings.endGroup()

    def load_settings(self):
        # TODO errors here should be caught (individually) and redirected to the logger
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

    # Needs acceptDrops
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        uris = event.mimeData().urls()
        files = [uri.toLocalFile() for uri in uris]
        logger.info(str(files))

    def confirm_close(self) -> bool:
        result = QMessageBox.question(self, self.windowTitle(), "Really exit?")
        return result == QMessageBox.Yes

    @Slot(int)
    def on_valueInput_valueChanged(self, value):
        logger.info(f"Value change: {value}")
        self.value_changed.emit(value)

    @Slot(logging.LogRecord)
    def log_message(self, log_record: logging.LogRecord):
        scroll_bar = self.ui.logTable.verticalScrollBar()
        at_end = (scroll_bar.value() == scroll_bar.maximum())

        self._log_model.append(log_record)

        if at_end:
            self.ui.logTable.scrollToBottom()

    @Slot(str)
    def on_textInput_textChanged(self, text):
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
    def file_selection_changed(self, index, previous_index):
        # Get the file entry from the model; if the selected index does not
        # represent a file, this will be None.
        file_entry = self._search_result_model.file_entry(index)

        if file_entry is None:
            self.ui.textView.clear()
        else:
            self.ui.textView.setPlainText(file_entry.contents())

        logger.info(file_entry.absolute_path.name)
