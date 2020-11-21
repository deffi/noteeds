from typing import Optional


class CancelException (Exception):
    pass


class ProgressMonitor:
    def __init__(self, increment = None):
        self._increment = increment

        self._running: bool = False
        self._value: Optional[int] = None
        self._total: Optional[int] = None

        self._next_value = None

    def start(self, total: int) -> None:
        self._running = True
        self._value = 0
        self._total = total
        self._next_value = self._increment

    def value(self, value: int) -> None:
        self._value = value
        if self._increment:
            if value >= self._next_value or value == self._total:
                self._progress(self._value, self._total)
                self._next_value += self._increment
        else:
            self._progress(self._value, self._total)

    def next(self, count: int = 1) -> None:
        self.value(self._value + 1)

    def wrap(self, value, /):
        self.next()
        return value

    def _start(self, total: int):
        pass

    def _progress(self, value: int, total: int):
        pass

    def _done(self):
        pass


class TextProgressMonitor(ProgressMonitor):
    def _progress(self, value, total) -> bool:
        print(f"{value}/{total}")
