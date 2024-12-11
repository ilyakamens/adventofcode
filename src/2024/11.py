#!/usr/bin/env python

"""https://adventofcode.com/2024/day/11."""

from collections import defaultdict

from main import main, runs


def blink(stones: list[str]) -> int:
    new_stones = []
    for stone in stones:
        if stone == '0':
            new_stones.append('1')
        elif len(stone) % 2 == 0:
            middle = len(stone) // 2
            new_stones.append(stone[:middle])
            new_stones.append(str(int(stone[middle:])))
        else:
            new_stones.append(str(int(stone) * 2024))

    return new_stones


CACHE = {}


def transform(stone: str, times: int) -> int:
    if times == 0:
        return 1

    if (stone, times) in CACHE:
        return CACHE[(stone, times)]

    if stone == '0':
        r = transform('1', times - 1)
    elif len(stone) % 2 == 0:
        middle = len(stone) // 2
        r = transform(stone[:middle], times - 1) + transform(str(int(stone[middle:])), times - 1)
    else:
        r = transform(str(int(stone) * 2024), times - 1)

    CACHE[(stone, times)] = r
    return r


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    stones = input.split()

    for _ in range(25):
        stones = blink(stones)

    return len(stones)


cache = defaultdict(lambda: defaultdict(int))


@runs(cases=set())
def p2(input: str, case: str) -> int:
    stones = input.split()

    for i in range(1, 76):
        count = sum(transform(stone, i) for stone in stones)

    return count


if __name__ == '__main__':
    main(p1, p2, [55312], [None])
