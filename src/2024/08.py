#!/usr/bin/env python

"""https://adventofcode.com/2024/day/8."""

from itertools import combinations

from main import main, runs
from utils import Grid


def diff(x1, y1, x2, y2):
    return (x1 - x2, y1 - y2)


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    grid = Grid(input)
    antennae = set()

    grid2 = Grid(input)

    for x, y in grid.iter():
        if grid[x][y] != '.':
            antennae.add(grid[x][y])

    for antenna in antennae:
        locs = list(grid.findall(antenna))
        for (x1, y1), (x2, y2) in combinations(locs, 2):
            dx, dy = diff(x1, y1, x2, y2)
            antinode1 = x1 + dx, y1 + dy
            antinode2 = x2 - dx, y2 - dy
            a1x, a1y = antinode1
            a2x, a2y = antinode2
            if grid.contains(*antinode1):
                grid2[a1x][a1y] = '#'
            if grid.contains(*antinode2):
                grid2[a2x][a2y] = '#'

    return len(grid2.findall('#'))


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    grid = Grid(input)
    antennae = set()

    grid2 = Grid(input)

    acount = 0
    for x, y in grid.iter():
        if grid[x][y] != '.':
            acount += 1
            antennae.add(grid[x][y])

    for antenna in antennae:
        print(antenna)
        locs = list(grid.findall(antenna))
        for (x1, y1), (x2, y2) in combinations(locs, 2):
            print((x1, y1), (x2, y2))
            dx, dy = diff(x1, y1, x2, y2)
            antinode1 = x1 + dx, y1 + dy
            antinode2 = x2 - dx, y2 - dy
            a1x, a1y = antinode1
            a2x, a2y = antinode2
            while grid.contains(a1x, a1y):
                grid2[a1x][a1y] = '#'
                a1x += dx
                a1y += dy
            while grid.contains(a2x, a2y):
                grid2[a2x][a2y] = '#'
                a2x -= dx
                a2y -= dy

    acount = 0
    for x, y in grid2.iter():
        if grid2[x][y] not in {'.', '#'}:
            acount += 1

    print(grid2)

    return len(grid2.findall('#')) + acount


if __name__ == '__main__':
    main(p1, p2, [14], [34])
