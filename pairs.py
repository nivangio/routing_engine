def pairs(seq, close_loop = True):
    i = iter(seq)
    prev = next(i)
    for item in i:
        yield prev, item
        prev = item

    if close_loop:
        yield (seq[-1], seq[0])
