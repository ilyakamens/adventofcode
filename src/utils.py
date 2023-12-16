from collections.abc import Iterable, Sequence, deque
from itertools import islice
from typing import TypeVar

T = TypeVar("T")


def chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i : i + size]


def rotate_cw(matrix):
    return [list(l) for l in list(zip(*matrix))[::-1]]


def rotate_ccw(matrix):
    return [list(l) for l in list(zip(*matrix[::-1]))]


# Taken from Zak.
def flip_rows_cols(lines: Sequence[str]) -> list[str]:
    return ["".join(x).strip() for x in zip(*lines)]


# Taken from Zak.
def sliding_window(iterable: Iterable[T], n: int) -> Iterable[Iterable[T]]:
    """sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG."""
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)
