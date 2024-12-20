import contextlib
import io
import sys
import threading
import time
import tomllib
from collections.abc import Callable
from dataclasses import dataclass

import aocd
from rich.align import Align
from rich.live import Live
from rich.table import Table

CHECK = '\u2713'
X = '\u2717'
TOO_LOW = '(too low)'
TOO_HIGH = '(too high)'
COWARD = 'coward'

interval = None
table_rows: list['Row'] = []


@dataclass
class Row:
    part: str
    result: str
    time: str | None

    def __post_init__(self):
        self.start = time.perf_counter()

    @property
    def get_time(self) -> str:
        return self.time or f'{int(time.perf_counter() - self.start):,}s'


@dataclass
class SetInterval:
    interval: int
    action: Callable

    def __post_init__(self):
        self.stop_event = threading.Event()
        thread = threading.Thread(target=self.__set_interval)
        thread.start()

    def __set_interval(self):
        self.action()

        next_time = time.time() + self.interval
        while not self.stop_event.wait(next_time - time.time()):
            next_time += self.interval
            self.action()

    def cancel(self):
        self.stop_event.set()


def _format_correct(result: str) -> str:
    return f'[green]{result}[/green]'


def _format_incorrect(result: str) -> str:
    return f'[red]{result}[/red]'


def _format_skipped(result: str) -> str:
    return f'[yellow]{result}[/yellow]'


def _format_result(result: int, expected: int | str) -> str:
    if expected == CHECK:
        return _format_correct(f'{result} {expected}')
    if expected in {X, TOO_LOW, TOO_HIGH}:
        return _format_incorrect(f'{result} {expected}')

    return (
        _format_correct(result)
        if result == expected
        else (
            _format_skipped(result)
            if expected is None or expected == COWARD
            else f'{_format_incorrect(result)} != {_format_correct(expected)}'
        )
    )


def _add_placeholder_row(live: Live, part: str):
    global interval
    table_rows.append(Row(part, '?', None))
    interval = SetInterval(1, lambda: _gen_table(live))


def _replace_row(live: Live, part: str, mine: str, theirs: str, time: str):
    global interval
    interval.cancel()
    table_rows[-1] = Row(part, _format_result(mine, theirs), time)
    _gen_table(live)


def _gen_table(live: Live):
    table = Table(show_footer=False)
    table.add_column('Part', justify='left', style='cyan', no_wrap=True)
    table.add_column('Result', justify='left', no_wrap=True)
    table.add_column('Time', justify='left', no_wrap=True)

    for row in table_rows:
        table.add_row(row.part, row.result, row.get_time)

    live.update(Align.center(table))


def main(p1: Callable[[str], int], p2: Callable[[str], int]):
    global table_rows

    year, day, input_path = sys.argv[1:]

    with open(input_path, 'rb') as f:
        data = tomllib.load(f)

    with Live() as live:
        p1_mines, p2_mines = [], []
        p1_theirs, p2_theirs = [], []
        for i, example in enumerate(data.get('examples', []), start=1):
            p1_example = example.get('p1')
            p2_example = example.get('p2')
            if p1_example:
                _add_placeholder_row(live, f'1 (example {i})')
                p1_answer, p1_time = run(p1, example['input'], p1_example)
                p1_mines.append(p1_answer)
                p1_theirs.append(p1_example['answer'])
                _replace_row(live, f'1 (example {i})', p1_answer, p1_example['answer'], p1_time)
            if p2_example:
                _add_placeholder_row(live, f'2 (example {i})')
                p2_answer, p2_time = run(p2, example['input'], p2_example)
                p2_mines.append(p2_answer)
                p2_theirs.append(p2_example['answer'])
                _replace_row(live, f'2 (example {i})', p2_answer, p2_example['answer'], p2_time)

        p1_answer, p1_duration = 'Skipped', ''
        p2_answer, p2_duration = 'Skipped', ''
        if p1_theirs and p1_mines == p1_theirs:
            _add_placeholder_row(live, '1 (real)')
            p1_answer, p1_duration = run(p1, data['real']['input'], data['real']['p1'])
            resp = submit(lambda: aocd.submit(p1_answer, part='a', day=int(day), year=int(year)))
            _replace_row(live, '1 (real)', p1_answer, resp, p1_duration)
        if p2_theirs and p2_mines == p2_theirs:
            _add_placeholder_row(live, '2 (real)')
            p2_answer, p2_duration = run(p2, data['real']['input'], data['real']['p2'])
            resp = submit(lambda: aocd.submit(p2_answer, part='b', day=int(day), year=int(year)))
            resp = '(too low)'
            _replace_row(live, '2 (real)', p2_answer, resp, p2_duration)


def run(f, input, data):
    return timeit(lambda: f(input, **data.get('args', {})))


def timeit(f):
    start = time.perf_counter()
    result = f()
    end = time.perf_counter()

    return result, format_time(end - start)


def format_time(time: float) -> str:
    suffix = 's'
    if time < 1:
        time = time * 1000
        suffix = 'ms'

    return f'{time:,.2f}{suffix}'


def format_submit_response(response: str) -> str:
    if "That's the right answer" in response:
        return CHECK
    if 'Your answer is too high' in response:
        return TOO_HIGH
    if 'Your answer is too low' in response:
        return TOO_LOW
    if "That's not the right answer" in response:
        return X

    raise RuntimeError(f'Unexpected response: {response}')


def submit(f: Callable):
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            f()
    except aocd.AocdError:
        resp = COWARD
    else:
        resp = buffer.getvalue()

    return format_submit_response(resp)
