#!/usr/bin/env python

"""https://adventofcode.com/2021/day/04."""

from collections import defaultdict
import os

def p1(lines):
    boards = []

    y = 0
    for line in lines[1:]:
        if line == "":
            boards.append(defaultdict(int))
            y = 0
            continue

        nums = [int(n) for n in line.split()]
        for x, num in enumerate(nums):
            boards[-1][num] = (x, y)

        y += 1

    winner = None
    matches = [defaultdict(lambda: defaultdict(int)) for _ in boards]
    draws = [int(d) for d in lines[0].split(",")]
    for d in draws:
        if winner:
            break
        for i, b in enumerate(boards):
            if d in b:
                x, y = b[d]
                matches[i]["x"][x] += 1
                matches[i]["y"][y] += 1
                if matches[i]["x"][x] == 5 or matches[i]["y"][y] == 5:
                    winner = b
                    winning_num = d
                    break

    sum_ = sum(n for n in winner.keys())
    for d in draws:
        if d in winner:
            sum_ -= d
        if d == winning_num:
           return sum_ * winning_num

def p2(lines):
    boards = []

    y = 0
    for line in lines[1:]:
        if line == "":
            boards.append(defaultdict(int))
            y = 0
            continue

        nums = [int(n) for n in line.split()]
        for x, num in enumerate(nums):
            boards[-1][num] = (x, y)

        y += 1

    winner = None
    winners = {}
    matches = [defaultdict(lambda: defaultdict(int)) for _ in boards]
    draws = [int(d) for d in lines[0].split(",")]
    for d in draws:
        if winner:
            break
        for i, b in enumerate(boards):
            if d in b:
                x, y = b[d]
                matches[i]["x"][x] += 1
                matches[i]["y"][y] += 1
                if matches[i]["x"][x] == 5 or matches[i]["y"][y] == 5:
                    winners[i] = 1
                    if len(winners) == len(boards):
                        winner = b
                        winning_num = d
                        break

    sum_ = sum(n for n in winner.keys())
    for d in draws:
        if d in winner:
            sum_ -= d
        if d == winning_num:
           return sum_ * winning_num

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "04.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
