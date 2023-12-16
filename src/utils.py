def chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i : i + size]


def rotateleft(matrix):
    return [list(l) for l in list(zip(*matrix))[::-1]]


def rotateright(matrix):
    return [list(l) for l in list(zip(*matrix[::-1]))]
