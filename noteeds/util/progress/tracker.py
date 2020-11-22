from typing import Optional, TypeVar
from time import monotonic

from noteeds.util.progress import Monitor


T = TypeVar("T")


class Tracker:
    def __init__(self, monitor: Optional[Monitor], *,
                 steps: Optional[int] = None, delta: Optional[int] = None, delta_t: Optional[float] = None):
        if steps is not None and delta is not None:
            raise ValueError("Only one of steps and delta can be specified")

        self._monitor = monitor
        self._steps = steps
        self._delta = delta
        self._delta_t = delta_t or 0

        self._total = None

        self._running = False
        self._progress = None
        self._next_time = None
        self._next_value = None

    def start(self, total: int) -> None:
        if not self._monitor:
            return

        self._total = total

        if self._steps:
            self._delta = total / self._steps

        self._running = True
        self._progress = 0
        self._next_value = self._delta
        self._next_time = monotonic() + self._delta_t

        self._monitor.start(total)

    def progress(self, progress: int) -> None:
        if not self._monitor:
            return

        # Ignore if not yet started or already done
        if not self._running:
            return

        if progress >= self._total:
            # Done
            self._running = False
            self._progress = self._total
            self._monitor.progress(self._total)
            self._monitor.done()
        else:
            self._progress = progress

            notify_monitor = False

            if self._delta and progress >= self._next_value:
                self._next_value += self._delta
                notify_monitor = True

            if self._delta_t and monotonic() >= self._next_time:
                self._next_time += self._delta_t
                notify_monitor = True

            if notify_monitor:
                self._monitor.progress(progress)

    def next(self, increment: int = 1) -> None:
        self.progress(self._progress + increment)

    def done(self) -> None:
        self.progress(self._total)

    def wrap(self, value: T, /, increment: int = 1) -> T:
        self.next(increment)
        return value
