#!/usr/bin/env python

"""https://adventofcode.com/2015/day/16."""

import re
from dataclasses import dataclass
from typing import Annotated

from main import main, runs

run_type = Annotated[str, '1, 2, 3, etc., or real']

SUE_STR = 'Sue 0: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1'  # noqa


@dataclass
class Sue:
    name: str
    children: int | None = None
    cats: int | None = None
    samoyeds: int | None = None
    pomeranians: int | None = None
    akitas: int | None = None
    vizslas: int | None = None
    goldfish: int | None = None
    trees: int | None = None
    cars: int | None = None
    perfumes: int | None = None

    def __eq__(self, other: 'Sue') -> bool:
        for k, v in self.__dict__.items():
            if k == 'name' or v is None:
                continue
            if v != other.__dict__[k]:
                return False

        return True


class Sue2(Sue):
    def __eq__(self, other: 'Sue') -> bool:
        for k, v in self.__dict__.items():
            if k == 'name' or v is None:
                continue
            if k in {'cats', 'trees'}:
                if v <= other.__dict__[k]:
                    return False
            elif k in {'pomeranians', 'goldfish'}:
                if v >= other.__dict__[k]:
                    return False
            elif v != other.__dict__[k]:
                return False

        return True


def parse_sue(line: str, cls: type[Sue]) -> Sue:
    match = re.match(r'Sue (\d+): ', line)
    name = int(match.group(1))
    rest = line.replace(match.group(), '')

    return cls(name, **{k: int(v) for k, v in (item.split(': ') for item in rest.split(', '))})


SUE = parse_sue(SUE_STR, Sue)


@runs(cases={'real'})
def p1(run: run_type, input: str) -> int:
    sues: list[Sue] = []
    for line in input.splitlines():
        sues.append(parse_sue(line, Sue))

    for sue in sues:
        if sue == SUE:
            return sue.name


@runs(cases={'real'})
def p2(run: run_type, input: str) -> int:
    sues: list[Sue] = []
    for line in input.splitlines():
        sues.append(parse_sue(line, Sue2))

    for sue in sues:
        if sue == SUE:
            return sue.name


if __name__ == '__main__':
    main(p1, p2, [None], [None])
