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

input_day_path = SRC / "input" / args.year / args.day
inputpath = str(input_day_path / "input.txt")
Path(str(input_day_path)).mkdir(parents=True, exist_ok=True)
with open(inputpath, "w") as f:
    f.write(data)

daypath = str(SRC / args.year / args.day) + ".py"
if not os.path.exists(daypath):
    call([str(ROOT / "mkday.sh"), args.year, args.day])
call([daypath, args.year, args.day, inputpath])
