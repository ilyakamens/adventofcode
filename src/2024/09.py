#!/usr/bin/env python

"""https://adventofcode.com/2024/day/9."""

from dataclasses import dataclass

from main import main, runs
from utils import LL, Node


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    input = input.strip()

    disk = []
    fileid = 0
    for i, c in enumerate(input):
        is_file = i % 2 == 0
        disk.extend([str(fileid) if is_file else '.'] * int(c))
        fileid += 1 if is_file else 0

    i = 0
    j = len(disk) - 1
    while True:
        while disk[i] != '.':
            i += 1
        while disk[j] == '.':
            j -= 1
        if i >= j:
            break
        disk[i], disk[j] = disk[j], disk[i]
        i += 1
        j -= 1

    return sum(i * int(c) for i, c in enumerate(disk) if c != '.')


@dataclass
class File:
    size: int
    id: int = -1
    moved: bool = False

    @property
    def is_file(self) -> bool:
        return self.id != -1

    @property
    def is_block(self) -> bool:
        return self.id == -1


@dataclass
class Disk:
    items: LL[Node[File]]

    @property
    def checksum(self) -> int:
        checksum = 0

        i = 0
        f: File
        for f in self.items.itervals():
            if f.is_block:
                i += f.size
                continue

            for _ in range(f.size):
                checksum += i * f.id
                i += 1

        return checksum

    def move(self, from_: Node[File], to: Node[File]):
        file, block = from_.val, to.val

        remaining = block.size - file.size
        block.size = file.size
        block.id, file.id = file.id, block.id
        block.moved = True

        if remaining > 0:
            self.items.insert(File(size=remaining), after=to)


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    input = input.strip()

    items = LL[Node[File]]()
    fileid = 0
    for i, c in enumerate(input):
        is_file = i % 2 == 0
        items.append(File(size=int(c), id=fileid if is_file else -1))
        fileid += 1 if is_file else 0

    disk = Disk(items)

    for i, filenode in reversed(list(enumerate(disk.items))):
        file = filenode.val
        if not file.is_file or file.moved:
            continue
        for j, blocknode in enumerate(disk.items):
            if j >= i:
                break
            block = blocknode.val
            if not block.is_block:
                continue
            if block.size >= file.size:
                disk.move(filenode, blocknode)
                break

    return disk.checksum


if __name__ == '__main__':
    main(p1, p2, [1928], [2858])
