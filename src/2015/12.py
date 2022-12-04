#!/usr/bin/env python

"""https://adventofcode.com/2015/day/12."""

import json
import os


def getsome(doc, skip=None):
    some = 0

    dfs = [v for v in doc.values()]
    while dfs:
        v = dfs.pop()
        if isinstance(v, int):
            some += v
            continue
        if isinstance(v, str):
            continue
        if isinstance(v, dict):
            if skip in v or skip in v.values():
                continue
            v = v.values()
        for e in v:
            dfs.append(e)

    return some


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "12.txt")) as f:
        doc = json.load(f)

    print(f"Part 1: {getsome(doc)}")
    print(f"Part 2: {getsome(doc, skip='red')}")
