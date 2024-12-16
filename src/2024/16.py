#!/usr/bin/env python

"""https://adventofcode.com/2024/day/16."""

import heapq
from collections import defaultdict
from dataclasses import dataclass

from main import main, runs
from utils import Dir, Grid, Point, manhattan


@dataclass
class Move:
    p: Point
    dir: Dir
    total_cost: int = float('inf')

    def __hash__(self):
        return hash((self.p, self.dir))

    def __lt__(self, other: 'Move'):
        return self.total_cost < other.total_cost

    def __eq__(self, other: 'Move'):
        return self.p == other.p and self.dir == other.dir


class MazeGrid(Grid):
    def is_opposite_dir(self, d1: Dir, d2: Dir) -> bool:
        return {Dir.N: Dir.S, Dir.S: Dir.N, Dir.E: Dir.W, Dir.W: Dir.E}[d1] == d2

    def navigate(self, all=False):
        end_pos = self.findall('E')[0]
        start_pos = self.findall('S')[0]

        heap: list[Move] = []
        start = Move(start_pos, Dir.E, total_cost=manhattan(start_pos, end_pos))
        heapq.heappush(heap, start)

        came_from = defaultdict(set)
        partial_costs = defaultdict(lambda: float('inf'))
        partial_costs[start] = 0

        total_costs = defaultdict(lambda: float('inf'))
        total_costs[start] = manhattan(start_pos, end_pos)

        while heap:
            m = heapq.heappop(heap)

            if m.p == end_pos:
                self.end = m
                self.end_cost = total_costs[m]
                self.came_from = came_from
                return

            for d in Dir.iter():
                if self.is_opposite_dir(m.dir, d):
                    continue
                n = self.neighbor(m.p, d)
                if self[n] == '#':
                    continue

                cost = 1
                if d != m.dir:
                    cost += 1000

                move = Move(n, d)
                partial_cost = partial_costs[m] + cost
                if partial_cost <= partial_costs[move]:
                    came_from[move].add(m)
                    partial_costs[move] = partial_cost
                    total_costs[move] = partial_cost + manhattan(n, end_pos)
                    move.total_cost = total_costs[move]
                    if move not in heap:
                        heapq.heappush(heap, move)


@runs(cases={'1', '2'})
def p1(input: str, case: str) -> int:
    grid = MazeGrid(input)
    grid.navigate()

    return grid.end_cost


@runs(cases={'1', '2'})
def p2(input: str, case: str) -> int:
    grid = MazeGrid(input)
    grid.navigate()

    seen = set()
    froms = {grid.end}
    while froms:
        m = froms.pop()
        seen.add(m.p)
        froms.update(grid.came_from[m])

    return len(seen)


if __name__ == '__main__':
    main(p1, p2, [7036, 11048], [45, 64])
