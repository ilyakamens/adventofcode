def chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i : i + size]
