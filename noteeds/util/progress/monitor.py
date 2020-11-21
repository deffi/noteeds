class Monitor:
    def start(self, total: int) -> None:
        pass

    def progress(self, value: int) -> None:
        raise NotImplementedError

    def done(self) -> None:
        pass
