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


@dataclass
class Runner:
    p1: Callable[[str], int]
    p2: Callable[[str], int]
    input_path: str

    def __post_init__(self):
        self.table_rows = []
        self.live = Live()
        with open(self.input_path, 'rb') as f:
            self.data = tomllib.load(f)

    def __enter__(self):
        self.live.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.live.__exit__(exc_type, exc_val, exc_tb)

    def _add_placeholder_row(self, part: str):
        self.table_rows.append(Row(part, '?', None))
        self.interval = SetInterval(1, self._gen_table)

    def _replace_row(self, part: str, mine: str, theirs: str, time: str):
        self.interval.cancel()
        self.table_rows[-1] = Row(part, _format_result(mine, theirs), time)
        self._gen_table()

    def _gen_table(self):
        table = Table(show_footer=False)
        table.add_column('Part', justify='left', style='cyan', no_wrap=True)
        table.add_column('Result', justify='left', no_wrap=True)
        table.add_column('Time', justify='left', no_wrap=True)

        for row in self.table_rows:
            table.add_row(row.part, row.result, row.get_time)

        self.live.update(Align.center(table))

    def _iter_parts(self):
        p1_mines, p2_mines = [], []
        p1_theirs, p2_theirs = [], []
        for i, (k, f, m, t, p) in enumerate(
            [
                ('p1', self.p1, p1_mines, p1_theirs, 'a'),
                ('p2', self.p2, p2_mines, p2_theirs, 'b'),
            ],
            start=1,
        ):
            yield i, k, f, m, t, p

    def run(self, year: int, day: int):
        for i, k, f, m, t, p in self._iter_parts():
            for j, example in enumerate(self.data.get('examples', []), start=1):
                ex = example.get(k)
                if not ex:
                    continue
                self._add_placeholder_row(f'{k} (example {j})')
                answer, time = timeit(lambda: f(example['input'], **ex.get('args', {})))
                m.append(answer)
                t.append(ex['answer'])
                self._replace_row(f'{k} (example {j})', answer, ex['answer'], time)

        # Use `m` and `t` from above since that has `mine` and `their` answers.
        for i, k, f, _, _, p in self._iter_parts():
            answer, duration = 'Skipped', ''
            if not t or m != t:
                continue
            self._add_placeholder_row(f'{i} (real)')
            real = self.data['real']
            answer, duration = timeit(lambda: f(real['input'], **real[k].get('args', {})))
            resp = submit(lambda: aocd.submit(answer, part=p, day=day, year=year))
            self._replace_row(f'{i} (real)', answer, resp, duration)


def main(p1: Callable[[str], int], p2: Callable[[str], int]):
    year, day, input_path = sys.argv[1:]

    with Runner(p1, p2, input_path) as runner:
        runner.run(int(year), int(day))


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
