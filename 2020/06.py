#!/usr/bin/env python

"""https://adventofcode.com/2020/day/6."""

from functools import reduce
import os

if __name__ == "__main__":
    with open(os.path.join("input", "06.txt")) as f:
        group_answers = [answers.replace("\n", " ").strip() for answers in f.read().split("\n\n")]

    yes_union_count = 0
    yes_intersection_count = 0
    for group_answer in group_answers:
        yes_union = set(group_answer.replace(" ", ""))
        # Part 1: At least one person in the group answered "yes" to the question (set union)
        yes_union_count += len(yes_union)

        # Part 2: Everyone in the group answered "yes" to the question (set intersection)
        first, *rest = group_answer.split(" ")
        yes_intersection_count += len(set(first).intersection(*[set(r) for r in rest]))

    print(f"Number of questions to which any in group answered 'yes': {yes_union_count}")
    print(
        f"Number of questions to which everyone in group answered 'yes': {yes_intersection_count}"
    )
