#!/usr/bin/env python

"""https://adventofcode.com/2024/day/23."""

from collections import defaultdict
from collections.abc import Iterable
from itertools import combinations

from main import main


def parse(input: str) -> dict:
    connected_to = defaultdict(set)
    for line in input.splitlines():
        a, b = line.split('-')
        connected_to[a].add(b)
        connected_to[b].add(a)

    return connected_to


def connected(computers: Iterable[str], connected_to: dict) -> bool:
    for a, b in combinations(computers, 2):
        if a not in connected_to[b]:
            return False

    return True


def find_groups(start: str, connected_to: dict, size: int) -> list[tuple[str]]:
    groups = []
    for group in combinations(connected_to[start], size):
        if connected(group, connected_to):
            groups.append(tuple(sorted(group + (start,))))

    return groups


def p1(input: str) -> int:
    connected_to = parse(input)

    lans = set()
    for computer in connected_to.keys():
        groups = find_groups(computer, connected_to, 2)
        for group in groups:
            if any(c.startswith('t') for c in group):
                lans.add(group)

    return len(lans)


def p2(input: str) -> int:
    connected_to = parse(input)

    max_size = max(len(v) for v in connected_to.values())
    while True:
        for computer in connected_to.keys():
            groups = find_groups(computer, connected_to, max_size)
            for group in groups:
                return ','.join(group)
        max_size -= 1


if __name__ == '__main__':
    main(p1, p2)
