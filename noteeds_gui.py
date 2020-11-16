import sys
from pathlib import Path

import logging
from PySide2.QtWidgets import QApplication

from noteeds.gui import MainWindow, LogEmitter


# TODO remove text; GUI configuration for root
if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} root text")
    exit(1)

root = Path(sys.argv[1])
text = sys.argv[2]

if __name__ == "__main__":
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    log_emitter = LogEmitter(None)
    root_logger.addHandler(log_emitter.handler)

    app = QApplication(sys.argv)
    app.setOrganizationName("noteeds")
    app.setOrganizationDomain("noteeds.invalid")
    app.setApplicationName("noteeds")

    window = MainWindow(None)
    log_emitter.log.connect(window.log_message)
    window.load_settings()
    window.set_root(root)
    window.set_text(text)
    window.show()
    result = app.exec_()
    window.store_settings()
    sys.exit(result)
