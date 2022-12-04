#!/usr/bin/env python

"""https://adventofcode.com/2020/day/1."""

import os
import sys

if __name__ == "__main__":
    with open(os.path.join("input", "01.txt")) as f:
        expenses = [int(expense) for expense in f.read().splitlines()]
    expenses_map = {expense: expense for expense in expenses}

    # Part 1: Find the two expenses that sum to 2020 and compute their product.
    for expense in expenses:
        remainder = 2020 - expense
        if remainder not in expenses_map:
            continue
        print(f"Product (part 1): {expense * remainder}")
        break

    # Part 2: Find the three expenses that sum to 2020 and compute their product.
    for i, expense_1 in enumerate(expenses):
        for expense_2 in expenses[i:]:
            remainder = 2020 - (expense_1 + expense_2)
            if remainder in expenses_map:
                print(f"Product (part 2): {expense_1 * expense_2 * remainder}")
                sys.exit(0)
