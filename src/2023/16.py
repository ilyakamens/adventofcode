#!/usr/bin/env python

"""https://adventofcode.com/2023/day/16."""

from collections import defaultdict
import copy
from dataclasses import dataclass
from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


@dataclass
class Solver:
    grid: list[list[str]]
    print_enabled: bool = False

    def print(self, px, py, dx, dy):
        if not self.print_enabled:
            return

        mapping = {(1, 0): ">", (-1, 0): "<", (0, 1): "v", (0, -1): "^"}
        count = len(self.energized[(px, py)])
        if self.gridcopy[py][px] in ["."] + list(mapping.values()):
            self.gridcopy[py][px] = mapping[(dx, dy)] if count < 2 else str(count)
        for row in self.gridcopy:
            print(" ".join(row))
        print()

    def traverse(self, position: tuple[int, int] = (0, 0), direction: tuple[int, int] = (1, 0)):
        self.energized = defaultdict(set)
        self.gridcopy = copy.deepcopy(self.grid)

        return self._traverse(*position, *direction)

    def _traverse(self, px: int, py: int, dx: int, dy: int):
        while px >= 0 and py >= 0 and py < len(self.grid) and px < len(self.grid[py]):
            if (dx, dy) in self.energized[(px, py)]:
                break

            self.energized[(px, py)].add((dx, dy))

            self.print(px, py, dx, dy)

            tile = self.grid[py][px]
            if tile == ".":
                pass
            elif tile == "/":
                dx, dy = -dy, -dx
            elif tile == "\\":
                dx, dy = dy, dx
            elif tile == "|" and dx != 0:
                self._traverse(px, py - 1, 0, -1)
                self._traverse(px, py + 1, 0, 1)
                break
            elif tile == "-" and dy != 0:
                self._traverse(px + 1, py, 1, 0)
                self._traverse(px - 1, py, -1, 0)
                break
            px += dx
            py += dy

        return len(self.energized)


def p1(grid):
    return Solver(grid).traverse()


def p2(lines):
    best = 0

    solver = Solver(lines)

    for px in range(len(lines[0])):
        best = max(solver.traverse((px, 0), (0, 1)), best)

    for px in range(len(lines[0])):
        best = max(solver.traverse((px, len(lines) - 1), (0, -1)), best)

    for py in range(len(lines)):
        best = max(solver.traverse((len(lines[0]) - 1, py), (-1, 0)), best)

    for py in range(len(lines)):
        best = max(solver.traverse((0, py), (1, 0)), best)

    return best


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "16.txt")) as f:
        lines = [list(l) for l in f.read().splitlines()]

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
