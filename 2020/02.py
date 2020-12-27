#!/usr/bin/env python

"""https://adventofcode.com/2020/day/2."""

import os

if __name__ == "__main__":
    with open(os.path.join("input", "02.txt")) as f:
        password_lines = f.read().splitlines()

    num_valid_pt_1 = 0
    num_valid_pt_2 = 0
    for password_line in password_lines:
        split = password_line.split(" ")
        min_req, max_allowed = [int(rule) for rule in split[0].split("-")]
        req_char = split[1][0]
        password = split[2]

        # Part 1: Compute the number of valid passports given the min and max times the required
        # char should appear in the password.
        password_count = password.count(req_char)
        if min_req <= password_count <= max_allowed:
            num_valid_pt_1 += 1

        # Part 2: Compute the number of valid passports given the required char at one, but not
        # both, indices.
        index_1, index_2 = min_req, max_allowed
        index_1_satisfied = password[index_1 - 1] == req_char
        index_2_satisfied = password[index_2 - 1] == req_char
        # XOR
        if index_1_satisfied != index_2_satisfied:
            num_valid_pt_2 += 1

    print(f"Number of valid passwords (part 1): {num_valid_pt_1}")
    print(f"Number of valid passwords (part 2): {num_valid_pt_2}")
