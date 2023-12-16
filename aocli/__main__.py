import argparse
from datetime import datetime
import os
from pathlib import Path
from subprocess import call

from aocd import get_data

ROOT = Path(__file__).parent.parent.resolve()
SRC = ROOT / "src"

os.environ["PYTHONPATH"] = str(SRC)

parser = argparse.ArgumentParser(prog="aocli", description="CLI for AoC solutions.")
parser.add_argument("year", action="store", default=datetime.now().year, type=str)
parser.add_argument("day", action="store", default=datetime.now().day, type=str)

args = parser.parse_args()

data = get_data(year=args.year, day=int(args.day))

root_input_path = SRC / "input" / args.year / args.day
input_path = str(root_input_path / "input.txt")
Path(str(root_input_path)).mkdir(parents=True, exist_ok=True)
with open(input_path, "w") as f:
    f.write(data)
example_path = str(root_input_path / "example-1.txt")
if not os.path.exists(example_path):
    open(example_path, "w").close()

daypath = str(SRC / args.year / args.day) + ".py"
if not os.path.exists(daypath):
    call([str(ROOT / "mkday.sh"), args.year, args.day])
call([daypath, args.year, args.day, root_input_path])
