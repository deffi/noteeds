import logging
from typing import Optional

from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QKeySequence

from system_hotkey import SystemHotkey


logger = logging.getLogger(__name__)


class GlobalHotkey(QObject):
    pressed = Signal()

    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)

        self._hk = SystemHotkey()

    def is_registered(self, key):
        key = set(key)
        return any(set(k) == key for k in self._hk.keybinds)

    def register(self, key_sequence: Optional[QKeySequence]):
        key = self.convert_key_sequence(key_sequence)

        if key and self.is_registered(key):
            logger.debug("Already registered: %s", key)
            return

        self.unregister()
        if key_sequence and not key_sequence.isEmpty():
            logger.info("Registering hotkey: %s", key)
            # If this fails, we get a system_hotkey.SystemRegisterError
            # exception, but in a different thread - so we can neither catch it
            # here nor is it logged.
            self._hk.register(key, callback=self._callback)

    @staticmethod
    def convert_key_sequence(key_sequence: QKeySequence):
        if not key_sequence or key_sequence.isEmpty():
            return None

        # Restrict to the first key
        key_sequence = QKeySequence(key_sequence[0])

        # Convert to format for SystemHotkey - simple approach, may not be
        # sufficient.
        key = key_sequence.toString(QKeySequence.PortableText).split("+")
        key = [part.lower() for part in key]

        if "meta" in key:
            key.remove("meta")
            key = ["super"] + key

        return key

    def unregister(self):
        for key in self._hk.keybinds:
            logger.info("Unregistering hotkey: %s", (key, ))
            self._hk.unregister(key)

    def _callback(self, *_, **__):
        self.pressed.emit()
