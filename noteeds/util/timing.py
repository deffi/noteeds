from contextlib import contextmanager
from time import perf_counter
from typing import Generator


@contextmanager
def stopwatch(description: str) -> Generator:
    start_time = perf_counter()
    yield
    end_time = perf_counter()
    duration = end_time - start_time
    print(f"Time for {description}: {duration:.2f} s")
