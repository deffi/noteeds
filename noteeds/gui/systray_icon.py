import logging

from PySide2.QtCore import Signal, QObject
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget

logger = logging.getLogger(__name__)


class SystrayIcon(QObject):
    show_window = Signal()
    exit = Signal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # Bold font
        bold = QFont()
        bold.setBold(True)

        # Systray icon
        icon: QIcon = QApplication.instance().windowIcon()
        self._systray_icon = QSystemTrayIcon(icon, self)
        self._systray_icon.setToolTip("Noteeds")

        # Show action
        self._show_action = QAction("&Show", self)
        self._show_action.setFont(bold)

        # Exit action
        self._exit_action = QAction("E&xit", self)

        # Menu
        self._menu = QMenu(parent)
        self._menu.addAction(self._show_action)
        self._menu.addAction(self._exit_action)
        self._systray_icon.setContextMenu(self._menu)

        # Connections
        self._systray_icon.activated.connect(self._activated)
        self._show_action.triggered.connect(self.show_window)
        self._exit_action.triggered.connect(self.exit)

    def _activated(self, reason: QSystemTrayIcon.ActivationReason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_window.emit()

    def show(self):
        self._systray_icon.show()

    def hide(self):
        self._systray_icon.hide()
