import heapq
import re
from collections import defaultdict, deque
from collections.abc import Callable, Generator, Iterable
from dataclasses import dataclass
from itertools import combinations, islice
from math import prod
from operator import le, lt
from typing import Generic, Iterator, TypeVar

T = TypeVar('T')

Vector = tuple[int, int]
Point = tuple[int, int]

int_re = re.compile(r'[-+]?\d+')


def binary_search(f: Callable[[int], bool], low: int, high: int) -> int:
    while low < high:
        mid = (low + high) // 2
        if f(mid):
            low = mid + 1
        else:
            high = mid - 1

    return low


def sum_tuples(t1: tuple[T, ...], t2: tuple[T, ...]) -> tuple[T, ...]:
    return tuple(x + y for x, y in zip(t1, t2))


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


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


# Taken from zakj.
class IterableClass[T](type):
    @classmethod
    def iter(cls):
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        return self.iter()


# Inspired by zakj's.
class Dir(metaclass=IterableClass):
    N: Vector = (0, -1)
    E: Vector = (1, 0)
    S: Vector = (0, 1)
    W: Vector = (-1, 0)

    @classmethod
    def iter(cls) -> Iterator[Vector]:
        for d in [cls.N, cls.E, cls.S, cls.W]:
            yield d

    @classmethod
    def opposite(cls, dir: Vector) -> Vector:
        return {cls.N: cls.S, cls.E: cls.W, cls.S: cls.N, cls.W: cls.E}[dir]


# Inspired by zakj's.
class DirDiag(metaclass=IterableClass):
    NE: Vector = (1, -1)
    SE: Vector = (1, 1)
    SW: Vector = (-1, 1)
    NW: Vector = (-1, -1)

    @classmethod
    def iter(cls) -> Iterator[Vector]:
        for d in [cls.NE, cls.SE, cls.SW, cls.NW]:
            yield d

    @classmethod
    def opposite(cls, dir: Vector) -> Vector:
        return {cls.NE: cls.SW, cls.SE: cls.NW, cls.SW: cls.NE, cls.NW: cls.SE}[dir]


# Inspired by zakj's.
class Dir8(Dir, DirDiag, metaclass=IterableClass):
    @classmethod
    def iter(cls) -> Iterator[Vector]:
        for d in [cls.N, cls.NE, cls.E, cls.SE, cls.S, cls.SW, cls.W, cls.NW]:
            yield d

    @classmethod
    def opposite(cls, dir: Vector) -> Vector:
        return {
            cls.N: cls.S,
            cls.E: cls.W,
            cls.S: cls.N,
            cls.W: cls.E,
            cls.NE: cls.SW,
            cls.SE: cls.NW,
            cls.SW: cls.NE,
            cls.NW: cls.SE,
        }[dir]


