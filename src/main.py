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


def _print_rich(p1_data, p2_data):
    console = Console()
    table = Table(show_footer=False)
    table_centered = Align.center(table)
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        table.add_column('Part', justify='left', style='cyan', no_wrap=True)
        table.add_column('Result', justify='left', no_wrap=True)
        table.add_column('Time', justify='left', no_wrap=True)

        for i, (p1_mine, p1_their, p1_time) in enumerate(p1_data):
            part = '1 (real)' if not p1_their else f'1 (example {i + 1})'
            table.add_row(part, _format_result(p1_mine, p1_their), f'{p1_time}ms')

        for i, (p2_mine, p2_their, p2_time) in enumerate(p2_data):
            part = '2 (real)' if not p2_their else f'2 (example {i + 1})'
            table.add_row(part, _format_result(p2_mine, p2_their), f'{p2_time}ms')

    return table


def main(p1: Callable[[str], int], p2: Callable[[str], int]):
    year, day, input_path = sys.argv[1:]

    with open(input_path, 'rb') as f:
        data = tomllib.load(f)

    p1_times, p2_times = [], []
    p1_mines, p2_mines = [], []
    p1_theirs, p2_theirs = [], []
    for i, example in enumerate(data.get('examples', []), start=1):
        if 'p1' in example['answers']:
            print(f'P1: Example {i}')
            p1_answer, p1_time = run(p1, example)
            p1_times.append(p1_time)
            p1_mines.append(p1_answer)
            p1_theirs.append(example['answers']['p1'])
        if 'p2' in example['answers']:
            print(f'P2: Example {i}')
            p2_answer, p2_time = run(p2, example)
            p2_times.append(p2_time)
            p2_mines.append(p2_answer)
            p2_theirs.append(example['answers']['p2'])

    p1_answer, p1_duration = 'Skipped', ''
    p2_answer, p2_duration = 'Skipped', ''
    if p1_mines == p1_theirs:
        print('P1: Real')
        p1_answer, p1_duration = run(p1, data['real'])
        aocd.submit(p1_answer, part='a', day=int(day), year=int(year))
    if p2_mines == p2_theirs:
        print('P2: Real')
        p2_answer, p2_duration = run(p2, data['real'])
        aocd.submit(p2_answer, part='b', day=int(day), year=int(year))

    p1_times.append(p1_duration)
    p2_times.append(p2_duration)
    p1_mines.append(p1_answer)
    p2_mines.append(p2_answer)
    p1_theirs.append(None)
    p2_theirs.append(None)
    _print_rich(zip(p1_mines, p1_theirs, p1_times), zip(p2_mines, p2_theirs, p2_times))


def run(f, data):
    return timeit(lambda: f(data['input'], **data.get('args', {})))


def timeit(f):
    start = time.perf_counter()
    result = f()
    end = time.perf_counter()

    return result, f'{(end - start) * 1000:.2f}'
