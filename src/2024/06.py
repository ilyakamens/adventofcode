#!/usr/bin/env python

"""https://adventofcode.com/2024/day/6."""

from collections import defaultdict

from main import main, runs
from utils import Dir, Grid


class GuardGrid(Grid):
    def __init__(self, input: str):
        super().__init__(input)

        self.last_carot = None
        self.guard: tuple[int, int] = self.findall('^')[0]
        self.dir: Dir = Dir.N

    def turn(self):
        self.dir = {Dir.N: Dir.E, Dir.E: Dir.S, Dir.S: Dir.W, Dir.W: Dir.N}[self.dir]

    @property
    def carot(self) -> str:
        return {Dir.N: '^', Dir.E: '>', Dir.S: 'v', Dir.W: '<'}[self.dir]

    def move(self):
        x, y = self.guard
        nx, ny = (x + self.dir[0], y + self.dir[1])

        if nx not in self or ny not in self[nx]:
            self[x][y] = 'X'
            return False

        if self[nx][ny] in {'.', 'X'}:
            self[nx][ny] = self.carot
            self[x][y] = 'X'
            self.guard = (nx, ny)
        else:
            self.turn()

        return True


class Loop(Exception):
    pass


class LoopGrid(GuardGrid):
    def __init__(self, input: str):
        super().__init__(input)

        self.seen = defaultdict(set)

    def move(self):
        x, y = self.guard
        nx, ny = (x + self.dir[0], y + self.dir[1])

        if nx not in self or ny not in self[nx]:
            return False

        if self[nx][ny] in {'.', '^', '>', 'v', '<'}:
            self[nx][ny] = self.carot
            self[x][y] = self.carot
            self.guard = (nx, ny)
            if (nx, ny) in self.seen[(x, y)]:
                raise Loop
            self.seen[(x, y)].add((nx, ny))
        else:
            self.turn()

        return True


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    grid = GuardGrid(input)

    while grid.move():
        pass

    return len(grid.findall('X'))


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    guardgrid = GuardGrid(input)
    start = guardgrid.guard

    while guardgrid.move():
        pass

    loops = 0
    for x, y in guardgrid.findall('X'):
        if (x, y) == start:
            continue

        loopgrid = LoopGrid(input)
        loopgrid[x][y] = 'O'
        try:
            while loopgrid.move():
                pass
        except Loop:
            loops += 1

    return loops


if __name__ == '__main__':
    main(p1, p2, [41], [6])
