#!/usr/bin/env python

"""https://adventofcode.com/2020/day/22."""

from collections import defaultdict, deque
from itertools import islice
import os

prev_hands = defaultdict(dict)


def hash_hands(h1, h2):
    return ",".join(["".join([str(c) for c in h1]), "".join([str(c) for c in h2])])


def combat(h1, h2, i=0, recurse=False):
    if not h1:
        return False, h2
    if not h2:
        return True, h1

    h1, h2 = deque(h1), deque(h2)
    while len(h1) > 0 and len(h2) > 0:
        key = hash_hands(h1, h2)
        if recurse:
            if key in prev_hands[i]:
                return True, h1
            prev_hands[i][key] = True
        c1, c2 = h1.popleft(), h2.popleft()
        if not recurse or len(h1) < c1 or len(h2) < c2:
            wh = h1 if c1 > c2 else h2
        else:
            w, wh = combat(list(islice(h1, c1)), list(islice(h2, c2)), i + 1, True)
            wh = h1 if w else h2
        wh.extend([c1, c2] if wh == h1 else [c2, c1])
    return True if wh == h1 else False, wh


def score(hand):
    score = 0
    for i, c in enumerate(reversed(hand), start=1):
        score += i * c
    return score


if __name__ == "__main__":
    with open(os.path.join("input", "22.txt")) as f:
        h1, h2 = [[int(c) for c in l.strip().split("\n")[1:]] for l in f.read().split("\n\n")]

    _, wh = combat(h1, h2)
    print(f"Part 1: {score(wh)}")

    _, wh = combat(h1, h2, 0, True)
    print(f"Part 2: {score(wh)}")
