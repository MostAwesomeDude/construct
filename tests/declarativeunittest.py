import unittest
import traceback
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys


class TestCase(unittest.TestCase):

    def test_suite_static(self):
        if hasattr(self, "alltests"):
            self.execute(self.alltests)

    def test_suite_from_yields(self):
        if hasattr(self, "alltestsinteractive"):
            self.execute(self.alltestsinteractive())

    def execute(self, tests):
        errors = []
        for i, line in enumerate(tests):

            if len(line) == 1:
                returned = line[0]
                if not returned:
                    errors.append("test #%d" % i)
                    errors.append("returned %r" % returned)

            if len(line) == 2:
                returned, expected = line
                if returned != expected or expected != returned:
                    errors.append("test id #%d" % i)
                    errors.append("returned %r, expected %r" % (returned, expected))

            if len(line) == 3:
                func, args, res, exctype = line
                if type(args) is not tuple:
                    args = (args,)
                try:
                    r = func(*args)
                except:
                    t, ex, tb = sys.exc_info()
                    if exctype is None:
                        errors.append("test id #%d" % i)
                        errors.append("%d::: %s" % (i, "".join(traceback.format_exception(t, ex, tb))))
                        continue
                    if t is not exctype:
                        errors.append("test id #%d" % i)
                        errors.append("%s: raised %r, expected %r" % (func, t, exctype))
                        continue
                else:
                    if exctype is not None:
                        print("Testing: %r", (i, func, args, res, exctype))
                        errors.append("test id #%d" % i)
                        errors.append("%s: expected exception %r" % (func, exctype))
                        continue
                    if r != res:
                        errors.append("test id #%d" % i)
                        errors.append("%s: returned %r, expected %r" % (func, r, res))
                        continue
        if errors:
            self.fail("\n=========================\n".join(str(e) for e in errors))

