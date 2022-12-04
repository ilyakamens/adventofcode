#!/usr/bin/env python

"""https://adventofcode.com/2020/day/4."""

from functools import reduce
import os
import re


def _has_required_fields(passport):
    req_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

    return set(passport.keys()).issuperset(req_fields)


def _valid_byr(passport):
    return len(passport["byr"]) == 4 and 1920 <= int(passport["byr"]) <= 2002


def _valid_iyr(passport):
    return len(passport["iyr"]) == 4 and 2010 <= int(passport["iyr"]) <= 2020


def _valid_eyr(passport):
    return len(passport["eyr"]) == 4 and 2020 <= int(passport["eyr"]) <= 2030


def _valid_hgt(passport):
    hgt = passport["hgt"]
    if "cm" in hgt:
        return 150 <= int(hgt.replace("cm", "")) <= 193
    if "in" in hgt:
        return 59 <= int(hgt.replace("in", "")) <= 76
    return False


def _valid_hcl(passport):
    return re.match(r"^#[a-f0-9]{6,6}$", passport["hcl"]) is not None


def _valid_ecl(passport):
    return passport["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def _valid_pid(passport):
    return re.match(r"^[0-9]{9,9}$", passport["pid"]) is not None


def is_valid(passport, validators):
    passport = {field.split(":")[0]: field.split(":")[1] for field in passport.split(" ")}
    for validator in validators:
        try:
            if not validator(passport):
                return False
        except Exception:
            return False

    return True


part_1_validators = (_has_required_fields,)
part_2_validators = (
    _valid_byr,
    _valid_ecl,
    _valid_eyr,
    _valid_hcl,
    _valid_hgt,
    _valid_iyr,
    _valid_pid,
)

if __name__ == "__main__":
    with open(os.path.join("input", "04.txt")) as f:
        passports = [passport.replace("\n", " ").strip() for passport in f.read().split("\n\n")]

    for i, validators in enumerate((part_1_validators, part_2_validators), start=1):
        num_valid_passports = reduce(
            lambda a, p: a + 1 if is_valid(p, validators) else a, passports, 0
        )
        print(f"Valid passports count (part {i}): {num_valid_passports}")
