#!/usr/bin/env python

"""https://adventofcode.com/2024/day/3."""

import re

from main import main

pattern = r'mul\((\d+),(\d+)\)'


def p1(input):
    sums = 0
    matches = re.finditer(pattern, input)
    for match in matches:
        l, r = match.group().split(',')
        sums += int(l.replace('mul(', '')) * int(r.replace(')', ''))

    return sums


def p2(input):
    sums = 0
    do = True
    i = 1
    while i < len(input):
        if input[i - 4 : i] == 'do()':
            print('do', i)
            do = True
        elif input[i - 7 : i] == "don't()":
            print('dont', i)
            do = False
        if not do:
            i += 1
            continue

        if input[i - 4 : i] == 'mul(':
            print('mul', i, input[i - 4 : i + 9])
            matches = re.finditer(pattern, input[i - 4 : i + 9])
            for match in matches:
                l, r = match.group().split(',')
                sums += int(l.replace('mul(', '')) * int(r.replace(')', ''))
                i += match.end() - 5
                break

        i += 1

    return sums


if __name__ == '__main__':
    main(p1, p2, [161], [161])
