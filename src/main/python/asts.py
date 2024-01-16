class AbstractNode:
    def accept(self, v, *args):
        func = getattr(v, 'visit' + self.__class__.__name__)
        return func(self, *args)


class AbstractVisitor:
    def visitProgram(self, node, *args):
        if node.b:
            return node.b.accept(self, *args)

    def visitBlock(self, node, *args):
        ret = None
        if node.children:
            for n in node.children:
                if n:
                    ret = n.accept(self, *args)
        return ret

    def visitVariableDeclaration(self, node, *args):
        if node.rhs:
            return node.rhs.accept(self, *args)

    def visitProcedureDeclaration(self, node, *args):
        if node.params:
            node.params.accept(self, *args)
        if node.b:
            node.b.accept(self, *args)

    def visitFormalParameters(self, node, *args):
        pass

    def visitStatement(self, node, *args):
        if node.assign:
            return node.assign.accept(self, *args)
        if node.call:
            return node.call.accept(self, *args)
        if node.ret:
            return node.ret.accept(self, *args)
        if node.ifs:
            return node.ifs.accept(self, *args)
        if node.whiles:
            return node.whiles.accept(self, *args)

    def visitAssignmentStatement(self, node, *args):
        if node.e:
            return node.e.accept(self, *args)

    def visitCallExpression(self, node, *args):
        if node.params:
            return node.params.accept(self, *args)

    def visitReturnStatement(self, node, *args):
        if node.e:
            return node.e.accept(self, *args)

    def visitIfStatement(self, node, *args):
        if node.c:
            node.c.accept(self, *args)
        if node.t:
            node.t.accept(self, *args)
        if node.f:
            node.f.accept(self, *args)

    def visitWhileStatement(self, node, *args):
        if node.c:
            node.c.accept(self, *args)
        if node.s:
            node.s.accept(self, *args)

    def visitActualParameters(self, node, *args):
        if node.params:
            for e in node.params:
                if e:
                    e.accept(self, *args)

    def visitCondition(self, node, *args):
        if node.lhs:
            node.lhs.accept(self, *args)
        if node.rhs:
            node.rhs.accept(self, *args)

    def visitExpression(self, node, *args):
        if node.t:
            node.t.accept(self, *args)
        if node.e:
            node.e.accept(self, *args)

    def visitTerm(self, node, *args):
        if node.f:
            node.f.accept(self, *args)
        if node.t:
            node.t.accept(self, *args)

    def visitFactor(self, node, *args):
        if node.f:
            return node.f.accept(self, *args)
        if node.call:
            return node.call.accept(self, *args)

    def visitParenthesisFactor(self, node, *args):
        if node.e:
            return node.e.accept(self, *args)


class ActualParameters(AbstractNode):
    def __init__(self):
        self.params = []


class AssignmentStatement(AbstractNode):
    def __init__(self):
        self.id = None
        self.e = None


class Block(AbstractNode):
    def __init__(self):
        self.children = []


class CallExpression(AbstractNode):
    def __init__(self):
        self.id = None
        self.params = None


class Condition(AbstractNode):
    def __init__(self):
        self.lhs = None
        self.op = None
        self.rhs = None


class Expression(AbstractNode):
    def __init__(self):
        self.t = None
        self.op = None
        self.e = None


class Factor(AbstractNode):
    def __init__(self):
        self.id = None
        self.int = None
        self.float = None
        self.str = None
        self.f = None
        self.call = None


class FormalParameters(AbstractNode):
    def __init__(self):
        self.params = []
        self.types = []


class IfStatement(AbstractNode):
    def __init__(self):
        self.c = None
        self.t = None
        self.f = None


class ParenthesisFactor(AbstractNode):
    def __init__(self):
        self.e = None


class ProcedureDeclaration(AbstractNode):
    def __init__(self):
        self.id = None
        self.params = None
        self.ret = None
        self.b = None


class Program(AbstractNode):
    def __init__(self):
        self.b = None


class ReturnStatement(AbstractNode):
    def __init__(self):
        self.e = None


class Statement(AbstractNode):
    def __init__(self):
        self.assign = None
        self.call = None
        self.ret = None
        self.ifs = None
        self.whiles = None


class Term(AbstractNode):
    def __init__(self):
        self.f = None
        self.op = None
        self.t = None


class VariableDeclaration(AbstractNode):
    def __init__(self):
        self.id = None
        self.type = None
        self.rhs = None


class WhileStatement(AbstractNode):
    def __init__(self):
        self.c = None
        self.s = None
