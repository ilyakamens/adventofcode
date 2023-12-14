#!/usr/bin/env python

"""https://adventofcode.com/2023/day/05."""

from dataclasses import dataclass, field
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


def chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i : i + size]


@dataclass
class Range:
    group: "Group"
    src: int
    dest: int
    inc: int

    @property
    def ss(self):
        return self.src

    @property
    def se(self):
        return self.src + self.inc - 1

    @property
    def ds(self):
        return self.dest

    @property
    def de(self):
        return self.dest + self.inc - 1

    @property
    def index(self):
        return self.group.ranges.index(self)

    def isbefore(self, range: "Range"):
        return self.de < range.ss

    def isafter(self, range: "Range"):
        return self.ds > range.se

    def overlapsleft(self, range: "Range"):
        return self.ds < range.ss

    def overlapsright(self, range: "Range"):
        return self.de > range.se

    def issubrange(self, range: "Range"):
        return self.ds >= range.ss and self.de <= range.se

    def addleft(self, start, end):
        self.group.ranges.insert(self.index, Range(self.group, start, start, end - start))

    def addright(self, start, end):
        self.group.ranges.append(Range(self.group, start, start, (end - start) + 1))

    def splitleft(self, newde):
        r = Range(self.group, self.ss, self.ds, newde - self.ds)
        self.src = r.se + 1
        self.dest = r.de + 1
        self.inc = self.inc - r.inc
        self.group.ranges.insert(self.index, r)

    def __repr__(self):
        return f"{self.ss} -> {self.se}\n{self.ds} -> {self.de}"


@dataclass
class Group:
    ranges: list[Range] = field(default_factory=list)

    def __repr__(self):
        src = []
        dest = []
        for r in self.ranges:
            src.append(f"{r.ss:02} -> {r.se:02}")
            dest.append(f"{r.ds:02} -> {r.de:02}")

        return f"{', '.join(src)}\n{', '.join(dest)}"

    @property
    def pbs(self):
        self.ranges = self.ranges_by_src
        return self

    @property
    def pbd(self):
        self.ranges = self.ranges_by_dest
        return self

    @property
    def ranges_by_src(self) -> list[Range]:
        return sorted(self.ranges, key=lambda r: r.src)

    @property
    def ranges_by_dest(self) -> list[Range]:
        return sorted(self.ranges, key=lambda r: r.dest)

    def match_groups(self, other: "Group"):
        changed = False

        my_ranges_by_dest: list[Range] = sorted(self.ranges, key=lambda r: r.ds)

        i = j = 0
        while i < len(my_ranges_by_dest):
            myrange = my_ranges_by_dest[i]
            otherranges = other.ranges_by_src
            otherrange = otherranges[j]
            lastotherrange = j == len(otherranges) - 1

            # NOTE: The order of these matters.
            if myrange.isbefore(otherrange):
                otherrange.addleft(myrange.ds, myrange.de + 1)
                changed = True
                continue
            if myrange.overlapsleft(otherrange):
                otherrange.addleft(myrange.ds, otherrange.ss)
                myrange.splitleft(otherrange.ss)
                changed = True
                continue
            if myrange.issubrange(otherrange):
                i += 1
                continue
            if myrange.isafter(otherrange):
                if lastotherrange:
                    otherrange.addright(myrange.ds, myrange.de)
                    i += 1
                    changed = True
                    continue
                j += 1
                continue
            if myrange.overlapsright(otherrange):
                myrange.splitleft(otherrange.se + 1)
                changed = True
                continue

        return changed

    def map(self, src: int) -> int:
        for r in self.ranges_by_src:
            if r.ss <= src <= r.se:
                return r.ds + (src - r.ss)


def parse(lines) -> tuple[list[int], list[Group]]:
    seeds = [int(n) for n in re.findall(r"(\d+)", lines[0].split("seeds: ")[1])]

    groups: list[Group] = []
    group: list[list[int]] = Group()
    for line in lines[1:]:
        nums = re.findall(r"(\d+)", line)
        if nums:
            range = [int(n) for n in nums]
            range[0], range[1] = range[1], range[0]
            group.ranges.append(Range(group, *range))
            continue

        if group.ranges:
            groups.append(group)
            group = Group()

    groups.append(group)

    return seeds, groups


def solve(seedgroup, groups):
    changed = True

    while changed:
        changed = False
        prevgroup = seedgroup
        for g in groups:
            changed = changed or prevgroup.match_groups(g)
            prevgroup = g

    lowest = sys.maxsize
    for seedrange in seedgroup.ranges_by_src:
        seed = seedrange.ss
        for g in groups:
            seed = g.map(seed)
        lowest = min(lowest, seed)

    return lowest


def p1(lines):
    seeds, groups = parse(lines)

    seedgroup = Group()
    for seed in seeds:
        seedgroup.ranges.append(Range(seedgroup, seed, seed, 1))

    return solve(seedgroup, groups)


def p2(lines):
    seeds, groups = parse(lines)

    seedgroup = Group()
    for start, dist in chunks(seeds, 2):
        seedgroup.ranges.append(Range(seedgroup, start, start, dist))

    return solve(seedgroup, groups)


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "05.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
