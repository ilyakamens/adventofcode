#!/usr/bin/env python

"""https://adventofcode.com/2024/day/16."""

from dataclasses import dataclass

from main import main, runs
from utils import AStarGrid, AStarNode, Dir, Point, Vector, manhattan


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
            if Dir.opposite(node.dir) == d or self[neighbor_pos] == '#':
                continue

            cost = 1
            if d != node.dir:
                cost += 1000

            neighbors.append((ReindeerNode(self, neighbor_pos, d), cost))

        return neighbors


@runs(cases={'1', '2'})
def p1(input: str, case: str) -> int:
    grid = ReindeerGrid(input)
    start = ReindeerNode(grid, grid.find('S'), Dir.E)
    grid.shortest_path(start, grid.find('E'))

    return grid.cost


@runs(cases={'1', '2'})
def p2(input: str, case: str) -> int:
    grid = ReindeerGrid(input)
    start = ReindeerNode(grid, grid.find('S'), Dir.E)
    grid.shortest_path(start, grid.find('E'))

    seen = set()
    froms = {grid.end}
    while froms:
        m = froms.pop()
        seen.add(m.p)
        froms.update(grid.came_from[m])

    return len(seen)


if __name__ == '__main__':
    main(p1, p2, [7036, 11048], [45, 64])
