import sys
from dataclasses import dataclass
from pathlib import Path
import argparse

import logging
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from noteeds.engine import FileEntry
from noteeds.gui import MainWindow, LogEmitter


@dataclass()
class Args(argparse.Namespace):
    repositories: list[Path] = None
    text: str = None
    load_delay: float = None
    load_delay_probability: float = 0.05


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

    root = args.repositories[0]
    text = args.text
    FileEntry.load_delay = args.load_delay
    FileEntry.load_delay_probability = args.load_delay_probability

    app = QApplication(sys.argv)
    app.setOrganizationName("noteeds")
    app.setOrganizationDomain("noteeds.invalid")
    app.setApplicationName("noteeds")

    window = MainWindow(None)
    log_emitter.log.connect(window.log_message)
    window.load_settings()
    window.set_repositories(args.repositories)
    window.set_text(text)
    window.show()
    QTimer.singleShot(0, window.startup)
    result = app.exec_()
    window.store_settings()
    sys.exit(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--load-delay", type=float)
    parser.add_argument("--load-delay-probability", type=float)
    parser.add_argument("--repository", "-r", action='append', dest="repositories", type=Path)
    parser.add_argument("text")
    args = parser.parse_args(namespace=Args())
    noteeds_gui(args)

if __name__ == "__main__":
    main()
