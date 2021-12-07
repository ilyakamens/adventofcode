#!/usr/bin/env zsh

if [[ $# -lt 2 ]]; then
    echo "Example usage: ./mkday.sh 2020 01"
    exit 1
fi

pyfile="$1/$2.py"

touch $pyfile "$1/input/$2.txt"
chmod a+x $pyfile
cat > $pyfile <<EOL
#!/usr/bin/env python

"""https://adventofcode.com/$1/day/$2."""

from collections import defaultdict
import os

def p1(lines):
    pass

def p2(lines):
    pass

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "$2.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
EOL
