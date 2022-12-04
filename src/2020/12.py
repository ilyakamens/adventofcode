#!/usr/bin/env python

"""https://adventofcode.com/2020/day/12."""

from math import cos, radians, sin
import os


def iter_instructions(instructions):
    for instruction in instructions:
        yield instruction[0], int(instruction[1:])


def get_direction(degrees):
    return round(sin(radians(degrees))), round(cos(radians(degrees)))


def rotate_wp(degrees, x, y):
    degrees = degrees % 360

    if degrees == 0:
        return x, y
    if degrees == 90:
        return y, -x
    if degrees == 180:
        return -x, -y
    if degrees == 270:
        return -y, x


if __name__ == "__main__":
    with open(os.path.join("input", "12.txt")) as f:
        instructions = f.read().splitlines()

    sx, sy = 0, 0
    degrees = 90
    dx, dy = get_direction(degrees)

    for action, value in iter_instructions(instructions):
        if action == "N":
            sy += value
        elif action == "E":
            sx += value
        elif action == "S":
            sy -= value
        elif action == "W":
            sx -= value
        elif action == "L":
            degrees -= value
            dx, dy = get_direction(degrees)
        elif action == "R":
            degrees += value
            dx, dy = get_direction(degrees)
        elif action == "F":
            sx += dx * value
            sy += dy * value

    print(f"Part 1: {abs(sx) + abs(sy)}")

    sx, sy = 0, 0
    wpx, wpy = 10, 1

    for action, value in iter_instructions(instructions):
        if action == "N":
            wpy += value
        elif action == "E":
            wpx += value
        elif action == "S":
            wpy -= value
        elif action == "W":
            wpx -= value
        elif action == "L":
            wpx, wpy = rotate_wp(-value, wpx, wpy)
        elif action == "R":
            wpx, wpy = rotate_wp(value, wpx, wpy)
        elif action == "F":
            sx += wpx * value
            sy += wpy * value

    print(f"Part 2: {abs(sx) + abs(sy)}")
