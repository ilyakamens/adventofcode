#!/usr/bin/env python

"""https://adventofcode.com/2024/day/16."""

from dataclasses import dataclass

from main import main
from utils import AStarGrid, AStarNode, Dir, Vector


@dataclass
class ReindeerNode(AStarNode):
    dir: Vector

    def __hash__(self):
        return hash((self.p, self.dir))

    def __eq__(self, other: 'ReindeerNode'):
        return self.p == other.p and self.dir == other.dir


class ReindeerGrid(AStarGrid):
    def cost(self, f: ReindeerNode, t: ReindeerNode) -> int:
        return 1 if f.dir == t.dir else 1001

    def get_neighbors(self, node: ReindeerNode) -> list[tuple[ReindeerNode, int]]:
        neighbors: list[tuple[ReindeerNode, int]] = []
        for d in self.dir:
            neighbor_pos = self.neighbor(node.p, d)
            if Dir.opposite(node.dir) == d or self[neighbor_pos] == '#':
                continue

            neighbors.append(ReindeerNode(self, neighbor_pos, d))

        return neighbors


def p1(input: str) -> int:
    grid = ReindeerGrid(input)
    start = ReindeerNode(grid, grid.find('S'), Dir.E)
    next(grid.shortest_path(start, grid.find('E')))

    return grid.best_total_cost


def p2(input: str) -> int:
    grid = ReindeerGrid(input)
    start = ReindeerNode(grid, grid.find('S'), Dir.E)

    seen = set()
    for end in grid.shortest_paths(start, grid.find('E')):
        seen.update(grid.all_path_points(end))

    return len(seen)


if __name__ == '__main__':
    main(p1, p2)
