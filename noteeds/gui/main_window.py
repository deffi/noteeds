import logging
from pathlib import Path
from typing import Optional

from PySide2.QtCore import QSettings, Slot, QModelIndex, Qt
from PySide2.QtGui import QCloseEvent, QColor, QKeySequence
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication

from noteeds.engine.config import Config
from noteeds.engine import Repository, Query, Engine
from noteeds.engine.repository import Config as RepositoryConfig
from noteeds.gui import SearchResultModel, Highlighter, DialogProgressMonitor, SystrayIcon, GlobalHotkey
from noteeds.gui.log_table import LogTable
from noteeds.gui.ui_main_window import Ui_MainWindow
from noteeds.util.progress import Tracker
from noteeds.gui.settings import SettingsDialog

logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
class MainWindow(QMainWindow):
    ##########
    # Window #
    ##########

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._settings: Optional[Config] = None

        # *** Window
        self._systray_icon = SystrayIcon(self)
        self._systray_icon.show_window.connect(self.show_window)
        self._systray_icon.exit.connect(QApplication.instance().exit)

        # *** Hotkey
        self._hotkey = GlobalHotkey(self)
        self._hotkey.pressed.connect(self.toggle_window)

        # *** Data
        self._engine: Optional[Engine] = None

        # *** Models
        self._search_result_model = SearchResultModel(self)
        self._log_model = LogTable(self)
        self._highlighter = Highlighter(self.ui.textView.document())

        # *** Menu
        self.ui.exitAction.triggered.connect(QApplication.instance().exit)
        self.ui.viewMenu.addAction(self.ui.dock.toggleViewAction())
        self.ui.hideAction.triggered.connect(self.hide_window)

        # *** Widgets ***
        self.ui.splitter.setStretchFactor(0, 0)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.resultsTree.setModel(self._search_result_model)
        self.ui.resultsTree.selectionModel().currentChanged.connect(self.file_selection_changed)
        self.ui.logTable.setModel(self._log_model)
        self.ui.dock.setVisible(False)

    def startup(self):
        QApplication.instance().processEvents()

        self.apply_settings()

    ##############
    # Properties #
    ##############

    def set_text(self, text: str) -> None:
        self.ui.textInput.setText(text)

    ############
    # Settings #
    ############

    def apply_settings(self) -> None:
        # self._hotkey.register(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_W))
        # self._hotkey.register(QKeySequence(Qt.ALT + Qt.META + Qt.Key_Q))
        # self._hotkey.register(QKeySequence(Qt.ALT + Qt.META + Qt.Key_W))
        # self._hotkey.register(QKeySequence(Qt.META + Qt.Key_F2))

        if self._settings.gui.use_global_hotkey:
            self._hotkey.register(self._settings.gui.global_hotkey)
        else:
            self._hotkey.register(None)

        repos = [Repository(config) for config in self._settings.repositories or [] if config.root and config.enabled]
        self._engine = Engine(repos)
        tracker = Tracker(DialogProgressMonitor("Loading", self), delta_t=1/25)
        self._engine.load_all(tracker)
        self.search(self.ui.textInput.text())

    def set_settings(self, settings: Config) -> None:
        self._settings = settings

    def store_window_settings(self) -> None:
        settings = QSettings()
        settings.beginGroup("main_window")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())
        settings.setValue("splitter_state", self.ui.splitter.saveState())
        settings.setValue("log_table_header_state", self.ui.logTable.header().saveState())
        settings.endGroup()

    def load_window_settings(self) -> None:
        # TODO errors here should be caught (individually) and logged
        settings = QSettings()
        settings.beginGroup("main_window")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("window_state"))
        self.ui.splitter.restoreState(settings.value("splitter_state"))
        self.ui.logTable.header().restoreState(settings.value("log_table_header_state"))
        settings.endGroup()

    ##########
    # Window #
    ##########

    def hide_window(self):
        self._systray_icon.show()
        self.hide()

    def show_window(self):
        self._systray_icon.hide()
        self.show()
        self.ui.textInput.selectAll()
        self.ui.textInput.setFocus()

    def toggle_window(self):
        if self.isVisible():
            self.hide_window()
        else:
            self.show_window()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._settings.gui.close_to_systray:
            # Ignore the close event, hide the window (and create the systray
            # icon) instead
            event.ignore()
            self.hide_window()
        else:
            # Go ahead
            super().closeEvent(event)

    ######
    # UI #
    ######

    def log_message(self, log_record: logging.LogRecord) -> None:
        scroll_bar = self.ui.logTable.verticalScrollBar()
        at_end = (scroll_bar.value() == scroll_bar.maximum())

        self._log_model.append(log_record)

        if at_end:
            self.ui.logTable.scrollToBottom()

        if log_record.levelno >= logging.ERROR:
            self.ui.dock.setVisible(True)

    def search(self, text: str) -> None:
        if self._engine is None:
            return

        query = Query(text, False, None, 0)
        result = self._engine.find(query)
        self._search_result_model.set_result(result)
        self.ui.resultsTree.expandAll()

        if self._highlighter is not None:
            self._highlighter.set_search_term(text)

    @Slot(str)
    def on_textInput_textChanged(self, text: str) -> None:
        self.search(text)

    # noinspection PyUnusedLocal
    def file_selection_changed(self, index: QModelIndex, previous_index: QModelIndex) -> None:
        # Get the file entry from the model; if the selected index does not
        # represent a file, this will be None.
        file_entry = self._search_result_model.file_entry(index)

        if file_entry is None:
            self.ui.textView.clear()
        else:
            self.ui.textView.setPlainText(file_entry.contents())

    @Slot()
    def on_settingsAction_triggered(self):
        dialog = SettingsDialog(self)
        dialog.set_config(self._settings)
        result = dialog.exec_()
        if result == SettingsDialog.Accepted:
            self._settings = dialog.get_config()
            self._settings.store(QSettings())
            self.apply_settings()
