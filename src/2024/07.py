#!/usr/bin/env python

"""https://adventofcode.com/2024/day/7."""

from itertools import product

from main import main, runs
from utils import numbers


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    vals = []
    for line in input.splitlines():
        res, *rest = numbers(line)
        opss = product('*+', repeat=len(rest) - 1)
        for ops in opss:
            ops = list(ops)
            nums = list(rest.copy())
            total = nums.pop(0)
            while nums:
                op = ops.pop(0)
                num = nums.pop(0)
                total = eval(f'{total}{op}{num}')
            if total == int(res):
                vals.append(res)
                break

    return sum(vals)


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    vals = []
    for line in input.splitlines():
        print(line)
        res, *rest = numbers(line)
        opss = product('*+|', repeat=len(rest) - 1)
        for ops in opss:
            ops = list(ops)
            nums = list(rest.copy())
            total = nums.pop(0)
            while nums:
                op = ops.pop(0)
                num = nums.pop(0)
                if op == '|':
                    total = int(str(total) + str(num))
                else:
                    total = eval(f'{total}{op}{num}')
                if total > res:
                    break
            if total == res:
                vals.append(res)
                break

    return sum(vals)


if __name__ == '__main__':
    main(p1, p2, [3749], [11387])
