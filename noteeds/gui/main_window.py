import logging
from typing import Optional
import subprocess
from shutil import which

from PySide2.QtCore import QSettings, Slot, QModelIndex, Qt, QObject, QEvent
from PySide2.QtGui import QCloseEvent, QTextDocument, QFont, QKeyEvent, QTextCursor, QTextCharFormat
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox

from noteeds.util import MultiFormatter
from noteeds.engine.config import Config
from noteeds.engine import Repository, Query, Engine
from noteeds.gui import SearchResultModel, DialogProgressMonitor, SystrayIcon, GlobalHotkey
from noteeds.gui.log import LogTable
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

        # *** Menu
        self.ui.exitAction.triggered.connect(QApplication.instance().exit)
        self.ui.viewMenu.addAction(self.ui.dock.toggleViewAction())
        self.ui.hideAction.triggered.connect(self.hide_window)

        # *** Widgets ***
        self.ui.textInput.installEventFilter(self)
        self.ui.splitter.setStretchFactor(0, 0)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.resultsTree.setModel(self._search_result_model)
        self.ui.resultsTree.selectionModel().currentChanged.connect(self.file_selection_changed)

        self.ui.logTable.setModel(self._log_model)
        self.ui.dock.setVisible(False)

    def startup(self):
        QApplication.instance().processEvents()

        self.apply_settings()
        self.ui.textView.document().setDefaultFont(self.ui.resultsTree.font())

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

        self.highlight()

    @Slot(str)
    def on_textInput_textChanged(self, text: str) -> None:
        self.search(text)

    def highlight(self):
        text_format = QTextCharFormat()
        text_format.setFontWeight(QFont.Bold)
        text_format.setForeground(Qt.darkMagenta)
        text_format.setBackground(Qt.yellow)

        term = self.ui.textInput.text()
        view = self.ui.textView
        doc: QTextDocument = view.document()

        cursor = QTextCursor (doc)
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.setCharFormat(QTextCharFormat())

        cursor = QTextCursor (doc)
        positions = []
        while not (cursor := doc.find(term, cursor)).isNull():
            cursor.setCharFormat(text_format)
            positions.append(cursor)
        if positions:
            view.setTextCursor(positions[0])
            view.ensureCursorVisible()
            view.setTextCursor(QTextCursor())

    # noinspection PyUnusedLocal
    def file_selection_changed(self, index: QModelIndex, previous_index: QModelIndex) -> None:
        # Get the file entry from the model; if the selected index does not
        # represent a file, this will be None.
        file_entry = self._search_result_model.file_entry(index)

        if file_entry is None:
            self.ui.textView.clear()
            self.ui.editAction.setEnabled(False)
        else:
            self.ui.textView.setPlainText(file_entry.contents())
            self.highlight()
            self.ui.editAction.setEnabled(True)

    @Slot()
    def on_settingsAction_triggered(self):
        dialog = SettingsDialog(self)
        dialog.set_config(self._settings)
        result = dialog.exec_()
        if result == SettingsDialog.Accepted:
            self._settings = dialog.get_config()
            self._settings.store(QSettings())
            self.apply_settings()

    @Slot()
    def on_testAction_triggered(self):
        print(f"{QFont()                                   =}")
        print(f"{self.font()                               =}")
        print(f"{self.ui.fileMenu.font()                   =}")
        print(f"{self.ui.label.font()                      =}")
        print(f"{self.ui.textInput.font()                  =}")
        print(f"{self.ui.resultsTree.font()                =}")
        print(f"{self.ui.textView.font()                   =}")
        print(f"{self.ui.textView.document().defaultFont() =}")

        # f: QFont = self.ui.resultsTree.font()
        # f.setPointSize(14)
        # print(f)
        # self.ui.textView.setFont(f)
        # # self.ui.textView.document().setDefaultFont(f)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.ui.textInput and event.type() == QEvent.KeyPress:
            event: QKeyEvent
            if event.modifiers() == Qt.ControlModifier:
                if event.key() in [Qt.Key_Down, Qt.Key_Up, Qt.Key_PageDown, Qt.Key_PageUp, Qt.Key_Home, Qt.Key_End]:
                    QApplication.sendEvent(self.ui.resultsTree, event)
                    return True

        return super().eventFilter(watched, event)

    @Slot()
    def on_editAction_triggered(self):
        editor = self._settings.gui.external_editor.strip()
        if editor:
            current_index = self.ui.resultsTree.currentIndex()
            if current_index.isValid():
                file_entry = self._search_result_model.file_entry(current_index)
                if file_entry:
                    formatter = MultiFormatter(
                        file = file_entry.absolute_path,
                        search_term = self.ui.textInput.text()
                    )

                    command = editor.split()

                    # TODO handle KeyError
                    command = list(map(formatter.format, command))

                    # If the file was not specified, append it
                    if "file" in formatter.unused:
                        command.append(formatter.format_field("file"))

                    command_0 = which(command[0])
                    if command_0:
                        command[0] = command_0
                        logger.info("Run external editor: %s", command)
                        subprocess.Popen(command)
                    else:
                        QMessageBox.critical(self, self.windowTitle(), f"Editor not found: {command[0]}")
                else:
                    QMessageBox.critical(self, self.windowTitle(), "No file selected")
        else:
            QMessageBox.critical(self, self.windowTitle(), "No external editor configured")
