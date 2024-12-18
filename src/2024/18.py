#!/usr/bin/env python

"""https://adventofcode.com/2024/day/18."""

from main import main, runs
from utils import AStarGrid, AStarNode, binary_search, numbers


class MemoryGrid(AStarGrid):
    def get_neighbors(self, node: AStarNode) -> list[tuple[AStarNode, int]]:
        return [n for n in super().get_neighbors(node) if self[n.p] != '#']


def create_grid(lines: list[str], size: int, stop: int) -> MemoryGrid:
    grid: MemoryGrid = MemoryGrid.from_dimensions(size, size)
    for line in lines[:stop]:
        grid[tuple(numbers(line))] = '#'

    return grid


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    if case == '1':
        size = 7
        stop = 12
    else:
        size = 71
        stop = 1024

    lines = input.splitlines()
    grid: MemoryGrid = create_grid(lines, size, stop)

    start_node = AStarNode(grid, (0, 0))
    end_pos = (size - 1, size - 1)
    next(grid.shortest_path(start_node, end_pos))

    return grid.best_total_cost


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    if case == '1':
        size = 7
    else:
        size = 71

    lines = input.splitlines()

    def shortest_path_exists(i: int) -> bool:
        grid: MemoryGrid = create_grid(lines, size, i)
        start_node = AStarNode(grid, (0, 0))
        end_pos = (size - 1, size - 1)
        return next(grid.shortest_path(start_node, end_pos)) is not None

    return lines[binary_search(shortest_path_exists, 0, len(lines) - 1)]


if __name__ == '__main__':
    main(p1, p2, [22], ['6,1'])
