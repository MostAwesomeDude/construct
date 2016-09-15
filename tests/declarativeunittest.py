import unittest
import traceback
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys


class TestCase(unittest.TestCase):

    def test_suite(self):
        errors = []
        for i, (func, args, res, exctype) in enumerate(self.alltests):
            if type(args) is not tuple:
                args = (args,)
            try:
                r = func(*args)
            except:
                t, ex, tb = sys.exc_info()
                if exctype is None:
                    errors.append("%d::: %s" % (i, "".join(traceback.format_exception(t, ex, tb))))
                    continue
                if t is not exctype:
                    errors.append("%s: raised %r, expected %r" % (func, t, exctype))
                    continue
            else:
                if exctype is not None:
                    print("Testing: %r", (i, func, args, res, exctype))
                    errors.append("%s: expected exception %r" % (func, exctype))
                    continue
                if r != res:
                    errors.append("%s: returned %r, expected %r" % (func, r, res))
                    continue
        if errors:
            self.fail("\n=========================\n".join(str(e) for e in errors))

