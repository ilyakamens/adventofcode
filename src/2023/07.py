#!/usr/bin/env python

"""https://adventofcode.com/2023/day/07."""

from collections import Counter
from dataclasses import dataclass
from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


@dataclass
class Hand:
    hand: str
    bid: int
    mapping = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}

    @property
    def strength(self):
        counts = Counter(self.hand).values()
        set_length = len(set(self.hand))

        if len(counts) == 1:
            # Five of a kind.
            return -1
        if any(c == 4 for c in counts):
            # Four of a kind.
            return -2
        if set_length == 2:
            # Full house.
            return -3
        if any(c == 3 for c in counts):
            # Three of a kind.
            return -4
        if set_length == 3:
            # Two pair.
            return -5
        if any(c == 2 for c in counts):
            # One pair.
            return -6

        # High card.
        return -7

    def __lt__(self, other: "Hand"):
        if self.strength != other.strength:
            return self.strength < other.strength

        for c1, c2 in zip(self.hand, other.hand):
            v1 = self.mapping.get(c1, c1)
            v2 = self.mapping.get(c2, c2)
            if v1 == v2:
                continue

            return int(v1) < int(v2)

        raise RuntimeError("Hands are equal.")


@dataclass
class Hand2(Hand):
    hand: str
    bid: int
    mapping = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}

    @property
    def strength(self):
        if self.hand == "J" * 5:
            return super().strength

        hand = self.hand
        max_count = max(Counter(self.hand.replace("J", "")).items(), key=lambda x: x[1])
        self.hand = self.hand.replace("J", max_count[0])
        strength = super().strength
        self.hand = hand

        return strength


def p1(lines):
    hands = []
    for line in lines:
        hand, bid = line.split(" ")
        hands.append(Hand(hand, int(bid)))

    return sum(i * hand.bid for i, hand in enumerate(sorted(hands), start=1))


def p2(lines):
    hands = []
    for line in lines:
        hand, bid = line.split(" ")
        hands.append(Hand2(hand, int(bid)))

    return sum(i * hand.bid for i, hand in enumerate(sorted(hands), start=1))


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "07.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
