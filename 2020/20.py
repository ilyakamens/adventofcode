#!/usr/bin/env python

"""https://adventofcode.com/2020/day/20."""

from collections import deque
from functools import reduce
import os
import re


class Tile:
    def __init__(self, num, lines):
        self.num = num
        self.lines = [list(l) for l in lines]
        self.neighbor_set = set()
        self.neighbors = [None] * 4

    @property
    def borders(self):
        return [
            "".join(self.lines[0]),
            "".join([line[-1] for line in self.lines]),
            "".join(self.lines[-1]),
            "".join([line[0] for line in self.lines]),
        ]

    @property
    def borderless(self):
        return [line[1:-1] for line in self.lines[1:-1]]

    def rotate(self):
        lines = []
        for col, _ in enumerate(self.lines):
            lines.append([row[col] for row in reversed(self.lines)])
        self.lines = lines

    def flip(self):
        self.lines = list(reversed(self.lines))

    def __str__(self):
        return "\n".join(["".join(l) for l in self.lines])


def iter_orient(t):
    """Yield all orientations of tile t."""
    for _ in range(2):
        yield t
        for _ in range(3):
            t.rotate()
            yield t
        t.flip()


def iter_borders(t1, t2):
    for b1 in t1.borders:
        for b2 in t2.borders:
            yield b1, b2


def orient(t, n):
    """Orient tile n around tile t."""
    for nr in iter_orient(n):
        for i, b in enumerate(t.borders):
            j = (i + 2) % 4
            if b == nr.borders[j]:
                t.neighbors[i] = nr
                nr.neighbors[j] = t
                return
    raise Exception("Unable to orient neighbor.")


def has_monster(area):
    regexes = (
        ".{18}#.",
        "#.{4}##.{4}##.{4}###",
        ".#..#..#..#..#..#...",
    )
    return all(re.match(regex, "".join(line)) is not None for line, regex in zip(area, regexes))


if __name__ == "__main__":
    with open(os.path.join("input", "20.txt")) as f:
        tile_blocks = [block.strip().split("\n") for block in f.read().split("\n\n")]

    # Create tiles.
    tiles = []
    for tile in tile_blocks:
        num = int(re.match("^Tile (?P<num>[0-9]+):$", tile[0]).group("num"))
        tiles.append(Tile(num, tile[1:]))

    # Add neighbors.
    for i, t1 in enumerate(tiles):
        for t2 in tiles[i + 1 :]:
            for b1, b2 in iter_borders(t1, t2):
                if b2 in {b1, b1[::-1]}:
                    t1.neighbor_set.add(t2)
                    t2.neighbor_set.add(t1)
                    break

    # Orient tiles.
    visited = set()
    queue = deque([tiles[0]])
    while len(queue):
        tile = queue.popleft()
        if tile in visited:
            continue
        visited.add(tile)
        for n in tile.neighbor_set:
            orient(tile, n)
            queue.append(n)

    corners = [t for t in tiles if len([n for n in t.neighbors if n]) == 2]
    print(f"Part 1: {reduce(lambda a, c: c.num * a, corners, 1)}")

    # Starting with top-left tile, get all the tiles in the first column.
    tile = next(c for c in corners if not (c.neighbors[0] or c.neighbors[-1]))
    left_side_tiles = []
    while tile:
        left_side_tiles.append(tile)
        tile = tile.neighbors[2]

    # Combine tiles horizontally into a series of rows.
    rows = []
    for tile in left_side_tiles:
        combined = tile.borderless
        tile = tile.neighbors[1]
        while tile:
            combined = [l + r for l, r in zip(combined, tile.borderless)]
            tile = tile.neighbors[1]
        for row in combined:
            rows.append(row)

    # Big tile!
    sea = Tile("sea", rows)

    # Count monsters.
    num_monsters = 0
    for sea in iter_orient(sea):
        for row, line in enumerate(sea.lines[:-2]):
            for col, _ in enumerate(line[:-19]):
                if has_monster([line[col : col + 20] for line in sea.lines[row : row + 3]]):
                    num_monsters += 1
        if num_monsters > 0:
            break

    monster_size = 15
    pound_count = str(sea).count("#") - (num_monsters * monster_size)
    print(f"Part 2: {pound_count}")
