
def raises(func, *args, **kw):
    try:
        ret = func(*args, **kw)
    except Exception as e:
        return e.__class__
    else:
        return None


def atmostone(*args):
    return sum(int(bool(x)) for x in args) <= 1


def alldifferent(*args):
    return all(i != j and x == y for i,x in enumerate(args) for j,y in enumerate(args))

