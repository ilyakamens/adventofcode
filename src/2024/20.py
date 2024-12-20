#!/usr/bin/env python

"""https://adventofcode.com/2024/day/20."""

from collections import deque

from main import main
from utils import AStarGrid, AStarNode, Point


class RaceGrid(AStarGrid):
    def get_neighbors(self, node: AStarNode) -> list[tuple[AStarNode, int]]:
        return [n for n in super().neighbor_nodes(node) if self[n.p] != '#']

    def all_within_dist(self, p: Point, max_dist: int) -> list[Point]:
        points = {}
        seen = set()

        queue = deque([(p, 0)])

        while queue:
            point, dist = queue.popleft()
            if point in seen:
                continue

            seen.add(point)
            if dist > max_dist:
                continue
            if self[point] != '#':
                points[point] = dist
            for neighbor, _ in self.neighbors(point):
                queue.append((neighbor, dist + 1))

        return points


def cheat_pairs(grid: RaceGrid, path: set[Point]) -> list[tuple[int, int]]:
    pairs = []
    for i, p in enumerate(path):
        for n1, _ in grid.neighbors(p):
            if grid[n1] == '#':
                for n2, _ in grid.neighbors(n1):
                    if n2 == p or grid[n2] == '#':
                        continue
                    if n2 in path[:i]:
                        continue
                    pairs.append((n1, n2))
    return pairs


def cheats_for_path(path: list[Point], grid: RaceGrid, seconds_saved: int) -> int:
    count = 0
    print('len', len(path))
    for i, p in enumerate(path):
        print(i)
        nodes = grid.all_within_dist(p, 20)
        for node, dist in nodes.items():
            idx = path.index(node)
            if idx - i - dist >= seconds_saved:
                count += 1

    return count


def p1(input: str, seconds_saved: int) -> int:
    grid = RaceGrid(input)

    start_node = AStarNode(grid, grid.find('S'))
    end_pos = grid.find('E')
    end_node = next(grid.shortest_path(start_node, end_pos))

    default_cost = grid.best_total_cost
    path = grid.all_path_points(end_node)

    count = 0

    pairs = cheat_pairs(grid, path)

    for p1, p2 in pairs:
        grid.init()
        old_p1 = grid[p1]
        old_p2 = grid[p2]
        grid[p1] = '1'
        grid[p2] = '2'

        next(grid.shortest_path(start_node, end_pos))
        if default_cost - grid.best_total_cost == seconds_saved:
            count += 1
        grid[p1] = old_p1
        grid[p2] = old_p2

    return count


def p2(input: str, seconds_saved: int) -> int:
    grid = RaceGrid(input)

    start_node = AStarNode(grid, grid.find('S'))
    end_pos = grid.find('E')
    end_node = next(grid.shortest_path(start_node, end_pos))

    path = grid.all_path_points(end_node)

    return cheats_for_path(path, grid, seconds_saved)


if __name__ == '__main__':
    main(p1, p2)
