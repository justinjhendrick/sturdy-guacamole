def float_range(start, stop, step):
    val = start
    while val < stop and abs(val - stop) > .00001:
        yield(val)
        val += step