#!/usr/bin/env python

"""https://adventofcode.com/2020/day/21."""

from collections import defaultdict
import heapq
import os
import re


def iterlines(input_):
    for line in input_:
        ingredients = line.split(" (")[0].split(" ")
        allergens = re.search("\(contains (.+)\)", line).group(1).split(", ")
        yield ingredients, allergens


class Allergen:
    def __init__(self, name):
        self.name = name
        self.ingredients = defaultdict(int)

    @property
    def val(self):
        return len(self.ingredients)

    def __repr__(self):
        return f"{self.name}: {self.ingredients}"

    def __lt__(self, other):
        return self.val < other.val

    def add(self, i):
        self.ingredients[i] += 1

    def remove(self, i):
        del self.ingredients[i]

    def remove_safe_ingredients(self):
        max_count = max(self.ingredients.values())
        self.ingredients = {i: count for i, count in self.ingredients.items() if count == max_count}


if __name__ == "__main__":
    with open(os.path.join("input", "21.txt")) as f:
        input_ = f.read().splitlines()

    # Build Allergen map
    allergen_map = {}
    for ingredients, allergens in iterlines(input_):
        for allergen_str in allergens:
            if allergen_str not in allergen_map:
                allergen_map[allergen_str] = Allergen(allergen_str)
            allergen = allergen_map[allergen_str]
            for i in ingredients:
                allergen.add(i)

    # Remove safe ingredients + build ingredient map
    ingredients_map = defaultdict(set)
    allergic_ingredients = set()
    for allergen in allergen_map.values():
        allergen.remove_safe_ingredients()
        allergic_ingredients.update(allergen.ingredients.keys())
        for i in allergen.ingredients:
            ingredients_map[i].add(allergen)

    # Count safe ingredients
    count = 0
    for ingredients, _ in iterlines(input_):
        count += len([i for i in ingredients if i not in allergic_ingredients])

    print(f"Part 1: {count}")

    # Map bad allergens to their ingredients
    bad = {}
    heap = list(allergen_map.values())
    heapq.heapify(heap)
    while heap:
        allergen = heapq.heappop(heap)
        ingredient = list(allergen.ingredients)[0]
        bad[allergen.name] = ingredient
        for a in ingredients_map[ingredient]:
            a.remove(ingredient)
        heap.sort()

    print(f"Part 2: {','.join([tup[1] for tup in sorted(bad.items(), key=lambda x: x[0])])}")
