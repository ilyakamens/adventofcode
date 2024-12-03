#!/usr/bin/env python

"""https://adventofcode.com/2015/day/14."""

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from main import main


@dataclass
class Reindeer:
    name: str
    speed: int
    duration: int
    rest: int

    def distance_after(self, time) -> int:
        cycle_time = self.duration + self.rest
        full_cycles = time // cycle_time
        remaining_time = time % cycle_time

        return (
            full_cycles * self.speed * self.duration
            + min(remaining_time, self.duration) * self.speed
        )


def parse(input) -> List[Reindeer]:
    return [
        Reindeer(name, int(speed), int(duration), int(rest))
        for name, speed, duration, rest in re.findall(
            r'(\w+) can fly (\d+) km/s for (\d+) .+, .+ rest for (\d+) seconds', input
        )
    ]


def calc_points(reindeers: List[Reindeer], time: int) -> Dict[str, int]:
    points = defaultdict(int)
    for i in range(1, time + 1):
        max_distance = float('-inf')
        leading_reindeers = []
        for reindeer in reindeers:
            distance = reindeer.distance_after(i)
            if distance > max_distance:
                max_distance = distance
                leading_reindeers = [reindeer]
            elif distance == max_distance:
                leading_reindeers.append(reindeer)
        for reindeer in leading_reindeers:
            points[reindeer.name] += 1

    return points


def p1(input):
    reindeers = parse(input)

    return max(reindeer.distance_after(2503) for reindeer in reindeers)


def p2(input):
    reindeers = parse(input)

    return max(calc_points(reindeers, 2503).values())


if __name__ == '__main__':
    main(p1, p2, [2660], [1564])
