#!/usr/bin/env python

"""https://adventofcode.com/2020/day/13."""

import math
import os
import sys


def dep(d1, d2, b, diff):
    count = 0
    while True and count != 2:
        if (d1 + diff) % b == 0:
            yield d1
            count += 1
        d1, d2 = d2, d2 + (d2 - d1)


if __name__ == "__main__":
    with open(os.path.join("input", "13.txt")) as f:
        input_ = f.read().splitlines()

    earliest_could = int(input_[0])
    bus_times = [int(bus_time) for bus_time in input_[1].replace("x,", "").split(",")]

    earliest_bus_id = None
    shortest_wait = sys.maxsize
    for bus_time in bus_times:
        wait = (bus_time * math.ceil(earliest_could / bus_time)) - earliest_could
        if wait < shortest_wait:
            shortest_wait = wait
            earliest_bus_id = bus_time

    print(f"Part 1: {earliest_bus_id * shortest_wait}")

    bus_times = [int(bus_time) for bus_time in input_[1].replace("x", "-1").split(",")]
    d1 = bus_times[0]
    d2 = d1 * 2
    for i, _ in enumerate(bus_times[1:], start=1):
        if bus_times[i] == -1:
            continue
        d1, d2 = dep(d1, d2, bus_times[i], i)

    print(f"Part 2: {d1}")
