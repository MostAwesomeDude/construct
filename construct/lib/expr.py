#
# The 'this' expression (backported from construct3).
#
import operator


class ExprMixin(object):
    __slots__ = ()
    def __add__(self, other):
        return BinExpr(operator.add, self, other, "+")
    def __sub__(self, other):
        return BinExpr(operator.sub, self, other, "-")
    def __mul__(self, other):
        return BinExpr(operator.mul, self, other, "*")
    def __floordiv__(self, other):
        return BinExpr(operator.div, self, other, "//")
    def __truediv__(self, other):
        return BinExpr(operator.div, self, other, "/")
    __div__ = __floordiv__
    def __mod__(self, other):
        return BinExpr(operator.mod, self, other, "%")
    def __pow__(self, other):
        return BinExpr(operator.pow, self, other, "**")
    def __xor__(self, other):
        return BinExpr(operator.xor, self, other, "^")
    def __rshift__(self, other):
        return BinExpr(operator.rshift, self, other, ">>")
    def __lshift__(self, other):
        return BinExpr(operator.rshift, self, other, "<<")
    def __and__(self, other):
        return BinExpr(operator.and_, self, other, "and")
    def __or__(self, other):
        return BinExpr(operator.or_, self, other, "or")
    
    def __radd__(self, other):
        return BinExpr(operator.add, other, self, "+")
    def __rsub__(self, other):
        return BinExpr(operator.sub, other, self, "-")
    def __rmul__(self, other):
        return BinExpr(operator.mul, other, self, "*")
    def __rfloordiv__(self, other):
        return BinExpr(operator.div, other, self, "//")
    def __rtruediv__(self, other):
        return BinExpr(operator.div, other, self, "/")
    __rdiv__ = __rfloordiv__
    def __rmod__(self, other):
        return BinExpr(operator.mod, other, self, "%")
    def __rpow__(self, other):
        return BinExpr(operator.pow, other, self, "**")
    def __rxor__(self, other):
        return BinExpr(operator.xor, other, self, "^")
    def __rrshift__(self, other):
        return BinExpr(operator.rshift, other, self, ">>")
    def __rlshift__(self, other):
        return BinExpr(operator.rshift, other, self, "<<")
    def __rand__(self, other):
        return BinExpr(operator.and_, other, self, "and")
    def __ror__(self, other):
        return BinExpr(operator.or_, other, self, "or")

    def __neg__(self):
        return UniExpr(operator.neg, self, "-")
    def __pos__(self):
        return UniExpr(operator.pos, self, "+")
    def __invert__(self):
        return UniExpr(operator.not_, self, "not")
    __inv__ = __invert__
    
    def __contains__(self, other):
        return BinExpr(operator.contains, self, other, "in")
    def __gt__(self, other):
        return BinExpr(operator.gt, self, other, ">")
    def __ge__(self, other):
        return BinExpr(operator.ge, self, other, ">=")
    def __lt__(self, other):
        return BinExpr(operator.lt, self, other, "<")
    def __le__(self, other):
        return BinExpr(operator.le, self, other, "<=")
    def __eq__(self, other):
        return BinExpr(operator.eq, self, other, "==")
    def __ne__(self, other):
        return BinExpr(operator.ne, self, other, "!=")


class UniExpr(ExprMixin):
    __slots__ = ["op", "operand", "opname"]
    def __init__(self, op, operand, opname):
        self.op = op
        self.opname = opname
        self.operand = operand
    def __repr__(self):
        return "%s %r" % (self.lhs, self.opname, self.rhs)
    def __call__(self, context):
        operand = self.operand(context) if callable(self.operand) else self.operand
        return self.op(operand)


class BinExpr(ExprMixin):
    __slots__ = ["op", "lhs", "rhs", "opname"]
    def __init__(self, op, lhs, rhs, opname):
        self.op = op
        self.opname = opname
        self.lhs = lhs
        self.rhs = rhs
    def __repr__(self):
        return "(%r %s %r)" % (self.lhs, self.opname, self.rhs)
    def __call__(self, context):
        lhs = self.lhs(context) if callable(self.lhs) else self.lhs
        rhs = self.rhs(context) if callable(self.rhs) else self.rhs
        return self.op(lhs, rhs)


class Path(ExprMixin):
    __slots__ = ["__name", "__parent"]
    def __init__(self, name, parent = None):
        self.__name = name
        self.__parent = parent
    def __repr__(self):
        if self.__parent is None:
            return self.__name
        return "%r.%s" % (self.__parent, self.__name)
    def __call__(self, context):
        if self.__parent is None:
            return context
        context2 = self.__parent(context)
        return context2[self.__name]
    def __getattr__(self, name):
        return Path(name, self)


# let the magic begin!
this = Path("this")


if __name__ == "__main__":
    x = (this.foo * 2 + 3 << 2) % 11
    print x
    print x({"foo" : 7})




