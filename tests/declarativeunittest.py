
def raises(func, *args, **kw):
    try:
        func(*args, **kw)
        return None
    except Exception as e:
        return e.__class__


def atmostone(*args):
    return sum(1 for x in args if x) <= 1
