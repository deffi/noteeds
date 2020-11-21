from typing import Optional
from time import monotonic


class CancelException (Exception):
    pass


class ProgressMonitor:
    def __init__(self, increment: Optional[int] = None, dt: Optional[float] = None):
        self._increment = increment or 0
        self._dt = dt or 0

        self._running: bool = False
        self._value: Optional[int] = None
        self._total: Optional[int] = None

        self._next_time = None
        self._next_value = None

    # *** Public interface

    def start(self, total: int) -> None:
        self._running = True
        self._value = 0
        self._total = total
        self._next_value = self._increment
        self._next_time = monotonic() + self._dt
        self._start(total)

    def value(self):
        return self._value

    def set_value(self, value: int) -> None:
        if not self._running:
            # Ignore while not yet started or already finished
            return
        elif value >= self._total:
            # Done
            self._value = self._total
            self._progress(self._total, self._total)
            self._running = False
            self._done()
        else:
            self._value = value
            if value >= self._next_value:
                self._next_value += self._increment
                t = monotonic()
                if t >= self._next_time:
                    self._next_time += self._dt
                    self._progress(self._value, self._total)

    def done(self) -> None:
        self.set_value(self._total)

    def next(self, count: int = 1) -> None:
        self.set_value(self._value + 1)

    def wrap(self, value, /, count: int = 1):
        self.next(count)
        return value

    # *** Implementation interface

    def _start(self, total: int):
        pass

    def _progress(self, value: int):
        pass

    def _done(self):
        pass


class TextProgressMonitor(ProgressMonitor):
    def _progress(self, value, total) -> bool:
        print(f"{value}/{total} ", end="")
