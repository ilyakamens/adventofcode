#!/usr/bin/env python

"""https://adventofcode.com/2015/day/18."""

from main import main, runs
from utils import Grid


class LightGrid(Grid):
    def is_on(self, x: int, y: int) -> bool:
        return self[x][y] == '#'

    def step(self, x: int, y: int) -> bool:
        neighbors = self.neighbors(x, y)
        on_count = sum(self.is_on(nx, ny) for nx, ny in neighbors)

        if self.is_on(x, y):
            return '#' if on_count in (2, 3) else '.'
        else:
            return '#' if on_count == 3 else '.'


class StuckGrid(LightGrid):
    def step(self, x: int, y: int) -> str:
        if (x, y) in self.corners():
            return '#'

        return super().step(x, y)


def run_steps(grid: LightGrid, steps: int, cls: type[LightGrid]) -> LightGrid:
    for _ in range(steps):
        new_grid = cls('')
        for x, y in grid.iter():
            new_grid[x][y] = grid.step(x, y)
        grid = new_grid

    return grid


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    steps = {'1': 4, 'real': 100}[case]
    grid = LightGrid(input)
    grid = run_steps(grid, steps, LightGrid)

    return sum(grid.is_on(x, y) for x, y in grid.iter())


@runs(cases={'2'})
def p2(input: str, case: str) -> int:
    steps = {'2': 5, 'real': 100}[case]
    grid = StuckGrid(input)
    grid = run_steps(grid, steps, StuckGrid)

    return sum(grid.is_on(x, y) for x, y in grid.iter())


if __name__ == '__main__':
    main(p1, p2, [4, None], [None, 17])
