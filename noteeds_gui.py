import argparse
import ctypes
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from PySide2.QtCore import QTimer, Qt, QSettings
from PySide2.QtGui import QIcon, QColor, QKeySequence
from PySide2.QtWidgets import QApplication

from noteeds.engine.config import Config
from noteeds.engine import FileEntry
from noteeds.gui import MainWindow, LogEmitter


@dataclass()
class Args(argparse.Namespace):
    config: str = None
    load_delay: float = None
    load_delay_probability: float = 0.05
    text: str = None


def noteeds_gui(args: Args):
    # Configure logging
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    log_emitter = LogEmitter(None)
    root_logger.addHandler(log_emitter.handler)

    # Install an excepthook to log unhandled exceptions
    original_excepthook = sys.excepthook

    def excepthook(e_type, e_value, e_traceback):
        # Call the original hook before logging the error, because logging may
        # fail.
        original_excepthook (e_type, e_value, e_traceback)
        root_logger.error("Unhandled exception", exc_info=(e_type, e_value, e_traceback))
    sys.excepthook = excepthook

    # On Windows, set the AppUserModelID so the taskbar shows the application's
    # icon rather than the pythonw.exe icon.
    if os.name == "nt":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("noteeds.noteeds")

    text = args.text
    FileEntry.load_delay = args.load_delay
    FileEntry.load_delay_probability = args.load_delay_probability

    app = QApplication(sys.argv)
    app.setOrganizationName("noteeds")
    app.setOrganizationDomain("noteeds.invalid")
    app.setApplicationName(args.config)

    # icon_path = Path(__file__).parent / "images" / "icon48.png"
    icon_path = Path(__file__).parent / "images" / "icon.ico"
    icon = QIcon(str(icon_path))
    app.setWindowIcon(icon)

    config = Config.load(QSettings())
    window = MainWindow(None)
    log_emitter.log.connect(window.log_message)
    window.set_settings(config)
    window.load_window_settings()
    window.set_text(text)
    window.show()
    QTimer.singleShot(0, window.startup)
    result = app.exec_()
    window.store_window_settings()
    sys.exit(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="noteeds")
    parser.add_argument("--load-delay", type=float)
    parser.add_argument("--load-delay-probability", type=float)
    parser.add_argument("text", default="", nargs="?")
    args = parser.parse_args(namespace=Args())
    noteeds_gui(args)


if __name__ == "__main__":
    main()
