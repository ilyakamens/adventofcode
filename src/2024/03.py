#!/usr/bin/env python

"""https://adventofcode.com/2024/day/3.

Cleaned-up solution inspired by zakj's.
"""

import re

from main import main

mul_re = r'mul\((\d{1,3}),(\d{1,3})\)'


def p1(input):
    matches = re.findall(mul_re, input)

    return sum(int(m[0]) * int(m[1]) for m in matches)


def p2(input):
    all_re = r'|'.join([mul_re, r'do\(\)', r"don't\(\)"])
    matches = [m for m in re.finditer(all_re, input)]

    total = 0
    enabled = True
    for m in matches:
        if m.group() == 'do()':
            enabled = True
        elif m.group() == "don't()":
            enabled = False
        elif enabled:
            total += int(m.group(1)) * int(m.group(2))

    return total


if __name__ == '__main__':
    main(p1, p2, [161, 161], [161, 48])
