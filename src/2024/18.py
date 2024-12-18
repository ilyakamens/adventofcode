#!/usr/bin/env python

"""https://adventofcode.com/2024/day/18."""

from collections import defaultdict
from dataclasses import dataclass

from main import main, runs
from utils import AStarGrid, AStarNode, Dir, Point, Vector, manhattan, numbers


@dataclass
class ReindeerNode(AStarNode):
    dir: Vector

    def __hash__(self):
        return hash((self.p, self.dir))

    def __eq__(self, other: 'ReindeerNode'):
        return self.p == other.p and self.dir == other.dir


class ReindeerGrid(AStarGrid):
    def heuristic(self, start_pos: Point, end_pos: Point) -> int:
        return manhattan(start_pos, end_pos)

    def get_neighbors(self, node: ReindeerNode) -> list[tuple[ReindeerNode, int]]:
        neighbors: list[tuple[ReindeerNode, int]] = []

        for d in Dir:
            neighbor_pos = self.neighbor(node.p, d)
            if Dir.opposite(node.dir) == d or neighbor_pos not in self or self[neighbor_pos] == '#':
                continue

            neighbors.append((ReindeerNode(self, neighbor_pos, d), 1))

        return neighbors


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    if case == '1':
        width, height = 7, 7
    else:
        width, height = 71, 71

    grid: ReindeerGrid = ReindeerGrid.from_dimensions(width, height)
    for i, line in enumerate(input.splitlines()):
        if case == '1' and i == 12:
            break
        if case == 'real' and i == 1024:
            break
        grid[tuple(numbers(line))] = '#'

    next(grid.shortest_path(ReindeerNode(grid, (0, 0), Dir.E), (width - 1, height - 1)))

    return grid.best_total_cost


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    if case == '1':
        width, height = 7, 7
    else:
        width, height = 71, 71

    grid: ReindeerGrid = ReindeerGrid.from_dimensions(width, height)
    input_lines = input.splitlines()
    for i, line in enumerate(input_lines):
        if case == '1' and i == 12:
            break
        if case == 'real' and i == 2024:
            break
        grid[tuple(numbers(line))] = '#'

    next(grid.shortest_path(ReindeerNode(grid, (0, 0), Dir.E), (width - 1, height - 1)))

    # if case == 'real':
    #     i = 3000
    while grid.best_total_cost != float('inf'):
        print(i)
        grid.total_costs = defaultdict(lambda: float('inf'))
        grid.came_from = defaultdict(set)
        grid.best_total_cost = float('inf')
        grid[tuple(numbers(input_lines[i]))] = '#'
        try:
            next(grid.shortest_path(ReindeerNode(grid, (0, 0), Dir.E), (width - 1, height - 1)))
        except StopIteration:
            break
        i += 1

    return input_lines[i]


if __name__ == '__main__':
    main(p1, p2, [22], ['6,1'])
