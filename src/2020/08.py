#!/usr/bin/env python

"""https://adventofcode.com/2020/day/8."""

from collections import namedtuple
import os


class CorruptInstruction(Exception):
    pass


Override = namedtuple("Override", ["op", "arg", "i"])


def run(ignoreCorruption=False, override=Override(None, None, None)):
    i = 0
    acc = 0
    executed = set()

    def execute_instruction(op, arg):
        nonlocal i, acc

        if op == "acc":
            acc += int(arg)
        elif op == "jmp":
            i += int(arg)
            return
        i += 1

    while i not in executed and 0 <= i < len(instructions):
        executed.add(i)

        op, arg = (override.op, override.arg) if override.i == i else instructions[i].split(" ")
        execute_instruction(op, arg)

    if not ignoreCorruption and i != len(instructions):
        raise CorruptInstruction

    return acc


if __name__ == "__main__":
    with open(os.path.join("input", "08.txt")) as f:
        instructions = f.read().splitlines()

    for i, instruction in enumerate(instructions):
        op, arg = instruction.split(" ")
        if op == "nop":
            op = "jmp"
        elif op == "jmp":
            op = "nop"
        else:
            continue

        try:
            acc = run(override=Override(op, arg, i))
        except CorruptInstruction:
            continue
        else:
            break

    print(f"Part 1: {run(ignoreCorruption=True)}")
    print(f"Part 2: {acc}")
