#!/usr/bin/env python

"""https://adventofcode.com/2020/day/19."""

import os
import re

if __name__ == "__main__":
    with open(os.path.join("input", "19.txt")) as f:
        rule_lines, messages = [l.split("\n") for l in f.read().split("\n\n")]

    rules = {}
    for rl in rule_lines:
        i, rule = rl.split(": ")
        if rule.startswith('"'):
            rules[i] = rule.replace('"', "")
            continue
        if "|" in rule:
            rule = f"({rule})"
        rules[i] = rule

    # For Part 2; comment out for Part 1.
    rules["8"] = "(42 | 42 8)"
    rules["11"] = "(42 31 | 42 11 31)"

    eight_count = 0
    eleven_count = 0
    master_rule = f"^{rules['0']}$"
    while re.match(".*\d.*", master_rule):
        rule = re.match(".*?(?P<rule>\d+).*?", master_rule).group("rule")
        if rule == "8":
            eight_count += 1
        if rule == "11":
            eleven_count += 1
        if eight_count > 4:
            rules["8"] = "42"
        if eleven_count > 3:
            rules["11"] = "42 31"
        master_rule = master_rule.replace(f" {rule} ", f" {rules[rule]} ")
        master_rule = master_rule.replace(f" {rule})", f" {rules[rule]})")
        master_rule = master_rule.replace(f"({rule} ", f"({rules[rule]} ")
        master_rule = master_rule.replace(f"^{rule} ", f"^{rules[rule]} ")
        master_rule = master_rule.replace(f" {rule}$", f" {rules[rule]}$")
    master_rule = master_rule.replace(" ", "")

    count = len([m for m in messages if re.match(master_rule, m)])
    print(f"Part 1 (and 2): {count}")
