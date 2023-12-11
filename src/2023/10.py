#!/usr/bin/env python

"""https://adventofcode.com/2023/day/10."""

from collections import deque
from dataclasses import dataclass
from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

GRID = []


@dataclass
class Node:
    value: str
    x: int
    y: int
    distance: int = 0
    expanded: bool = False

    @property
    def next(self):
        if self.value == "F":
            n1 = GRID[self.y][self.x + 1]
            n2 = GRID[self.y + 1][self.x]
        if self.value == "-":
            n1 = GRID[self.y][self.x - 1]
            n2 = GRID[self.y][self.x + 1]
        if self.value == "7":
            n1 = GRID[self.y][self.x - 1]
            n2 = GRID[self.y + 1][self.x]
        if self.value == "|":
            n1 = GRID[self.y - 1][self.x]
            n2 = GRID[self.y + 1][self.x]
        if self.value == "J":
            n1 = GRID[self.y - 1][self.x]
            n2 = GRID[self.y][self.x - 1]
        if self.value == "L":
            n1 = GRID[self.y - 1][self.x]
            n2 = GRID[self.y][self.x + 1]

        filtered = [n for n in [n1, n2] if n.value != "S" and n.distance == 0]
        if not filtered:
            return None

        filtered[0].distance = self.distance + 1

        return filtered[0]

    @property
    def starting_nodes(self):
        for xd, yd in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x = self.x + xd
            y = self.y + yd
            if x < 0 or y < 0 or x >= len(GRID[0]) or y >= len(GRID):
                continue
            node = GRID[y][x]
            if node.value == "F" and (xd == -1 or yd == -1):
                yield node
            elif node.value == "-" and xd != 0:
                yield node
            elif node.value == "7" and (xd == 1 or yd == -1):
                yield node
            elif node.value == "|" and yd != 0:
                yield node
            elif node.value == "J" and (yd == 1 or xd == 1):
                yield node
            elif node.value == "L" and (xd == -1 or yd == 1):
                yield node

    @property
    def adjacent_nodes(self):
        for xd, yd in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x = self.x + xd
            y = self.y + yd
            if x < 0 or y < 0 or x >= len(GRID[0]) or y >= len(GRID):
                continue
            yield GRID[y][x]

    @property
    def has_exit(self):
        if self.distance:
            return False

        for xd, yd in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x = self.x + xd
            y = self.y + yd
            if x < 0 or y < 0 or x >= len(GRID[0]) or y >= len(GRID):
                return True
            if GRID[y][x].value == "O":
                return True

        return False


def expandx():
    x = y = 0
    while y < len(GRID):
        x = 0
        row = GRID[y]
        while x < len(row) - 1:
            cur = row[x]
            next_x = row[x + 1]
            if any(not n.distance for n in [cur, next_x]):
                value = "."
                distance = 0
            elif (
                any(n.value == "-" for n in [cur, next_x])
                or cur.value in {"F", "L"}
                or next_x.value in {"J", "7"}
            ):
                value = "-"
                distance = -2
            else:
                value = "."
                distance = 0
            row.insert(x + 1, Node(value, x + 1, y, distance=distance, expanded=True))
            row[x + 2].x = row[x + 1].x + 1
            x += 2
        y += 1


def expandy():
    y = 0
    while y < len(GRID) - 1:
        x = 0
        row = GRID[y]
        yrow = []
        while x < len(row):
            cur = row[x]
            next_y = GRID[y + 1][x]
            next_y.y = y + 2
            if any(not n.distance for n in [cur, next_y]):
                value = "."
                distance = 0
            elif (
                any(n.value == "|" for n in [cur, next_y])
                or cur.value in {"F", "7"}
                or next_y.value in {"J", "L"}
            ):
                value = "|"
                distance = -2
            else:
                value = "."
                distance = 0
            yrow.append(Node(value, x, y + 1, distance=distance, expanded=True))
            x += 1
        GRID.insert(y + 1, yrow)
        y += 2


def p1(lines):
    global GRID

    start = None

    for y, line in enumerate(lines):
        GRID.append([])
        for x, char in enumerate(line):
            GRID[y].append(Node(char, x, y))
            if char == "S":
                start = GRID[y][x]
                start.distance = -1

    q = deque()

    for node in start.starting_nodes:
        node.distance = 1
        q.append(node)

    while len(q) > 1:
        node = q.popleft()
        next_ = node.next
        if next_:
            q.append(next_)

    return q[0].distance


def p2():
    expandx()
    expandy()

    perimeter_coords = []
    for x in range(0, len(GRID[0])):
        perimeter_coords.append((x, 0))

    for y in range(1, len(GRID)):
        perimeter_coords.append((len(GRID[0]) - 1, y))

    for x in range(len(GRID[0]) - 2, -1, -1):
        perimeter_coords.append((x, len(GRID) - 1))

    for y in range(len(GRID) - 2, 0, -1):
        perimeter_coords.append((0, y))

    q = deque()
    for x, y in perimeter_coords:
        node = GRID[y][x]
        if not node.distance:
            q.append(node)

    while len(q):
        node = q.popleft()
        if not node.has_exit or node.value == "O":
            continue
        node.value = "O"
        for n in node.adjacent_nodes:
            q.append(n)

    trapped = 0
    for row in GRID:
        for node in row:
            if not node.has_exit and not node.distance and not node.expanded:
                trapped += 1

    return trapped


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "10.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2()}")
