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
    table.add_row(part, _format_result(mine, theirs), time)


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
            p1_example = example.get('p1')
            p2_example = example.get('p2')
            if p1_example:
                p1_answer, p1_time = run(p1, example['input'], p1_example)
                p1_mines.append(p1_answer)
                p1_theirs.append(p1_example['answer'])
                _add_row(table, f'1 (example {i})', p1_answer, p1_example['answer'], p1_time)
            if p2_example:
                p2_answer, p2_time = run(p2, example['input'], p2_example)
                p2_mines.append(p2_answer)
                p2_theirs.append(p2_example['answer'])
                _add_row(table, f'2 (example {i})', p2_answer, p2_example['answer'], p2_time)

        p1_answer, p1_duration = 'Skipped', ''
        p2_answer, p2_duration = 'Skipped', ''
        if p1_theirs and p1_mines == p1_theirs:
            p1_answer, p1_duration = run(p1, data['real']['input'], data['real']['p1'])
            aocd.submit(p1_answer, part='a', day=int(day), year=int(year))
            _add_row(table, '1 (real)', p1_answer, None, p1_duration)
        if p2_theirs and p2_mines == p2_theirs:
            p2_answer, p2_duration = run(p2, data['real']['input'], data['real']['p2'])
            aocd.submit(p2_answer, part='b', day=int(day), year=int(year))
            _add_row(table, '2 (real)', p2_answer, None, p2_duration)


def run(f, input, data):
    return timeit(lambda: f(input, **data.get('args', {})))


def timeit(f):
    start = time.perf_counter()
    result = f()
    end = time.perf_counter()

    diff = end - start
    if diff < 1:
        diff = diff * 1000
        suffix = 'ms'
    else:
        suffix = 's'

    return result, f'{diff:,.2f}{suffix}'
