def float_range(start, stop, step):
    val = start
    while val < stop and abs(val - stop) > .00001:
        yield(val)
        val += step

def vectors_close(a, b):
    norm_dot = a.dot(b) / (a.length * b.length)
    return abs(1.0 - norm_dot) < .01