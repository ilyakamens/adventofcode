#!/usr/bin/env python

"""https://adventofcode.com/2024/day/9."""

from dataclasses import dataclass

from main import main, runs


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    input = input.strip()

    count = 0
    for c in input:
        count += int(c)

    disk = []
    file = True
    filecount = 0
    for c in input:
        for _ in range(int(c)):
            if file:
                disk.append(str(filecount))
            else:
                disk.append('.')
        if file:
            filecount += 1
        file = not file

    i = 0
    j = len(disk) - 1
    while i < j:
        while disk[i] != '.':
            i += 1
        while disk[j] == '.':
            j -= 1
        if i >= j:
            break
        disk[i], disk[j] = disk[j], disk[i]
        i += 1
        j -= 1

    size = 0
    for i, c in enumerate(disk):
        if c == '.':
            break
        size += i * int(c)

    return size


@dataclass
class File:
    size: int
    id: int = -1


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    input = input.strip()

    count = 0
    for c in input:
        count += int(c)

    disk = []
    file = True
    fileid = 0
    for c in input:
        if file:
            disk.append(File(size=int(c), id=fileid))
            fileid += 1
        else:
            disk.append(File(size=int(c)))
        file = not file

    i = 0
    j = len(disk) - 1
    remaining = 0
    for j in range(len(disk) - 1, 0, -1):
        f1 = disk[j]
        if f1.id == -1:
            continue
        for i, f2 in enumerate(disk):
            if i >= j:
                break
            if f2.id != -1:
                continue
            if f1.size <= f2.size:
                remaining = f2.size - f1.size
                f1.id, f2.id = f2.id, f1.id
                f2.size = f1.size
                break

        if remaining > 0:
            disk.insert(i + 1, File(size=remaining))
            remaining = 0

    size = 0
    i = 0
    for f in disk:
        if f.id == -1:
            i += f.size
            continue

        for _ in range(f.size):
            size += i * f.id
            i += 1

    return size


if __name__ == '__main__':
    main(p1, p2, [1928], [2858])
