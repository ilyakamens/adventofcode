#!/usr/bin/env python

"""https://adventofcode.com/2024/day/11."""

from functools import cache

from main import main, runs


@cache
def blink(stone: str, times: int) -> int:
    if times == 0:
        return 1

    if stone == '0':
        return blink('1', times - 1)
    elif len(stone) % 2 == 0:
        middle = len(stone) // 2
        return blink(stone[:middle], times - 1) + blink(str(int(stone[middle:])), times - 1)
    else:
        return blink(str(int(stone) * 2024), times - 1)


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    stones = input.split()

    for i in range(1, 26):
        count = sum(blink(stone, i) for stone in stones)

    return count


@runs(cases=set())
def p2(input: str, case: str) -> int:
    stones = input.split()

    for i in range(1, 76):
        count = sum(blink(stone, i) for stone in stones)

    return count


if __name__ == '__main__':
    main(p1, p2, [55312], [None])
