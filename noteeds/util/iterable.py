from typing import Iterable

def pairs(items: Iterable) -> Iterable:
    return zip(items[:-1], items[1:])
