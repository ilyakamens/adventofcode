from collections.abc import Callable
import os
import sys

import aocd


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def _format_result(result, expected):
    return (
        f"{bcolors.OKGREEN}{result}{bcolors.ENDC}"
        if result == expected
        else f"{bcolors.WARNING}{result}{bcolors.ENDC}"
        if expected is None
        else f"{bcolors.FAIL}{result}{bcolors.ENDC} != {bcolors.OKGREEN}{expected}{bcolors.ENDC}"
    )


def main(p1: Callable[[str], int], p2: Callable[[str], int], p1_theirs: int, p2_theirs: int):
    year, day, path = sys.argv[1:]

    i = 1
    while True:
        example_path = path + f"/example-{i}.txt"
        if not os.path.exists(example_path):
            break
        with open(example_path) as f:
            lines = [list(l) for l in f.read().splitlines()]
        i += 1

    p1_mine = p1(lines)
    p2_mine = p2(lines)

    print("Examples:")
    print(f"Part a: {_format_result(p1_mine, p1_theirs)}")
    print(f"Part b: {_format_result(p2_mine, p2_theirs)}")
    print()

    with open(path + "/input.txt") as f:
        lines = [list(l) for l in f.read().splitlines()]

    print("Real:")
    if p1_theirs == p1_mine:
        aocd.submit(p1(lines), part="a", day=int(day), year=int(year))
    if p2_theirs == p2_mine:
        aocd.submit(p2(lines), part="b", day=int(day), year=int(year))
