#!/usr/bin/env python

"""https://adventofcode.com/2024/day/4."""

from typing import Annotated

from main import main
from utils import Dir8, DirDiag, Grid

run_type = Annotated[str, '1, 2, 3, etc., or real']


def p1(run: run_type, input: str) -> int:
    g = Grid(input)

    count = 0
    for x, y in g.iter():
        for dir in Dir8.iter():
            if g.substr(x, y, dir, 4) == 'XMAS':
                count += 1

    return count


def p2(run: run_type, input: str) -> int:
    g = Grid(input)

    count = 0
    for x, y in g.iter():
        if all(
            g.substr(x, y, dir, 3, offset=-1) in {'MAS', 'SAM'} for dir in [DirDiag.NE, DirDiag.SE]
        ):
            count += 1

    return count


if __name__ == '__main__':
    main(p1, p2, [18], [9])
