#!/usr/bin/env python

"""https://adventofcode.com/2015/day/15."""

import re
from dataclasses import dataclass
from itertools import combinations_with_replacement
from math import prod
from typing import Annotated

from main import main

run_type = Annotated[str, '1, 2, 3, etc., or real']


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @property
    def properties(self):
        return self.capacity, self.durability, self.flavor, self.texture


def parse(input: str) -> list[Ingredient]:
    ingredients: list[Ingredient] = []
    for line in input.splitlines():
        name, rest = line.split(': ')
        capacity, durability, flavor, texture, calories = map(int, re.findall(r'-?\d+', rest))
        ingredients.append(Ingredient(name, capacity, durability, flavor, texture, calories))

    return ingredients


def score(recipe: list[Ingredient]):
    properties = [0] * 4
    for ingredient in recipe:
        for i, p in enumerate(ingredient.properties):
            properties[i] += p

    return prod(max(p, 0) for p in properties)


def find_max_score(
    ingredients: list[Ingredient],
    num_ingredients: int = 100,
    calories: int | None = None,
):
    recipe: list[Ingredient] = []
    max_score = float('-inf')
    for test_recipe in combinations_with_replacement(ingredients, num_ingredients):
        new_score = score(test_recipe)
        if new_score > max_score and (calories is None or calorie_count(test_recipe) == calories):
            max_score = new_score
            recipe = test_recipe

    return score(recipe)


def calorie_count(recipe: list[Ingredient]):
    return sum(ingredient.calories for ingredient in recipe)


def p1(run: run_type, input: str) -> int:
    return find_max_score(parse(input))


def p2(run: run_type, input: str) -> int:
    return find_max_score(parse(input), calories=500)


if __name__ == '__main__':
    main(p1, p2, [62842880], [57600000])
