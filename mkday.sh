#!/usr/bin/env zsh

# https://stackoverflow.com/a/11130324/814589

if [[ $# -lt 2 ]]; then
    echo "Example usage: ./mkday.sh 2020 01"
    exit 1
fi

mkdir -p src/$1

pyfile="src/$1/$2.py"

touch $pyfile
chmod a+x $pyfile
cat > $pyfile <<EOL
#!/usr/bin/env python

"""https://adventofcode.com/$1/day/$((10#$2))."""

from main import main, runs


def p1(input: str) -> int:
    pass


def p2(input: str) -> int:
    pass


if __name__ == '__main__':
    main(p1, p2)
EOL
