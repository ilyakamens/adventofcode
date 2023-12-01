#!/usr/bin/env python

"""https://adventofcode.com/2022/day/15."""

from collections import *
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *

y = 2_000_000


class Sensor:
    def __init__(self, x, y, bx, by):
        self.x = x
        self.y = y
        self.beacon = (bx, by)
        self.beacon_manhattan = self._manhattan(*self.beacon)

    @property
    def coords(self):
        return (self.x, self.y)

    def _manhattan(self, x, y):
        return abs(x - self.x) + abs(y - self.y)

    def in_range(self, x, y):
        return self.beacon_manhattan >= self._manhattan(x, y)


def p1(lines):
    sensors = []

    for line in lines:
        sensors.append(Sensor(*map(int, re.findall("=([-+]?\d{1,})", line))))

    coords = set()
    for sensor in sensors:
        diff = sensor.beacon_manhattan - abs(sensor.y - y)
        for x in range(sensor.x - diff, (sensor.x + diff) + 1):
            coords.add((x, y))

    for sensor in sensors:
        coords.discard(sensor.beacon)

    return len(coords)


def p2(lines):
    pass


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "15.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
