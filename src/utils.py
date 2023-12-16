from collections.abc import Iterable, deque
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


# Modified from Zak's.
def flip_rows_cols(lines: list[str] | list[list[str]] | list[list[int]]) -> list[str]:
    flipped = []

    for x in zip(*lines):
        if isinstance(lines[0], str):
            flipped.append("".join(x).strip())
        elif isinstance(lines[0], list):
            flipped.append(list(x))

    return flipped


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
