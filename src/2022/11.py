#!/usr/bin/env python

"""https://adventofcode.com/2022/day/11."""

from collections import *
from math import lcm
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *

MONKEYS = {}


class Monkey:
    def __init__(self, lines):
        monkey, items, operation, test, true, false = [
            l.strip() for l in lines.splitlines()
        ]

        self.name = monkey.split(" ")[1][0]
        self.items = deque(items.split("Starting items: ")[1].split(", "))
        operation = operation.split("Operation: new = ")[1]
        self.operate = lambda item: eval(operation.replace("old", item))
        self.divisor = int(test.split(" ")[-1])
        self.test = lambda item: item % self.divisor == 0
        self.true = true.split(" ")[-1]
        self.false = false.split(" ")[-1]

        MONKEYS[self.name] = self
        self.num_inspections = 0

    def inspect(self, reduce_worry):
        while self.items:
            self.num_inspections += 1

            item = self.items.popleft()
            item = self.operate(item)
            item = reduce_worry(item)
            monkey = self.true if self.test(item) else self.false
            MONKEYS[monkey].items.append(str(item))

    def __str__(self):
        return f"Monkey {self.name}: {', '.join(self.items)}"


def p1(monkeys):
    for _ in range(20):
        for monkey in monkeys:
            monkey.inspect(lambda item: item // 3)

    m1, m2, *_ = sorted(monkeys, key=lambda m: m.num_inspections, reverse=True)

    return m1.num_inspections * m2.num_inspections


def p2(monkeys):
    LCM = lcm(*[m.divisor for m in monkeys])

    for _ in range(10_000):
        for monkey in monkeys:
            monkey.inspect(lambda item: item % LCM)

    m1, m2, *_ = sorted(monkeys, key=lambda m: m.num_inspections, reverse=True)

    return m1.num_inspections * m2.num_inspections


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "11.txt")) as f:
        lines = f.read().split("\n\n")

    print(f"Part 1: {p1([Monkey(monkey) for monkey in lines])}")
    print(f"Part 2: {p2([Monkey(monkey) for monkey in lines])}")
