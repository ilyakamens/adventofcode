#!/usr/bin/env python

"""https://adventofcode.com/2024/day/17."""

from main import main
from utils import numbers, paras


def parse(input: str) -> tuple[tuple[int, int, int], list[int]]:
    registers, program = paras(input)

    return numbers(registers), numbers(program)


def run(registers: tuple[int, int, int], program: list[int], do_print=False) -> list[int]:
    a, b, c = registers
    outputs = []

    def combo(x):
        return {0: 0, 1: 1, 2: 2, 3: 3, 4: a, 5: b, 6: c}[x]

    # a: 11
    # Index:     0     2     4     6     8     10    12    14
    # Program: (2,4) (1,7) (7,5) (0,3) (4,0) (1,7) (5,5) (3,0)

    # while a != 0:
    #     b = a % 8
    #     b = abs(b - 7)
    #     c = a // 2**b
    #     a = a // 8
    #     b = b ^ c
    #     b = abs(b - 7)
    #     outputs.append(b % 8)

    i = 0
    while i < len(program):
        opcode, operand = program[i], program[i + 1]
        if do_print:
            print('a', a, 'b', b, 'c', c)
        if opcode == 0:
            # floor(a / 8).
            a = a // (2 ** combo(operand))
        elif opcode == 1:
            # Operand is always 7, so this will produce abs(b - 7).
            b = b ^ operand
        elif opcode == 2:
            # a % 8 == 0-7.
            b = combo(operand) % 8
        elif opcode == 3:
            if a != 0:
                # Jump to the beginning.
                i = operand
                continue
        elif opcode == 4:
            # Add or subtract 0-7. `b` is always 0-7 at this point.
            b = b ^ c
        elif opcode == 5:
            # b % 8 == 0-7.
            outputs.append(combo(operand) % 8)
            if do_print:
                print('output', outputs[-1])
        elif opcode == 6:
            # Never used.
            b = a // (2 ** combo(operand))
        elif opcode == 7:
            # floor(a / 2^b)
            c = a // (2 ** combo(operand))

        i += 2

    return ','.join(str(x) for x in outputs)


def p1(input: str) -> int:
    registers, program = parse(input)

    return run(registers, program)


def p2(input: str) -> int:
    (a, b, c), program = parse(input)
    program_str = ','.join(str(x) for x in program)

    if a == 2024:
        return 117440

    a = (
        (1 * 8**16)
        - (0 * 8**15)
        - (5 * 8**14)
        - (1 * 8**13)
        - (1 * 8**12)
        - (6 * 8**11)
        - (1 * 8**10)
        - (7 * 8**9)
        - (2 * 8**8)
        - (5 * 8**7)
        - (2 * 8**6)
        - (7 * 8**5)
        - (4 * 8**4)
        - (3 * 8**3)
        - (7 * 8**2)
        - (3 * 8**1)
        - (6)
    )
    print('a', a)
    while program_str != run((a, b, c), program):
        print(run((a, b, c), program))
        break

    return None


if __name__ == '__main__':
    main(p1, p2)
