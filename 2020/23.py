#!/usr/bin/env python

"""https://adventofcode.com/2020/day/23."""


import os


class Cup:
    def __init__(self, val):
        self.val = val
        self.r = None

    def __repr__(self):
        return f"{self.val} {self.r.val}"


class Crab:
    def __init__(self, cups):
        self.len = len(cups)
        self.cup_map = {}
        for cup in cups:
            self.cup_map[cup] = Cup(cup)
        for i, cup in enumerate(cups):
            self.cup_map[cup].r = self.cup_map[cups[(i + 1) % self.len]]
        self.current = self.cup_map[cups[0]]

    def move(self):
        # Remove
        removed = [self.current.r, self.current.r.r, self.current.r.r.r]
        removed_vals = {self.current.r.val, self.current.r.r.val, self.current.r.r.r.val}
        self.current.r = removed[-1].r

        # Choose destination
        dest = self.current.val - 1
        while dest <= 0 or dest in removed_vals:
            dest = self.len if dest <= 0 else dest - 1
        dest = self.cup_map[dest]

        # Reinsert
        removed[-1].r = dest.r
        dest.r = removed[0]

        # Update current
        self.current = self.current.r

    def part_one(self):
        cups = []
        cur = self.cup_map[1].r
        while cur.val != 1:
            cups.append(str(cur.val))
            cur = cur.r

        return "".join(cups)

    def part_two(self):
        one = self.cup_map[1]
        return one.r.val * one.r.r.val

    def __str__(self):
        cups = [f"({self.current.val})"]
        cup = self.current.r
        while cup != self.current:
            cups.append(str(cup.val))
            cup = cup.r

        return " ".join(cups)


if __name__ == "__main__":
    with open(os.path.join("input", "23.txt")) as f:
        cups = [int(c) for c in f.read().strip()]

    crab = Crab(cups)
    for i in range(10):
        crab.move()

    print(f"Part 1: {crab.part_one()}")

    crab = Crab(cups + [i for i in range(1_000_001) if i > len(cups)])
    for i in range(10_000_000):
        crab.move()

    print(f"Part 2: {crab.part_two()}")
