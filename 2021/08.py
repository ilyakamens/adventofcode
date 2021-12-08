#!/usr/bin/env python

"""https://adventofcode.com/2021/day/08."""

from collections import defaultdict, deque
import os


def p1(lines):
    count = 0

    lens = {2, 3, 4, 7}
    for line in lines:
        l, r = line.split(" | ")
        outputs = r.split()

        for out in outputs:
            if len(out) in lens:
                count += 1

    return count

def p2(lines):
    sum_ = 0

    for line in lines:
        word_map = {}
        num_map = {}

        l, r = line.split(" | ")
        inputs = l.split()
        inputs.sort(key=lambda x: len(x))

        for out in inputs:
            out = "".join(sorted(out))
            if len(out) == 2:
                word_map[out] = 1
                num_map[1] = out
            elif len(out) == 3:
                word_map[out] = 7
                num_map[7] = out
            elif len(out) == 4:
                word_map[out] = 4
                num_map[4] = out
            elif len(out) == 5:
                if all(c in out for c in num_map[1]):
                    n = 3
                elif len(set(out) - set(num_map[4])) == 3:
                    n = 2
                else:
                    n = 5
                word_map[out] = n
                num_map[n] = out
            elif len(out) == 6:
                if not all(c in out for c in num_map[1]):
                    n = 6
                elif not all(c in out for c in num_map[4]):
                    n = 0
                else:
                    n = 9
                word_map[out] = n
                num_map[n] = out

        s = ""
        for out in r.split():
            out = "".join(sorted(out))
            if len(out) == 7:
                s += "8"
            else:
                s += str(word_map[out])
        sum_ += int(s)

    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "08.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
