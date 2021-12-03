#!/usr/bin/env python

"""https://adventofcode.com/2021/day/03."""

import os

def part_1(lines):
    e, g = "", ""
    for i in range(len(lines[0])):
        one_count, zero_count = 0, 0
        for line in lines:
            if line[i] == "1":
                one_count += 1
            else:
                zero_count += 1

        if one_count > zero_count:
            e += "1"
            g += "0"
        else:
            e += "0"
            g += "1"

    return int(e, 2) * int(g, 2)

def oxy(lines, i=0):
    if len(lines) == 1:
        return int(lines[0], 2)

    one_count, zero_count = 0, 0
    ones = []
    zeros = []
    for line in lines:
        if line[i] == "1":
            one_count += 1
            ones.append(line)
        else:
            zero_count += 1
            zeros.append(line)

    if one_count > zero_count:
        keep = ones
    elif zero_count > one_count:
        keep = zeros
    else:
        keep = ones

    return oxy(keep, i+1)

def co2(lines, i=0):
    if len(lines) == 1:
        return int(lines[0], 2)

    one_count, zero_count = 0, 0
    ones = []
    zeros = []
    for line in lines:
        if line[i] == "1":
            one_count += 1
            ones.append(line)
        else:
            zero_count += 1
            zeros.append(line)

    if one_count > zero_count:
        keep = zeros
    elif zero_count > one_count:
        keep = ones
    else:
        keep = zeros

    return co2(keep, i+1)

def part_2(lines):
    oxy_ = oxy(lines)
    co2_ = co2(lines)

    return oxy_ * co2_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "03.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {part_1(lines)}")

    print(f"Part 2: {part_2(lines)}")
