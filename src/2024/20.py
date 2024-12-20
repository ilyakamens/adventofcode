#!/usr/bin/env python

"""https://adventofcode.com/2024/day/20."""

from main import main
from utils import AStarGrid, AStarNode, Point, manhattan


class RaceGrid(AStarGrid):
    def get_neighbors(self, node: AStarNode) -> list[tuple[AStarNode, int]]:
        return [n for n in super().neighbor_nodes(node) if self[n.p] != '#']

    def num_cheats(self, path: list[Point], seconds_saved: int, max_dist: int) -> int:
        count = 0

        for i, s in enumerate(path):
            for j, e in enumerate(path[i + 1 :], start=1):
                dist = manhattan(s, e)
                if dist > max_dist:
                    continue
                if j - dist >= seconds_saved:
                    count += 1

        return count


def count_cheats(input: str, seconds_saved: int, max_dist: int) -> int:
    grid = RaceGrid(input)
    end_node = next(grid.shortest_path(AStarNode(grid, grid.find('S')), grid.find('E')))

    return grid.num_cheats(grid.path(end_node), seconds_saved, max_dist)


def p1(input: str, seconds_saved: int, max_dist: int) -> int:
    return count_cheats(input, seconds_saved, max_dist)


def p2(input: str, seconds_saved: int, max_dist: int) -> int:
    return count_cheats(input, seconds_saved, max_dist)


if __name__ == '__main__':
    main(p1, p2)
