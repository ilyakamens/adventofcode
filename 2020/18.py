#!/usr/bin/env python

"""https://adventofcode.com/2020/day/18."""

from collections import deque
import os


def postfix(expr, part_2=False):
    queue = deque([])
    stack = []
    for c in expr:
        if c in {"+", "*"}:
            while len(stack) and stack[-1] != "(":
                if part_2 and stack[-1] == "*" and c == "+":
                    break
                queue.append(stack.pop())
            stack.append(c)
        elif c == "(":
            stack.append(c)
        elif c == ")":
            while stack[-1] != "(":
                queue.append(stack.pop())
            stack.pop()
        else:
            queue.append(c)
    while len(stack):
        queue.append(stack.pop())
    return queue


if __name__ == "__main__":
    with open(os.path.join("input", "18.txt")) as f:
        exprs = [l.replace(" ", "") for l in f.read().splitlines()]

    for i in range(1, 3):
        n = 0
        for expr in exprs:
            stack = []
            queue = postfix(expr, part_2=i == 2)
            while len(queue):
                o = queue.popleft()
                stack.append(eval(f"{stack.pop()}{o}{stack.pop()}") if o in {"+", "*"} else o)
            n += stack[0]

        print(f"Part {i}: {n}")