class Grid:
    @classmethod
    def from_dimensions(cls, rows: int, cols: int, default: str = '.') -> 'Grid':
        s = ''
        for _ in range(rows):
            for _ in range(cols):
                s += default
            s += '\n'

        return cls(s)

    def __init__(self, input: str, t: str | int = str):
        self.m = {}
        self.width = 0
        self.height = 0

        for y, line in enumerate(input.strip().splitlines()):
            for x, c in enumerate(line):
                self[(x, y)] = c if t is str else int(c)
            self.width = max(self.width, x + 1)
            self.height = max(self.height, y + 1)

    def __getitem__(self, point: Point) -> T:
        return self.m[point]

    def __setitem__(self, point: Point, value: T):
        self.m[point] = value

    def __contains__(self, point: Point) -> bool:
        return point in self.m

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y

    def corner(self, dir: DirDiag) -> Point:
        if dir == DirDiag.NW:
            return 0, 0
        if dir == DirDiag.NE:
            return self.width - 1, 0
        if dir == DirDiag.SE:
            return self.width - 1, self.height - 1
        if dir == DirDiag.SW:
            return 0, self.height - 1

    def corners(self) -> set[Point]:
        return {self.corner(dir) for dir in DirDiag.iter()}

    def neighbor(self, p: Point, dir=Dir) -> Point:
        return sum_tuples(p, dir)

    def neighbors(self, p: Point, dir=Dir, allow_out=False) -> list[Point]:
        neighbors = []
        for d in dir.iter():
            n = sum_tuples(p, d)
            if n in self or allow_out:
                neighbors.append(n)

        return neighbors

    def find(self, value: T) -> Point:
        for point in self:
            if self[point] == value:
                return point

    # Inspired by zakj.
    def findall(self, value: T) -> list[Point]:
        coords = []
        for point in self:
            if self[point] == value:
                coords.append(point)

        return coords

    def substr(self, point: Point, dir: Dir | DirDiag | Dir8, length: int, offset=0):
        dirx, diry = dir

        s = ''
        for i in range(length):
            x = point.x + (i * dirx) + (offset * dirx)
            y = point.y + (i * diry) + (offset * diry)
            s += self[(x, y)]

        return s

    def rotate_ccw(self) -> 'Grid':
        rotated = Grid('')
        for y in range(self.height):
            for x in range(self.width):
                rotated.m[(y, self.width - 1 - x)] = self.m[(x, y)]

        self.m = rotated.m

    def rotate_cw(self) -> 'Grid':
        rotated = Grid('')
        for y in range(self.height):
            for x in range(self.width):
                rotated.m[(self.height - 1 - y, x)] = self.m[(x, y)]

        self.m = rotated.m

    def flip_x(self) -> 'Grid':
        flipped = Grid('')
        for y in range(self.height):
            for x in range(self.width):
                flipped.m[(self.width - 1 - x, y)] = self.m[(x, y)]

        self.m = flipped.m

    def flip_y(self) -> 'Grid':
        flipped = Grid('')
        for y in range(self.height):
            for x in range(self.width):
                flipped.m[(x, self.height - 1 - y)] = self.m[(x, y)]

        self.m = flipped.m

    def __eq__(self, other: 'Grid') -> bool:
        return self.m == other.m

    def __str__(self) -> str:
        if not self.m:
            return ''

        rows = []
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                row += str(self[(x, y)])
            rows.append(row)

        return '\n'.join(rows) + '\n'


@dataclass
class AStarNode:
    grid: 'AStarGrid'
    p: Point

    def __hash__(self):
        return hash(self.p)

    def __lt__(self, other: 'AStarNode'):
        return self.grid.total_costs[self] < self.grid.total_costs[other]

    def __eq__(self, other: 'AStarNode'):
        return self.p == other.p


class AStarGrid(Grid):
    def __init__(self, input: str, dir: Dir | DirDiag | Dir8 = Dir):
        super().__init__(input)

        self.dir = dir

        self.total_costs = defaultdict(lambda: float('inf'))
        self.came_from = defaultdict(set)
        self.best_total_cost = float('inf')

    def heuristic(self, start_pos: Point, end_pos: Point) -> int:
        return manhattan(start_pos, end_pos)

    def cost(self, f: AStarNode, t: AStarNode) -> int:
        return 1

    def get_neighbors(self, node: AStarNode) -> list[AStarNode]:
        return [AStarNode(self, p) for p in self.neighbors(node.p, self.dir)]

    def shortest_path(
        self,
        start_node: AStarNode,
        end_pos: Point,
        op: Callable[[int, int], bool] = lt,
    ) -> Generator[AStarNode]:
        heap: list[AStarNode] = []
        heapq.heappush(heap, start_node)

        partial_costs = defaultdict(lambda: float('inf'))
        partial_costs[start_node] = 0

        self.total_costs[start_node] = self.heuristic(start_node.p, end_pos)

        while heap:
            cur = heapq.heappop(heap)

            if cur.p == end_pos:
                # NOTE: This won't ever change.
                self.best_total_cost = self.total_costs[cur]
                yield cur
                continue

            for neighbor in self.get_neighbors(cur):
                if neighbor in self.came_from[cur]:
                    continue
                partial_cost = partial_costs[cur] + self.cost(cur, neighbor)
                total_cost = partial_cost + self.heuristic(neighbor.p, end_pos)
                if total_cost <= self.best_total_cost and op(partial_cost, partial_costs[neighbor]):
                    self.came_from[neighbor].add(cur)
                    partial_costs[neighbor] = partial_cost
                    self.total_costs[neighbor] = total_cost
                    if neighbor not in heap:
                        heapq.heappush(heap, neighbor)

    def shortest_paths(self, start_node: AStarNode, end_pos: Point) -> Generator[AStarNode]:
        return self.shortest_path(start_node, end_pos, op=le)

    def all_path_points(self, end: AStarNode) -> set[Point]:
        seen = set()

        froms = {end}
        while froms:
            node = froms.pop()
            seen.add(node.p)
            froms.update(self.came_from[node])

        return seen


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
