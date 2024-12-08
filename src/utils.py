import re
from collections import defaultdict, deque
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations, islice
from math import prod
from typing import Generic, Iterator, TypeVar

T = TypeVar('T')

Vector = tuple[int, int]

int_re = re.compile(r'[-+]?\d+')


def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)

    return factors


def divisors(n):
    factors = prime_factors(n)

    divisors = set()
    for i in range(1, len(factors) + 1):
        for c in combinations(factors, i):
            divisors.add(prod(c))

    return divisors


# Inspired by zakj.
def paras(input: str) -> list[str]:
    return [x.strip() for x in input.split('\n\n')]


# Inspired by zakj.
def numbers(line: str, cast=True) -> list[int]:
    return [int(x) if cast else x for x in int_re.findall(line)]


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

    def __contains__(self, x: int) -> bool:
        return x in self.m

    def contains(self, x, y):
        return x in self.m and y in self.m[x]

    def iter(self):
        for y in range(len(self.m)):
            for x in range(len(self.m[y])):
                yield x, y

    def corner(self, dir: DirDiag) -> tuple[int, int]:
        if dir == DirDiag.NW:
            return 0, 0
        if dir == DirDiag.NE:
            return len(self.m) - 1, 0
        if dir == DirDiag.SE:
            return len(self.m) - 1, len(self.m[0]) - 1
        if dir == DirDiag.SW:
            return 0, len(self.m[0]) - 1

    def corners(self) -> set[tuple[int, int]]:
        return {self.corner(dir) for dir in DirDiag.iter()}

    def neighbors(self, x: int, y: int, dir=Dir8) -> list[tuple[int, int]]:
        neighbors = []
        for dx, dy in dir.iter():
            nx, ny = x + dx, y + dy
            if self.contains(nx, ny):
                neighbors.append((nx, ny))

        return neighbors

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


@dataclass
class Node(Generic[T]):
    val: T
    prev: 'Node' = None
    next: 'Node' = None

    def __str__(self) -> str:
        return str(self.val)

    def __repr__(self) -> str:
        return f'Node({self.val})'


class LL(Generic[T]):
    """Doubly linked list."""

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size = 0

    def append(self, val: T):
        new_node = Node(val)
        self.size += 1

        if not self.head:
            self.head = self.tail = new_node
            return

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def prepend(self, val: T):
        new_node = Node(val)
        self.size += 1

        if not self.head:
            self.head = self.tail = new_node
            return

        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def insert(self, val: T, after: Node):
        if after == self.tail:
            self.append(val)
            return

        new_node = Node(val)
        new_node.next = after.next
        new_node.prev = after
        after.next.prev = new_node
        after.next = new_node
        self.size += 1

    def remove(self, node: Node):
        self.size -= 1

        if node == self.head == self.tail:
            self.head = self.tail = None
            return

        if node == self.head:
            self.head = node.next
            node.next.prev = None
            return

        if node == self.tail:
            self.tail = node.prev
            node.prev.next = None
            return

        node.prev.next = node.next
        node.next.prev = node.prev

    def itervals(self):
        node = self.head
        while node:
            yield node.val
            node = node.next

    def __len__(self):
        return self.size

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next

    def __reversed__(self):
        node = self.tail
        while node:
            yield node
            node = node.prev

    def __str__(self) -> str:
        return ' -> '.join(str(x) for x in self)
