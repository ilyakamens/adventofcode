#!/usr/bin/env python

"""https://adventofcode.com/2020/day/16."""

from collections import defaultdict
import heapq
import os


class RuleChoices:
    def __init__(self, rules, i):
        self.rules = rules
        self.i = i

    @property
    def val(self):
        return len(self.rules)

    def __lt__(self, other):
        return self.val < other.val

    def remove(self, rule):
        self.rules.remove(rule)


if __name__ == "__main__":
    with open(os.path.join("input", "16.txt")) as f:
        rules_str, my_ticket, other_tickets = [part.strip() for part in f.read().split("\n\n")]

    rule_set = set()
    rule_map = defaultdict(set)
    for rule in rules_str.split("\n"):
        name, nums = rule.split(": ")
        rule_set.add(name)
        for range_ in nums.split(" or "):
            low, high = [int(num) for num in range_.split("-")]
            for i in range(low, high + 1):
                rule_map[i].add(name)

    tickets = [[int(n) for n in t.split(",")] for t in other_tickets.split("\n")[1:]]

    invalid_ticket_vals = []
    for ticket in tickets:
        invalid_ticket_vals.append(*[n for n in ticket if n not in rule_map] or [0])

    print(f"Part 1: {sum(invalid_ticket_vals)}")

    good_tickets = [ticket for ticket in tickets if all(v in rule_map for v in ticket)]
    rule_combos = [rule_set for _ in rule_set]
    for ticket in good_tickets:
        for i, part in enumerate(ticket):
            rule_combos[i] = rule_combos[i].intersection(rule_map[part])

    correct_order = [None for _ in rule_combos]
    heap = [RuleChoices(r, i) for i, r in enumerate(rule_combos)]
    heapq.heapify(heap)
    while heap:
        rc = heapq.heappop(heap)
        rule = rc.rules.pop()
        correct_order[rc.i] = rule
        for choice in heap:
            choice.remove(rule)
        heap.sort()

    product = 1
    my_ticket = [int(n) for n in my_ticket.split("\n")[1].split(",")]
    for rule, ticket_part in zip(correct_order, my_ticket):
        if rule.startswith("departure"):
            product *= ticket_part

    print(f"Part 2: {product}")
