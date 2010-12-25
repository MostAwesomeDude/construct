from construct import *
from construct.text import *


class NodeAdapter(Adapter):
    def __init__(self, factory, subcon):
        Adapter.__init__(self, subcon)
        self.factory = factory
    def _decode(self, obj, context):
        return self.factory(obj)


#===============================================================================
# AST nodes
#===============================================================================
class Node(Container):
    def __init__(self, name, **kw):
        Container.__init__(self)
        self.name = name
        for k, v in kw.iteritems():
            setattr(self, k, v)
    
    def accept(self, visitor):
        return getattr(visitor, "visit_%s" % self.name)(self)

def binop_node(obj):
    lhs, rhs = obj
    if rhs is None:
        return lhs
    else:
        op, rhs = rhs
        return Node("binop", lhs=lhs, op=op, rhs=rhs)

def literal_node(value):
    return Node("literal", value = value)


#===============================================================================
# concrete grammar
#===============================================================================
ws = Whitespace()
term = IndexingAdapter(
    Sequence("term",
        ws, 
        Select("term", 
            NodeAdapter(literal_node, DecNumber("number")), 
            IndexingAdapter(
                Sequence("subexpr", 
                    Literal("("), 
                    LazyBound("expr", lambda: expr), 
                    Literal(")")
                ),
                index = 0
            ),
        ),
        ws,
    ),
    index = 0
)

def OptSeq(name, *args):
    return Optional(Sequence(name, *args))

expr1 = NodeAdapter(binop_node, 
    Sequence("expr1", 
        term,
        OptSeq("rhs",
            CharOf("op", "*/"), 
            LazyBound("rhs", lambda: expr1)
        ),
    )
)

expr2 = NodeAdapter(binop_node, 
    Sequence("expr2", 
        expr1, 
        OptSeq("rhs",
            CharOf("op", "+-"), 
            LazyBound("rhs", lambda: expr2)
        ),
    )
)

expr = expr2


#===============================================================================
# evaluation visitor
#===============================================================================
class EvalVisitor(object):
    def visit_literal(self, obj):
        return obj.value
    def visit_binop(self, obj):
        lhs = obj.lhs.accept(self)
        op = obj.op
        rhs = obj.rhs.accept(self)
        if op == "+":
            return lhs + rhs
        elif op == "-":
            return lhs - rhs
        elif op == "*":
            return lhs * rhs
        elif op == "/":
            return lhs / rhs
        else:
            raise ValueError("invalid op", op)

ev = EvalVisitor()

def myeval(text):
    ast = expr.parse(text)
    print ast
    return ast.accept(ev)


#===============================================================================
# test
#===============================================================================
if __name__ == "__main__":
    print myeval("2*3+4")
    #>>> myeval("2*3+4")
    #Node:
    #    name = 'binop'
    #    rhs = Node:
    #        name = 'literal'
    #        value = 4
    #    lhs = Node:
    #        name = 'binop'
    #        rhs = Node:
    #            name = 'literal'
    #            value = 3
    #        lhs = Node:
    #            name = 'literal'
    #            value = 2
    #        op = '*'
    #    op = '+'
    #10
    
    print "-" * 80
    
    print myeval("2*(3+4)")
    #>>> myeval("2*(3+4)")
    #Node:
    #    name = 'binop'
    #    rhs = Node:
    #        name = 'binop'
    #        rhs = Node:
    #            name = 'literal'
    #            value = 4
    #        lhs = Node:
    #            name = 'literal'
    #            value = 3
    #        op = '+'
    #    lhs = Node:
    #        name = 'literal'
    #        value = 2
    #    op = '*'
    #14
    #>>>

























