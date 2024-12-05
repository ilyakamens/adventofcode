#!/usr/bin/env python

"""https://adventofcode.com/2024/day/1."""

from main import main, runs


def parse_input(input):
    l1, l2 = [], []
    for line in input.splitlines():
        l, r = line.split()
        l1.append(int(l))
        l2.append(int(r))
    return l1, l2


@runs(cases={'1'})
def p1(input: str) -> int:
    l1, l2 = parse_input(input)

    l1.sort()
    l2.sort()

    return sum(abs(v2 - v1) for v1, v2 in zip(l1, l2))


@runs(cases={'1'})
def p2(input: str) -> int:
    l1, l2 = parse_input(input)

    return sum(v * l2.count(v) for v in l1)


if __name__ == '__main__':
    main(p1, p2, [11], [31])
