#!/usr/bin/env python

"""https://adventofcode.com/2015/day/13."""

import re
from collections import defaultdict
from itertools import permutations

from main import main
from utils import sliding_window


def gen_scores(input):
    scores = defaultdict(lambda: defaultdict(int))
    for line in input.splitlines():
        happiness = int(re.search(r'\d+', line).group())
        happiness = -happiness if ' lose ' in line else happiness
        split = line.split()
        scores[split[0]][split[-1][:-1]] = happiness

    return scores


def calc_happiness(scores, permutation):
    happiness = scores[permutation[-1]][permutation[0]]
    happiness += scores[permutation[0]][permutation[-1]]

    for a, b in sliding_window(permutation, 2):
        happiness += scores[a][b]
        happiness += scores[b][a]

    return happiness


def calc_max_happiness(scores):
    max_happiness = float('-inf')
    for permutation in permutations(scores.keys()):
        max_happiness = max(max_happiness, calc_happiness(scores, permutation))

    return max_happiness


def p1(input):
    scores = gen_scores(input)

    return calc_max_happiness(scores)


def p2(input):
    scores = gen_scores(input)

    scores['me'] = defaultdict(int)
    for person in scores.keys():
        if person == 'me':
            continue
        scores[person]['me'] = 0
        scores['me'][person] = 0

    return calc_max_happiness(scores)


if __name__ == '__main__':
    main(p1, p2, [330], [286])
