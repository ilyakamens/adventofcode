#!/usr/bin/env python

"""https://adventofcode.com/2020/day/5."""

import os

table = {
    "B": "1",
    "F": "0",
    "R": "1",
    "L": "0",
}


def compute_seat_id(boarding_pass):
    row = "".join([table[step] for step in boarding_pass[:7]])
    col = "".join([table[step] for step in boarding_pass[7:]])

    return (int(row, 2) * 8) + int(col, 2)


if __name__ == "__main__":
    with open(os.path.join("input", "05.txt")) as f:
        boarding_passes = f.read().splitlines()

    seat_ids = sorted([compute_seat_id(boarding_pass) for boarding_pass in boarding_passes])

    my_seat_id = None
    for i, seat_id in enumerate(seat_ids[:-1]):
        if seat_ids[i + 1] - seat_id == 2:
            my_seat_id = seat_id + 1
            break

    print(f"Highest seat ID (part 1): {seat_ids[-1]}")
    print(f"My seat ID (part 2): {my_seat_id}")
