#!/usr/bin/env python

"""https://adventofcode.com/2022/day/07."""

from collections import *
from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *

DIR_MAP = {}


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent if parent else self
        self.children = []
        self.file_sizes = 0

    @property
    def size(self):
        return self.file_sizes + sum(child.size for child in self.children)

    @property
    def pwd(self):
        return f"{self.parent.pwd}/{self.name}" if self.name != "/" else "/"


def p1(lines):
    current_dir = None

    for line in lines:
        if line == "$ cd ..":
            current_dir = current_dir.parent
        elif line.startswith("$ cd "):
            name = line.split(" ")[2]
            child_dir = Dir(name, current_dir)
            if child_dir.pwd not in DIR_MAP:
                DIR_MAP[child_dir.pwd] = child_dir
            if current_dir:
                current_dir.children.append(DIR_MAP[child_dir.pwd])
            current_dir = DIR_MAP[child_dir.pwd]
        elif line == "$ ls":
            continue
        elif not line.startswith("dir"):
            l, _ = line.split(" ")
            current_dir.file_sizes += int(l)

    total_size = 0
    nodes = [DIR_MAP["/"]]
    for node in nodes:
        if node.size <= 100_000:
            total_size += node.size
        for child in node.children:
            nodes.append(child)

    return total_size


def p2():
    DISK_SIZE = 70_000_000
    SPACE_NEEDED = 30_000_000

    root = DIR_MAP["/"]
    SPACE_USED = root.size
    TO_FREE = SPACE_NEEDED - (DISK_SIZE - SPACE_USED)

    smallest_sufficient = root

    nodes = [root]
    for node in nodes:
        if node.size >= TO_FREE and node.size < smallest_sufficient.size:
            smallest_sufficient = node
        for child in node.children:
            nodes.append(child)

    return smallest_sufficient.size


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "07.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2()}")
