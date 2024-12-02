#!/usr/bin/env python

"""https://adventofcode.com/2024/day/2."""

from main import main
from utils import sliding_window


def p1(input):
    lines = input.splitlines()
    count = 0
    for report in lines:
        r = [int(x) for x in report.split()]
        count += int(is_safe(r))

    return count


def is_safe(report):
    decreasing = None
    for a, b in sliding_window(report, 2):
        if a == b:
            return False
        if decreasing is None:
            decreasing = a > b
        if not decreasing and a > b:
            return False
        if decreasing and b > a:
            return False
        if abs(a - b) > 3:
            return False

    return True


def p2(input):
    lines = input.splitlines()
    count = 0
    for report in lines:
        r = [int(x) for x in report.split()]
        if is_safe(r):
            count += 1
        else:
            for i in range(len(r)):
                if is_safe(r[:i] + r[i + 1 :]):
                    count += 1
                    break

    return count


if __name__ == '__main__':
    main(p1, p2, [2], [4])
