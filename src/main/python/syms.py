# NOTE: This is the code from our in-class activity.
# Feel free to modify it as you see fit.


class Binding:
    pass


class IntBinding(Binding):
    def __repr__(self):
        return 'int'

    def __eq__(self, o):
        return isinstance(o, IntBinding)


class FloatBinding(Binding):
    def __repr__(self):
        return 'float'

    def __eq__(self, o):
        return isinstance(o, FloatBinding)


class StrBinding(Binding):
    def __repr__(self):
        return 'string'

    def __eq__(self, o):
        return isinstance(o, StrBinding)


class BoolBinding(Binding):
    def __repr__(self):
        return 'bool'

    def __eq__(self, o):
        return isinstance(o, BoolBinding)


class VoidBinding(Binding):
    def __repr__(self):
        return 'void'

    def __eq__(self, o):
        return isinstance(o, VoidBinding)


class ProcBinding(Binding):
    def __init__(self, params, ret):
        self.params = params
        self.ret = ret

    def __repr__(self):
        return 'proc(' + repr(self.params)[1:-1] + ')' + ' -> ' + repr(self.ret)

    def __eq__(self, o):
        if not isinstance(o, ProcBinding):
            return False
        return self.params == o.params and self.ret == o.ret


class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def __repr__(self):
        if self.parent:
            return repr(self.parent) + ' :: ' + repr(self.bindings)
        return repr(self.bindings)

    def bind(self, name, binding):
        if name in self.bindings:
            raise Exception("name is already bound in this scope")
        self.bindings[name] = binding

    def lookup(self, name, currentOnly=False):
        if name in self.bindings:
            return self.bindings[name]
        if currentOnly or not self.parent:
            return None
        return self.parent.lookup(name)

    def enter(self):
        return SymbolTable(parent=self)

    def exit(self):
        if not self.parent:
            return None
        return self.parent