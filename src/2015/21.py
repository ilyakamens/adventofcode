#!/usr/bin/env python

"""https://adventofcode.com/2015/day/21."""

from dataclasses import dataclass
from itertools import combinations
from math import ceil
from typing import Generator, Literal

from main import main, runs
from utils import paras

ITEMS = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3"""


@dataclass
class Player:
    hp: int
    damage: int
    armor: int
    items: list['Item']

    def __post_init__(self) -> None:
        for item in self.items:
            self.damage += item.damage
            self.armor += item.armor


BOSS = Player(hp=109, damage=8, armor=2, items=[])


@dataclass
class Item:
    name: str
    type: Literal['Weapons', 'Armor', 'Rings']
    cost: int
    damage: int
    armor: int


def count(items: list[Item], t: Literal['Weapons', 'Armor', 'Rings']) -> int:
    return len([item for item in items if item.type == t])


def play(player: Player) -> bool:
    player_dead_turns = ceil(player.hp / max(BOSS.damage - player.armor, 1))
    boss_dead_turns = ceil(BOSS.hp / max(player.damage - BOSS.armor, 1))

    return player_dead_turns >= boss_dead_turns


def parse_items() -> list[Item]:
    items: list[Item] = []
    for p in paras(ITEMS):
        for l in p.splitlines():
            if ':' in l:
                item_type = l.split(':')[0]
                continue
            name, *rest = [x.strip() for x in l.split()]
            if name in {'Damage', 'Defense'}:
                name = f'{name} {rest[0]}'
                rest = rest[1:]
            cost, damage, armor = [int(x) for x in rest]
            items.append(Item(name, item_type, cost, damage, armor))

    return sorted(items, key=lambda item: item.cost)


def iter_items(items: list[Item]) -> Generator[list[Item], None, None]:
    for i in range(1, len(items) + 1):
        for group in combinations(items, i):
            if (
                count(group, 'Weapons') != 1
                or count(group, 'Armor') > 1
                or count(group, 'Rings') > 2
            ):
                continue
            yield group, sum(item.cost for item in group)


@runs(cases=set())
def p1(input: str, case: str) -> int:
    min_cost = float('inf')
    for group, cost in iter_items(parse_items()):
        if cost >= min_cost:
            continue
        if play(Player(hp=100, damage=0, armor=0, items=group)):
            min_cost = cost

    return min_cost


@runs(cases=set())
def p2(input: str, case: str) -> int:
    max_cost = float('-inf')
    for group, cost in iter_items(parse_items()):
        if cost <= max_cost:
            continue
        if not play(Player(hp=100, damage=0, armor=0, items=group)):
            max_cost = cost

    return max_cost


if __name__ == '__main__':
    main(p1, p2, [None], [None])
