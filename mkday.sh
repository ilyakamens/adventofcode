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

    i = 1
    while True:
        example_path = path + f"/example-{i}.txt"
        if not os.path.exists(example_path):
            break
        with open(example_path) as f:
            lines = [list(l) for l in f.read().splitlines()]
        i += 1

    p1_theirs = None
    p2_theirs = None

    p1_mine = p1(lines)
    p2_mine = p2(lines)

    print("Examples:")
    print(f"Part a (theirs): {p1_theirs}")
    print(f"Part b (theirs): {p2_theirs}")
    print()
    print(f"Part a (mine): {p1_mine}")
    print(f"Part b (mine): {p2_mine}")
    print()
    print()

    with open(path + "/input.txt") as f:
        lines = [list(l) for l in f.read().splitlines()]

    print("Real:")
    if p1_theirs == p1_mine:
        aocd.submit(p1(lines), part="a", day=int(day), year=int(year))
    if p2_theirs == p2_mine:
        aocd.submit(p2(lines), part="b", day=int(day), year=int(year))
EOL
