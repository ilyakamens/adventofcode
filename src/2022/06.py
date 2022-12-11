#!/usr/bin/env python

"""https://adventofcode.com/2022/day/06."""

from collections import *
from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *


def start_of_packet_marker(packet, segment_length):
    for i in range(len(packet)):
        if i < segment_length - 1:
            continue
        if len({*list(packet[i - segment_length : i])}) == segment_length:
            return i


def p1(line):
    return start_of_packet_marker(line, 4)


def p2(line):
    return start_of_packet_marker(line, 14)


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "06.txt")) as f:
        lines = f.read().splitlines()

    for num, func in ((1, p1), (2, p2)):
        print(f"Part {num}: {func(lines[0])}")
