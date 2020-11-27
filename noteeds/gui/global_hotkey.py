from typing import Optional

from PySide2.QtCore import QObject, Signal

from system_hotkey import SystemHotkey


class GlobalHotkey(QObject):
    pressed = Signal()

    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)

        hk = SystemHotkey()
        hk.register(('shift', 'alt', 'w'), callback=self._callback)

    def _callback(self, *args, **kwargs):
        self.pressed.emit()
