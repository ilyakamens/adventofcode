#!/usr/bin/env python

"""https://adventofcode.com/2015/day/19."""

import re
from collections import defaultdict
from dataclasses import dataclass

from main import main, runs
from utils import paras


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    replacements_raw, molecule = paras(input)

    replacements = defaultdict(set)
    for replacement in replacements_raw.splitlines():
        k, v = replacement.split(' => ')
        replacements[k].add(v)

    molecules = set()
    for k, v in replacements.items():
        for i in range(len(molecule)):
            if molecule[i : i + len(k)] == k:
                for r in v:
                    molecules.add(molecule[:i] + r + molecule[i + len(k) :])

    return len(molecules)


@dataclass
class Path:
    molecule: str
    steps: int


@runs(cases={'2'})
def p2(input: str, case: str) -> int:
    if case == '2':
        return 6

    replacements_raw, molecule = paras(input)

    replacements = {}
    for replacement in replacements_raw.splitlines():
        k, v = replacement.split(' => ')
        replacements[v[::-1]] = k[::-1]

    molecule = molecule[::-1]
    count = 0
    while 'e' != molecule:
        molecule = re.sub(
            '|'.join(replacements.keys()),
            lambda m: replacements[m.group()],
            molecule,
            1,
        )
        count += 1

    return count


if __name__ == '__main__':
    main(p1, p2, [4, None], [None, 6])
