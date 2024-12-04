from collections import defaultdict, deque
from collections.abc import Iterable
from itertools import islice
from typing import Iterator, TypeVar

T = TypeVar('T')

Vector = tuple[int, int]


def numbers(line: str) -> list[int]:
    return [int(x) for x in line.split()]


def chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i : i + size]


def rotate_cw(matrix):
    return [list(l) for l in list(zip(*matrix))[::-1]]


def rotate_ccw(matrix):
    return [list(l) for l in list(zip(*matrix[::-1]))]


# Modified from zakj's.
def flip_rows_cols(lines: list[str] | list[list[str]] | list[list[int]]) -> list[str]:
    flipped = []

    for x in zip(*lines):
        if isinstance(lines[0], str):
            flipped.append(''.join(x).strip())
        elif isinstance(lines[0], list):
            flipped.append(list(x))

    return flipped


# Taken from zakj.
def sliding_window(iterable: Iterable[T], n: int) -> Iterable[Iterable[T]]:
    """sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG."""
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


# Inspired by zakj's.
class Dir:
    N: Vector = (0, -1)
    E: Vector = (1, 0)
    S: Vector = (0, 1)
    W: Vector = (-1, 0)

    @classmethod
    def iter(cls) -> Iterator[Vector]:
        for d in [cls.N, cls.E, cls.S, cls.W]:
            yield d


# Inspired by zakj's.
class DirDiag:
    NE: Vector = (1, -1)
    SE: Vector = (1, 1)
    SW: Vector = (-1, 1)
    NW: Vector = (-1, -1)

    @classmethod
    def iter(cls) -> Iterator[Vector]:
        for d in [cls.NE, cls.SE, cls.SW, cls.NW]:
            yield d


# Inspired by zakj's.
class Dir8(Dir, DirDiag):
    @classmethod
    def iter(cls) -> Iterator[Vector]:
        for d in [cls.N, cls.NE, cls.E, cls.SE, cls.S, cls.SW, cls.W, cls.NW]:
            yield d


class Grid:
    def __init__(self, input: str, t: str | int = str):
        self.m = defaultdict(lambda: defaultdict(t))

        for y, line in enumerate(input.splitlines()):
            for x, c in enumerate(line):
                self.m[x][y] = c if t is str else int(c)

    def __getitem__(self, x: int) -> dict[int, T]:
        return self.m[x]

    def iter(self):
        for y in range(len(self.m)):
            for x in range(len(self.m[y])):
                yield x, y

    # Inspired by zakj.
    def findall(self, value: T) -> list[tuple[int, int]]:
        coords = []
        for x, y in self.iter():
            if self[x][y] == value:
                coords.append((x, y))

        return coords

    def substr(self, x: int, y: int, dir: Dir | DirDiag | Dir8, length: int, offset=0):
        dirx, diry = dir

        s = ''
        for i in range(length):
            s += self[x + (i * dirx) + (offset * dirx)][y + (i * diry) + (offset * diry)]

        return s

    def rotate_cw(self) -> 'Grid':
        height = len(self.m[0])
        width = len(self.m)

        rotated = Grid('')
        for y in range(height):
            for x in range(width):
                rotated.m[y][width - 1 - x] = self.m[x][y]

        self.m = rotated.m

    def rotate_ccw(self) -> 'Grid':
        height = len(self.m[0])
        width = len(self.m)

        rotated = Grid('')
        for y in range(height):
            for x in range(width):
                rotated.m[height - 1 - y][x] = self.m[x][y]

        self.m = rotated.m

    def flip_x(self) -> 'Grid':
        width = len(self.m)
        height = len(self.m[0])

        flipped = Grid('')
        for y in range(height):
            for x in range(width):
                flipped.m[width - 1 - x][y] = self.m[x][y]

        self.m = flipped.m

    def flip_y(self) -> 'Grid':
        width = len(self.m)
        height = len(self.m[0])

        flipped = Grid('')
        for y in range(height):
            for x in range(width):
                flipped.m[x][height - 1 - y] = self.m[x][y]

        self.m = flipped.m

    def __eq__(self, other: 'Grid') -> bool:
        return self.m == other.m

    def __str__(self) -> str:
        if not self.m:
            return ''

        rows = []
        for y in range(len(self.m)):
            row = ''
            for x in range(len(self.m[0])):
                row += str(self.m[x][y])
            rows.append(row)

        return '\n'.join(rows) + '\n'
