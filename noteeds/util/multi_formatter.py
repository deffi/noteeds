from noteeds.util import Formatter


class MultiFormatter:
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

        self._formatter = Formatter()
        self.unused = set(range(len(args))) | set(kwargs.keys())

    def format(self, format_string, use=True):
        result = self._formatter.vformat(format_string, self.args, self.kwargs)
        if use:
            self.unused &= self._formatter.unused
        return result

    def format_field(self, field_name, format_spec="", conversion=None, *, use=True):
        field_name = str(field_name)
        obj, used_value = self._formatter.get_field(field_name, self.args, self.kwargs)
        obj = self._formatter.convert_field(obj, conversion)
        if use:
            self.unused -= {used_value}
        return self._formatter.format_field(obj, format_spec)
