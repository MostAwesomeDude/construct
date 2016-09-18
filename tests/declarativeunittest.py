import unittest
# import traceback
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
# import sys


def raises(func, *args, **kw):
    try:
        ret = func(*args, **kw)
    except Exception as e:
        return e.__class__
    else:
        return None

