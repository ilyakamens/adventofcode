#!/usr/bin/env python

"""https://adventofcode.com/2024/day/2."""

from main import main
from utils import numbers, sliding_window


def p1(input):
    lines = input.splitlines()
    count = 0
    for report in lines:
        count += int(is_safe(numbers(report)))

    return count


def is_safe(report):
    decreasing = report[0] > report[1]
    for a, b in sliding_window(report, 2):
        if decreasing and not a > b:
            return False
        if not decreasing and not b > a:
            return False
        if abs(a - b) > 3:
            return False

    return True


def p2(input):
    lines = input.splitlines()
    count = 0
    for report in lines:
        r = numbers(report)
        for i in range(len(r)):
            if is_safe(r[:i] + r[i + 1 :]):
                count += 1
                break

    return count


if __name__ == '__main__':
    main(p1, p2, [2], [4])
