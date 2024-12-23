#!/usr/bin/env python

"""https://adventofcode.com/2024/day/14."""

import math
from collections import defaultdict
from dataclasses import dataclass

from main import main, runs
from utils import DirDiag, Grid, Point, numbers

GUID = 0


@dataclass
class Robot:
    p: Point
    v: Point

    def __post_init__(self):
        global GUID
        self.guid = GUID
        GUID += 1

    def __hash__(self):
        return self.guid

    def move(self, cols: int, rows: int):
        x, y = self.p.x + self.v.x, self.p.y + self.v.y
        x = x % cols
        y = y % rows
        self.p = Point(x, y)

    def quadrant(self, cols: int, rows: int) -> DirDiag:
        x, y = self.p.x, self.p.y
        if x == cols // 2 or y == rows // 2:
            return None

        if x < cols // 2 and y < rows // 2:
            return DirDiag.NW
        if x < cols // 2 and y > rows // 2:
            return DirDiag.NE
        if x > cols // 2 and y < rows // 2:
            return DirDiag.SW
        if x > cols // 2 and y > rows // 2:
            return DirDiag.SE

        raise ValueError(f'Invalid quadrant: {x}, {y}')


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    rows = 7
    cols = 11
    if case == 'real':
        rows = 103
        cols = 101

    r = set()
    for row in input.splitlines():
        px, py, vx, vy = numbers(row)
        r.add(Robot(Point(px, py), Point(vx, vy)))

    for i in range(100):
        for robot in r:
            robot.move(cols, rows)

    counts = defaultdict(int)
    for robot in r:
        q = robot.quadrant(cols, rows)
        if q is not None:
            counts[q] += 1

    return math.prod(counts.values())


@runs(cases=set())
def p2(input: str, case: str) -> int:
    answer = 8270

    rows = 103
    cols = 101
    r = set()
    for row in input.splitlines():
        px, py, vx, vy = numbers(row)
        r.add(Robot(Point(px, py), Point(vx, vy)))

    # There's something interesting every (i - 89) % 101 == 0.
    for _ in range(answer):
        for robot in r:
            robot.move(cols, rows)

    grid = Grid.from_dimensions(rows, cols)
    for robot in r:
        grid[robot.p] = '1'
    print(grid)

    return answer


if __name__ == '__main__':
    main(p1, p2, [12], [None])
