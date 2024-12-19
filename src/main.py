import sys
import time
import tomllib
from collections.abc import Callable

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


def _add_row(table: Table, part: str, mine: str, theirs: str, time: str):
    table.add_row(part, _format_result(mine, theirs), f'{time}ms')


def main(p1: Callable[[str], int], p2: Callable[[str], int]):
    year, day, input_path = sys.argv[1:]

    with open(input_path, 'rb') as f:
        data = tomllib.load(f)

    table = Table(show_footer=False)
    table.add_column('Part', justify='left', style='cyan', no_wrap=True)
    table.add_column('Result', justify='left', no_wrap=True)
    table.add_column('Time', justify='left', no_wrap=True)
    with Live(Align.center(table), console=Console(), screen=False, refresh_per_second=20):
        p1_mines, p2_mines = [], []
        p1_theirs, p2_theirs = [], []
        for i, example in enumerate(data.get('examples', []), start=1):
            if 'p1' in example['answers']:
                p1_answer, p1_time = run(p1, example)
                p1_mines.append(p1_answer)
                p1_theirs.append(example['answers']['p1'])
                _add_row(table, f'1 (example {i})', p1_answer, example['answers']['p1'], p1_time)
            if 'p2' in example['answers']:
                p2_answer, p2_time = run(p2, example)
                p2_mines.append(p2_answer)
                p2_theirs.append(example['answers']['p2'])
                _add_row(table, f'2 (example {i})', p2_answer, example['answers']['p2'], p2_time)

        p1_answer, p1_duration = 'Skipped', ''
        p2_answer, p2_duration = 'Skipped', ''
        if p1_theirs and p1_mines == p1_theirs:
            p1_answer, p1_duration = run(p1, data['real'])
            aocd.submit(p1_answer, part='a', day=int(day), year=int(year))
            _add_row(table, '1 (real)', p1_answer, None, p1_duration)
        if p2_theirs and p2_mines == p2_theirs:
            p2_answer, p2_duration = run(p2, data['real'])
            aocd.submit(p2_answer, part='b', day=int(day), year=int(year))
            _add_row(table, '2 (real)', p2_answer, None, p2_duration)


def run(f, data):
    return timeit(lambda: f(data['input'], **data.get('args', {})))


def timeit(f):
    start = time.perf_counter()
    result = f()
    end = time.perf_counter()

    return result, f'{(end - start) * 1000:.2f}'
