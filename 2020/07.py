#!/usr/bin/env python

"""https://adventofcode.com/2020/day/7."""

from collections import defaultdict, deque
from functools import reduce
import os
import re

if __name__ == "__main__":
    with open(os.path.join("input", "07.txt")) as f:
        rules = f.read().splitlines()

    # Part 1: Which bags contain one bag in particular?
    parent_graph = defaultdict(set)
    # Part 2: Which bags does one bag in particular contain?
    children_graph = defaultdict(set)
    bag_counts = defaultdict(dict)
    leafs = set()
    for rule in rules:
        bag = re.match("^(?P<bag>.+) bags contain", rule).group("bag")
        children = set(re.findall("([0-9]+) ([a-z ]+) bag[s]?[,.]", rule))

        for count, child in children:
            parent_graph[child].add(bag)
            children_graph[bag].add(child)
            bag_counts[bag][child] = int(count)

        if not children:
            leafs.add(bag)

    # Part 1
    ancestors = set()
    queue = deque(["shiny gold"])
    while len(queue):
        bag = queue.popleft()
        ancestors.update(parent_graph[bag])
        queue.extend(parent_graph[bag])

    # Part 2
    visited = set()
    running_sums = defaultdict(int)
    queue = deque(leafs)
    while len(queue):
        bag = queue.popleft()
        if bag in visited:
            running_sums[bag] = 0
        for child in children_graph[bag]:
            child_count = bag_counts[bag][child]
            running_sums[bag] += child_count + (running_sums[child] * child_count)
        queue.extend(parent_graph[bag])
        visited.add(bag)

    print(f"Part 1: {len(ancestors)}")
    print(f"Part 2: {running_sums['shiny gold']}")
