import sys

from noteeds.util.progress import Monitor


class TextMonitor(Monitor):
    def __init__(self, line_end: str = "\n", end: str = "", *, file=sys.stdout):
        self._file = file
        self._line_end: str = line_end
        self._end: str = end
        self._total: int = 0

    def start(self, total: int) -> None:
        self._total = total

    def progress(self, value: int) -> None:
        print(f"{value/self._total*100:.0f}%", end=self._line_end, file=self._file)

    def done(self) -> None:
        print("", end=self._end, file=self._file)
