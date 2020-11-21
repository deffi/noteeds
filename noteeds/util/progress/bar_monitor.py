import sys

from noteeds.util.progress import Monitor


class BarMonitor(Monitor):
    def __init__(self, length: int, *, file=sys.stdout):
        self._length = length
        self._file = file

        self._total: int = 0

    def start(self, total: int) -> None:
        self._total = total

        print("[" + " " * self._length + "]", end="")

    def progress(self, value: int) -> None:
        l = int(self._length * value / self._total)
        print("\b" * (self._length + 2), end="")
        print("[" + "#" * l + " " * (self._length - l) + "]", end="")

    def done(self) -> None:
        print(file=self._file)
