#!/usr/bin/env python

"""https://adventofcode.com/2024/day/20."""

from collections import deque

from main import main
from utils import AStarGrid, AStarNode, Point


class RaceGrid(AStarGrid):
    def get_neighbors(self, node: AStarNode) -> list[tuple[AStarNode, int]]:
        return [n for n in super().neighbor_nodes(node) if self[n.p] != '#']

    def cheat_ends(self, p: Point, max_dist: int) -> list[Point]:
        points = {}
        seen = set()

        queue = deque([(p, 0)])

        while queue:
            point, dist = queue.popleft()
            if point in seen:
                continue

            seen.add(point)
            if dist > max_dist:
                break
            if self[point] != '#':
                points[point] = dist
            for neighbor, _ in self.neighbors(point):
                queue.append((neighbor, dist + 1))

        return points

    def cheats_for_path(self, path: list[Point], seconds_saved: int, max_dist: int) -> int:
        count = 0

        for i, p in enumerate(path):
            nodes = self.cheat_ends(p, max_dist)
            for node, dist in nodes.items():
                if path.index(node) - i - dist >= seconds_saved:
                    count += 1

        return count


def p1(input: str, seconds_saved: int, max_dist: int) -> int:
    grid = RaceGrid(input)

    start_node = AStarNode(grid, grid.find('S'))
    end_pos = grid.find('E')
    end_node = next(grid.shortest_path(start_node, end_pos))

    path = grid.path(end_node)

    return grid.cheats_for_path(path, seconds_saved, max_dist)


def p2(input: str, seconds_saved: int, max_dist: int) -> int:
    grid = RaceGrid(input)

    start_node = AStarNode(grid, grid.find('S'))
    end_pos = grid.find('E')
    end_node = next(grid.shortest_path(start_node, end_pos))

    path = grid.path(end_node)

    return grid.cheats_for_path(path, seconds_saved, max_dist)


if __name__ == '__main__':
    main(p1, p2)
