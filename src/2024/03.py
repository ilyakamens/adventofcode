#!/usr/bin/env python

"""https://adventofcode.com/2024/day/3."""

import re

from main import main

mul_re = r'mul\((\d{1,3}),(\d{1,3})\)'


def p1(input):
    sums = 0
    for match in re.findall(mul_re, input):
        sums += int(match[0]) * int(match[1])

    return sums


def p2(input):
    sums = 0
    do = True
    i = 0
    do_re = re.compile(r'do\(\)')
    dont_re = re.compile(r"don't\(\)")

    while i < len(input):
        if do_re.match(input[i : i + 4]):
            i += 4
            do = True
            continue
        if dont_re.match(input[i : i + 7]):
            i += 7
            do = False
            continue
        if not do:
            do_i = input[i:].find('do()')
            if do_i == -1:
                break
            i += do_i
            continue

        match = re.match(mul_re, input[i : i + 12])
        if match:
            sums += int(match.group(1)) * int(match.group(2))
            i += match.end()
            continue

        i += 1

    return sums


if __name__ == '__main__':
    main(p1, p2, [161, 161], [161, 48])
