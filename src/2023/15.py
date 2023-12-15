#!/usr/bin/env python

"""https://adventofcode.com/2023/day/15."""

from dataclasses import dataclass, field
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


@dataclass
class Node:
    label: str
    lense: int
    next: "Node" = None
    prev: "Node" = None


@dataclass
class LL:
    head: Node = None
    tail: Node = None
    map: dict = field(default_factory=dict)

    def append(self, label: str, lense: int):
        node = Node(label, lense)
        self.map[label] = node

        if not self.head:
            self.head = node
            self.tail = self.head
            return

        node.prev = self.tail
        self.tail.next = node
        self.tail = node

    def remove(self, label: str):
        node = self.map.pop(label, None)
        if not node:
            return

        if node == self.head == self.tail:
            self.head = None
            self.tail = None
            return
        if node == self.head:
            self.head = node.next
            self.head.prev.next = None
            self.head.prev = None
            return
        if node == self.tail:
            self.tail = node.prev
            self.tail.next.prev = None
            self.tail.next = None
            return

        node.prev.next = node.next
        node.next.prev = node.prev

    def replace(self, label: str, lense: int):
        node = self.map.get(label)
        if node:
            node.lense = lense

        return node is not None

    def __str__(self):
        node = self.head
        s = ""
        while node:
            s += f"{node.label}:{node.lense} "
            node = node.next
        return s


def compute_hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256

    return h


def p1(steps):
    return sum(compute_hash(step) for step in steps)


def p2(steps):
    boxes = [LL() for _ in range(256)]

    for step in steps:
        label = re.search(r"\w+", step).group()
        idx = compute_hash(label)
        if step.endswith("-"):
            boxes[idx].remove(label)
            continue
        lense = int(step[-1])
        if not boxes[idx].replace(label, lense):
            boxes[idx].append(label, lense)

    sums = 0
    for i, box in enumerate(boxes, start=1):
        node = box.head
        j = 1
        while node:
            sums += i * node.lense * j
            node = node.next
            j += 1

    return sums


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "15.txt")) as f:
        lines = f.read().strip().split(",")

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
