#!/usr/bin/env python

"""https://adventofcode.com/2020/day/11."""

import os
import sys


def iter_seats(seats):
    for row, _ in enumerate(seats):
        for col, _ in enumerate(seats[row]):
            yield row, col


def calc_changes(seats, max_iter, min_num_occupied_to_switch):
    changes = {}
    for row, col in iter_seats(seats):
        seat = seats[row][col]
        if seat == ".":
            continue
        num_occupied = calc_num_occupied(row, col, seats, max_iter)
        if seat == "L" and num_occupied == 0:
            changes[(row, col)] = "#"
        if seat == "#" and num_occupied >= min_num_occupied_to_switch:
            changes[(row, col)] = "L"

    return changes


def calc_num_occupied(row, col, seats, max_iter):
    num_occupied = 0
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if x == y == 0:
                continue
            if is_occupied_in_direction(row, col, x, y, seats, max_iter):
                num_occupied += 1

    return num_occupied


def is_occupied_in_direction(row, col, x, y, seats, max_iterations):
    for _ in range(max_iterations):
        row += x
        col += y
        if min(col, row) < 0:
            return False
        if row >= len(seats) or col >= len(seats[row]):
            return False
        if seats[row][col] == "L":
            return False
        if seats[row][col] == "#":
            return True

    return False


if __name__ == "__main__":
    for i, (num_occupied_func, min_num_occupied_to_switch) in enumerate(
        ((1, 4), (sys.maxsize, 5)),
        start=1,
    ):
        with open(os.path.join("input", "11.txt")) as f:
            seats = [list(row) for row in f.read().splitlines()]

        changes = {"fake": "change"}
        while changes:
            changes = calc_changes(seats, num_occupied_func, min_num_occupied_to_switch)
            for (row, col), change in changes.items():
                seats[row][col] = change

        num_occupied = 0
        for row, col in iter_seats(seats):
            if seats[row][col] == "#":
                num_occupied += 1

        print(f"Part {i}: {num_occupied}")
