import string


class MultiFormatter(string.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

        self.unused = set(range(len(args))) |set(kwargs.keys())

    # TODO violates Liskov, also the duplicate format/vformat is ridiculous. Compose a util.Formatter.
    def format(self, format_string):
        return self.vformat(format_string)

    def vformat(self, format_string):
        return super().vformat(format_string, self.args, self.kwargs)

    def check_unused_args(self, used_args, args, kwargs):
        super().check_unused_args(used_args, args, kwargs)
        self.unused -= used_args
