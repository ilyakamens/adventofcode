#!/usr/bin/env python

"""https://adventofcode.com/2015/day/10."""

import os


def look_and_say(digits, iterations):
    for _ in range(iterations):
        new_digits = []

        counting = digits[0]
        count = 1
        for d in digits[1:]:
            if d == counting:
                count += 1
                continue

            new_digits.extend([str(count), counting])
            counting = d
            count = 1

        new_digits.extend([str(count), counting])
        digits = "".join(new_digits)

    return digits


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "10.txt")) as f:
        digits = f.read().strip()

    print(f"Part 1: {len(look_and_say(digits, 40))}")

    print(f"Part 2: {len(look_and_say(digits, 50))}")
