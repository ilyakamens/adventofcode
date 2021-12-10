#!/usr/bin/env python

"""https://adventofcode.com/2021/day/10."""

from collections import defaultdict
import os

def is_closing(c, o):
    return (c == "[" and o == "]") or (c == "(" and o == ")") or (c == "{" and o == "}") or (c == "<" and o == ">")

def p1(lines):
    bads = []

    for line in lines:
        stack = []
        for c in line:
            if c in "({[<":
                stack.append(c)
            elif is_closing(stack[-1], c):
                stack.pop()
            else:
                bads.append(c)
                break

    sum_ = 0
    for bad in bads:
        if bad == ")":
            sum_ += 3
        elif bad == "]":
            sum_ += 57
        elif bad == "}":
            sum_ += 1197
        elif bad == ">":
            sum_ += 25137

    return sum_



def p2(lines):
    remainders = []

    for line in lines:
        stack = []
        for c in line:
            if c in "({[<":
                stack.append(c)
            elif is_closing(stack[-1], c):
                stack.pop()
            else:
                break
        else:
            remainders.append("".join(stack))

    scores = []
    for remainder in remainders:
        score = 0
        for c in reversed(remainder):
            score *= 5
            if c == "(":
                score += 1
            elif c == "[":
                score += 2
            elif c == "{":
                score += 3
            elif c == "<":
                score += 4

        scores.append(score)

    return sorted(scores)[len(scores) // 2]

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "10.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
