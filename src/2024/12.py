#!/usr/bin/env python

"""https://adventofcode.com/2024/day/12."""

from collections import deque

from main import main, runs
from utils import Dir, Dir8, Grid, Point


class Garden(Grid):
    def __init__(self, input: str):
        super().__init__(input)
        self.visited = set()

    def get_region(self, p: Point) -> list[Point]:
        if p in self.visited:
            return []

        visited = [p]
        queue = deque([p])
        while queue:
            current = queue.popleft()
            for neighbor in self.neighbors(current, Dir):
                if (
                    neighbor in self.visited
                    or neighbor in visited
                    or self[neighbor] != self[current]
                ):
                    continue
                visited.append(neighbor)
                queue.append(neighbor)

        self.visited.update(set(visited))

        return visited

    def calc_perimeter(self, region: list[Point]) -> int:
        perimeter = 0
        for p in region:
            for neighbor in self.neighbors(p, Dir, allow_out=True):
                if neighbor not in region:
                    perimeter += 1

        return perimeter

    def get_corners(self, region: list[Point]) -> set[tuple[Point, Dir]]:
        corners = set()

        directions = list(Dir8.iter())
        directions.append(directions[0])
        for p in region:
            for start in range(0, len(directions) - 1, 2):
                end = start + 3
                s1, c, s2 = directions[start:end]
                if (
                    self.neighbor(p, s1) not in region
                    and self.neighbor(p, c) not in region
                    and self.neighbor(p, s2) not in region
                ):
                    corners.add((p, s1, c, s2))
                elif (
                    self.neighbor(p, s1) in region
                    and self.neighbor(p, c) not in region
                    and self.neighbor(p, s2) in region
                ):
                    corners.add((p, s1, c, s2))
                elif (
                    self.neighbor(p, s1) not in region
                    and self.neighbor(p, c) in region
                    and self.neighbor(p, s2) not in region
                ):
                    corners.add((p, s1, c, s2))

        return corners


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    grid = Garden(input)

    sums = 0
    regions = [grid.get_region(p) for p in grid.iter()]
    for region in regions:
        if not region:
            continue
        plots = grid.calc_perimeter(region)
        sums += len(region) * plots

    return sums


@runs(cases={'1', '2', '3', '4', '5'})
def p2(input: str, case: str) -> int:
    grid = Garden(input)

    sums = 0
    regions = [grid.get_region(p) for p in grid.iter()]
    for region in regions:
        if not region:
            continue
        sums += len(region) * len(grid.get_corners(region))

    return sums


if __name__ == '__main__':
    main(p1, p2, [140, None, None, None, None], [80, 436, 236, 368, 1206])
