#!/usr/bin/env python

"""https://adventofcode.com/2024/day/15."""

from collections import deque

from main import main, runs
from utils import Dir, Grid, Point, paras

DIR_MAP = {
    '>': Dir.E,
    '<': Dir.W,
    '^': Dir.N,
    'v': Dir.S,
}


class FishGrid(Grid):
    def __init__(self, map_: str):
        super().__init__(map_)
        self.robot = self.findall('@')[0]

    def move_to(self, f: Point, t: Point):
        self[t] = self[f]
        self[f] = '.'
        if self[t] == '@':
            self.robot = t

    def move(self, move: str):
        dir = DIR_MAP[move]
        np = self.neighbor(self.robot, dir)
        if self[np] == '#':
            return
        if self[np] == '.':
            self[self.robot] = '.'
            self[np] = '@'
            self.robot = np
            return
        after_box = self.get_after_box(np, dir)
        if self[after_box] == '#':
            return

        opp_dir = self.opposite_dir(dir)
        box = self.neighbor(after_box, opp_dir)
        while self[box] != '@':
            self.move_to(box, self.neighbor(box, dir))
            box = self.neighbor(box, opp_dir)
        self.move_to(box, self.neighbor(box, dir))

    def get_after_box(self, p: Point, dir: Dir) -> Point:
        while self[p] == 'O':
            p = self.neighbor(p, dir)

        return p

    def opposite_dir(self, dir: Dir) -> Dir:
        if dir == Dir.N:
            return Dir.S
        if dir == Dir.E:
            return Dir.W
        if dir == Dir.S:
            return Dir.N
        if dir == Dir.W:
            return Dir.E


@runs(cases={'1', '2'})
def p1(input: str, case: str) -> int:
    map_, moves = paras(input)

    grid = FishGrid(map_)
    moves = moves.replace('\n', '')
    for move in moves:
        grid.move(move)

    coordinates = 0
    for p in grid.findall('O'):
        coordinates += p.x + p.y * 100

    return coordinates


def resize(m: str) -> str:
    rows = []
    for r in m.split('\n'):
        row = ''
        for c in r:
            if c == '.':
                row += '..'
            elif c == '#':
                row += '##'
            elif c == '@':
                row += '@.'
            elif c == 'O':
                row += '[]'
        rows.append(row)

    return '\n'.join(rows)


class LargeFishGrid(FishGrid):
    def move(self, move: str):
        dir = DIR_MAP[move]
        np = self.neighbor(self.robot, dir)
        if self[np] == '#':
            return
        if self[np] == '.':
            self[self.robot] = '.'
            self[np] = '@'
            self.robot = np
            return

        if move in {'<', '>'}:
            after_box = self.get_after_box(np, dir)
            if self[after_box] == '#':
                return

            opp_dir = self.opposite_dir(dir)
            box = self.neighbor(after_box, opp_dir)
            while self[box] != '@':
                self.move_to(box, self.neighbor(box, dir))
                box = self.neighbor(box, opp_dir)
            self.move_to(box, self.neighbor(box, dir))
            return

        box = {np}
        nc = self[np]
        box.add(self.neighbor(np, Dir.E if nc == '[' else Dir.W))
        after_box = self.get_after_box_ns(box, dir)

        if after_box == '#':
            return

        self.move_box_row_ns(box, dir)
        self.move_to(self.robot, np)

    def move_box_row_ns(self, box: set[Point], dir: Dir):
        for p in box:
            n = self.neighbor(p, dir)
            if self[n] == '#':
                return
            if self[n] == '.':
                self.move_to(p, n)
                continue
            if self[n] == '[':
                self.move_box_row_ns({n, self.neighbor(n, Dir.E)}, dir)
            elif self[n] == ']':
                self.move_box_row_ns({n, self.neighbor(n, Dir.W)}, dir)
            self.move_to(p, n)

    def get_after_box_ns(self, boxes: set[Point], dir: Dir) -> Point:
        queue = deque(boxes)
        while queue:
            b = queue.popleft()
            n = self.neighbor(b, dir)
            if self[n] == '#':
                return '#'
            if self[n] == '.':
                continue
            if self[n] == '[':
                queue.append(n)
                queue.append(self.neighbor(n, Dir.E))
            elif self[n] == ']':
                queue.append(n)
                queue.append(self.neighbor(n, Dir.W))
            else:
                raise ValueError(f'Unexpected character: {self[n]}')

        return '.'

    def get_after_box(self, p: Point, dir: Dir) -> Point:
        while self[p] in {'[', ']'}:
            p = self.neighbor(p, dir)

        return p


@runs(cases={'2'})
def p2(input: str, case: str) -> int:
    map_, moves = paras(input)
    map_ = resize(map_)
    grid = LargeFishGrid(map_)
    moves = moves.replace('\n', '')
    for move in moves:
        grid.move(move)

    coordinates = 0
    for p in grid.findall('['):
        coordinates += p.x + p.y * 100

    return coordinates


if __name__ == '__main__':
    main(p1, p2, [2028, 10092], [None, 9021])
