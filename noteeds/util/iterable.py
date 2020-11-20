from typing import Iterable, Sequence


def pairs(items: Iterable) -> Iterable:
    return zip(items[:-1], items[1:])


def sequence_join(sep: Sequence, sequences: Sequence[Sequence]):
    if sequences:
        yield from sequences[0]

    for sequence in sequences[1:]:
        yield from sep
        yield from sequence
