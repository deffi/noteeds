from noteeds.util import Formatter


class MultiFormatter:
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

        self._formatter = Formatter()
        self.unused = set(range(len(args))) |set(kwargs.keys())

    def format(self, format_string):
        result = self._formatter.vformat(format_string, self.args, self.kwargs)
        self.unused &= self._formatter.unused
        return result
