import os
import sys
import time
from collections.abc import Callable
from functools import wraps
from typing import Annotated

import aocd
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table


def _format_result(result, expected):
    return (
        f'[green]{result}[/green]'
        if result == expected
        else (
            f'[yellow]{result}[/yellow]'
            if expected is None
            else f'[red]{result}[/red] != [green]{expected}[/green]'
        )
    )


def _print_rich(p1_pairs, p2_pairs):
    console = Console()
    table = Table(show_footer=False)
    table_centered = Align.center(table)
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        table.add_column('Part', justify='center', style='cyan', no_wrap=True)
        table.add_column('Result', justify='center', no_wrap=True)
        table.add_column('Time', justify='center', no_wrap=True)

        for (p1_mine, p1_time), p1_their in p1_pairs:
            table.add_row('A', _format_result(p1_mine, p1_their), f'{p1_time}ms')

        for (p2_mine, p2_time), p2_their in p2_pairs:
            table.add_row('B', _format_result(p2_mine, p2_their), f'{p2_time}ms')

    return table


def main(
    p1: Callable[[str], int], p2: Callable[[str], int], p1_theirs: list[int], p2_theirs: list[int]
):
    year, day, path = sys.argv[1:]

    p1_mines = []
    p2_mines = []
    i = 1
    while True:
        example_path = path + f'/example-{i}.txt'
        if not os.path.exists(example_path):
            break
        with open(example_path) as f:
            example_input = f.read()
        p1_mines.append(timeit(lambda: p1(str(i), example_input)))
        p2_mines.append(timeit(lambda: p2(str(i), example_input)))
        i += 1

    with open(path + '/input.txt') as f:
        input = f.read()

    print('Real:')
    if [p[0] for p in p1_mines] == p1_theirs:
        p1_answer, p1_duration = timeit(lambda: p1('real', input))
        aocd.submit(p1_answer, part='a', day=int(day), year=int(year))
    else:
        p1_answer, p1_duration = 'Skipped', ''
    if [p[0] for p in p2_mines] == p2_theirs:
        p2_answer, p2_duration = timeit(lambda: p2('real', input))
        aocd.submit(p2_answer, part='b', day=int(day), year=int(year))
    else:
        p2_answer, p2_duration = 'Skipped', ''
    p1_mines.append((p1_answer, p1_duration))
    p2_mines.append((p2_answer, p2_duration))
    p1_theirs.append(None)
    p2_theirs.append(None)
    _print_rich(zip(p1_mines, p1_theirs), zip(p2_mines, p2_theirs))


def runs(cases: Annotated[set[str], '(Example input) 1, 2, 3, etc.']):
    def inner(f):
        @wraps(f)
        def wrapper(case, *args, **kwargs):
            return f(*args, **kwargs, case=case) if case in cases | {'real'} else None

        return wrapper

    return inner


def timeit(f):
    start = time.perf_counter()
    result = f()
    end = time.perf_counter()

    return result, f'{(end - start) * 1000:.2f}'
