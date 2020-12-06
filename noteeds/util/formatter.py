import string


class Formatter(string.Formatter):
    def __init__(self):
        super().__init__()
        self.unused = set()

    def check_unused_args(self, used_args, args, kwargs):
        super().check_unused_args(used_args, args, kwargs)
        all_args = set(range(len(args))) | set(kwargs.keys())
        self.unused = all_args - used_args
