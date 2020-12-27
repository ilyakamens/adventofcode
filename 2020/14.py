#!/usr/bin/env python

"""https://adventofcode.com/2020/day/14."""

from collections import defaultdict
import os
import re


def get_binstr(intstr):
    binstr = bin(int(intstr))[2:]

    return "0" * (36 - len(binstr)) + binstr


def parse_instruction(line):
    l, r = line.split(" = ")
    address = re.match("mem\[(?P<address>[0-9]+)\]", l).group("address")

    return address, get_binstr(r)


def mask_val(mask, binstr):
    masked = []
    for m, b in zip(mask, binstr):
        masked.append(m if m != "X" else b)

    return int("".join(masked), 2)


def get_addresses(mask, address):
    binstr = get_binstr(address)

    masked = []
    float_indices = []
    i = 0
    for m, b in zip(mask, binstr):
        masked.append(b if m == "0" else m)
        if m == "X":
            float_indices.append(i)
        i += 1

    addresses = ["".join(masked)]
    for i in float_indices:
        new_addresses = []
        for address in addresses:
            for c in ("0", "1"):
                new_addresses.append(address[:i] + c + address[i + 1 :])
        addresses = new_addresses

    return [int(address, 2) for address in addresses]


def decode(lines, mask_addresses=False):
    memory = defaultdict(int)
    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
            continue

        address, binstr = parse_instruction(line)
        val = mask_val(mask, binstr) if not mask_addresses else int(binstr, 2)
        addresses = get_addresses(mask, address) if mask_addresses else [address]
        for address in addresses:
            memory[address] = val

    return memory


if __name__ == "__main__":
    with open(os.path.join("input", "14.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {sum(decode(lines).values())}")

    print(f"Part 2: {sum(decode(lines, mask_addresses=True).values())}")
