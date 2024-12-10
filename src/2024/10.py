#!/usr/bin/env python

"""https://adventofcode.com/2024/day/10."""

from collections import deque

from main import main, runs
from utils import Dir, Grid


class Map(Grid):
    def walk(self, start: tuple[int, int], allow_dupes: bool = False) -> int:
        count = 0

        q = deque([start])
        seen = set()
        while len(q):
            cx, cy = q.popleft()

            elevation = int(self[cx][cy])
            if elevation == 9:
                if allow_dupes:
                    count += 1
                elif (cx, cy) not in seen:
                    count += 1
                    seen.add((cx, cy))
                continue

            for nx, ny in self.neighbors(cx, cy, dir=Dir):
                try:
                    neighbor = int(self[nx][ny])
                except ValueError:
                    continue
                if neighbor == elevation + 1:
                    q.append((nx, ny))

        return count


@runs(cases={'1', '2', '3'})
def p1(input: str, case: str) -> int:
    grid = Map(input)
    starts = grid.findall('0')

    counts = 0
    for start in starts:
        counts += grid.walk(start)

    return counts


@runs(cases={'4', '5', '6'})
def p2(input: str, case: str) -> int:
    grid = Map(input)
    starts = grid.findall('0')

    counts = 0
    for start in starts:
        counts += grid.walk(start, allow_dupes=True)

    return counts


if __name__ == '__main__':
    main(p1, p2, [1, 2, 4, None, None, None], [None, None, None, 3, 13, 81])
