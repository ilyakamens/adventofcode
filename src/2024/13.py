#!/usr/bin/env python

"""https://adventofcode.com/2024/day/13."""

from main import main, runs
from utils import numbers, paras

A_COST = 3
B_COST = 1


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    machines = paras(input)
    costs = 0
    for p in machines:
        x1, y1, x2, y2, xp, yp = numbers(p)
        min_cost = float('inf')
        for i in range(1, 101):
            for j in range(1, 101):
                if i * x1 + j * x2 == xp and i * y1 + j * y2 == yp:
                    min_cost = min(min_cost, i * A_COST + j * B_COST)
        if min_cost != float('inf'):
            costs += min_cost

    return costs


def calc_count(eq1: tuple[int, int, int], eq2: tuple[int, int, int]) -> int:
    """Solve for B in:

    AX1 + BY1 = C1.
    AX2 + BY2 = C2.

    Simplified version of:
    1. Multiply eq1 by X2.
    2. Multiply eq2 by X1.
    3. Subtract eq2 from eq1 (A disappears).
    4. Divide both sides by Y.


    E.g.:
    A94 + B22 = 8400
    A34 + B67 = 5400

    3162A + 748B = 285600
    3162A + 6298B = 507600

    5550B = 222000

    B = 40
    """
    a, b, c = eq1
    d, e, f = eq2

    return (c * d - f * a) / (b * d - e * a)


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    machines = paras(input)
    costs = 0
    for p in machines:
        x1, y1, x2, y2, xp, yp = numbers(p)
        xp = 10000000000000 + xp
        yp = 10000000000000 + yp
        b_count = calc_count((x1, x2, xp), (y1, y2, yp))
        a_count = calc_count((x2, x1, xp), (y2, y1, yp))
        if int(b_count) != b_count or int(a_count) != a_count:
            continue

        costs += int(a_count) * A_COST + int(b_count) * B_COST

    return costs


if __name__ == '__main__':
    main(p1, p2, [480], [875318608908])
