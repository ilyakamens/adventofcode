#!/usr/bin/env zsh

if [[ $# -lt 2 ]]; then
    echo "Example usage: ./mkday.sh 2020 01"
    exit 1
fi

pyfile="src/$1/$2.py"

touch $pyfile
chmod a+x $pyfile
cat > $pyfile <<EOL
#!/usr/bin/env python

"""https://adventofcode.com/$1/day/$2."""

import sys

import aocd


def p1(lines):
    pass


def p2(lines):
    pass


if __name__ == "__main__":
    year, day, path = sys.argv[1:]

    with open(path) as f:
        lines = [list(l) for l in f.read().splitlines()]

    aocd.submit(p1(lines), part="a", day=int(day), year=int(year))
    aocd.submit(p2(lines), part="b", day=int(day), year=int(year))
EOL
