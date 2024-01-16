from asts import AbstractVisitor
from syms import VoidBinding, BoolBinding, IntBinding, FloatBinding, StrBinding, ProcBinding, SymbolTable

def getname(node):
    return node.id

def getTypeBinding(t):
    if t is None:
        return VoidBinding()
    if t == 'int':
        return IntBinding()
    if t == 'float':
        return FloatBinding()
    if t == 'bool':
        return BoolBinding()
    if t == 'string':
        return StrBinding()
    typeCheckError("Unknown type: " + t)

def typeCheckError(err):
    raise Exception(err)


class ProcFindingVisitor(AbstractVisitor):
    def visitProcedureDeclaration(self, node, *args):
        ft = args[0]

        ID1 = getname(node)
        # If it already exists *in the current scope* then error(ID1 + “ already exists”)
        if ft.lookup(ID1):
            typeCheckError(f'procedure {ID1} already exists')

        types = []
        if node.params:
            types = node.params.accept(self)
        retType = getTypeBinding(node.ret)

        ft.bind(node.id, ProcBinding(types, retType))

    def visitFormalParameters(self, node, *args):
        return [getTypeBinding(t) for t in node.types]


class Project3Visitor(AbstractVisitor):
    def visitProgram(self, node, *args):
        # Create empty symbol tables (created by the caller)
        # Return the block’s type
        return super().visitProgram(node, *args)

    def visitBlock(self, node, *args):
        ft, vt = args
        # Enter new scopes
        ft = ft.enter()
        vt = vt.enter()
        # Collect all the function types first
        node.accept(ProcFindingVisitor(), ft)
        # Check each declaration/statement, in order
        lastType = super().visitBlock(node, ft, vt)
        # Exit back to original scopes
        ft = ft.exit()
        vt = vt.exit()
        # Return the type of the last thing checked
        return lastType

    def visitVariableDeclaration(self, node, *args):
        ft, vt = args
        # First look up ID1
        ID1 = getname(node)
        # Ensure the name ID1 is not a type name else error(“cannot use reserved name '” + ID1 + “'”)
        if ID1 in ['int', 'float', 'string']:
            typeCheckError(f'cannot use reserved name {ID1}')
        idtype = vt.lookup(ID1, True)
        # If it already exists *in the current scope* then error(ID1 + “ already exists”)
        if idtype:
            typeCheckError(f'{ID1} already exists')
        # Get the type of the expression
        rhs = node.rhs.accept(self, *args)
        # If they gave a type ID2, make sure it matches otherwise error(“cannot assign expression of type “ + exprType + ” to a variable of type ” + ID2)
        if node.type:
            t = getTypeBinding(node.type)
            if t != rhs:
                typeCheckError(f'cannot assign expression of type {rhs} to a variable of type {t}')
        # Bind the variable to the type
        vt.bind(ID1, rhs)
        # Return the type
        return rhs

    def visitProcedureDeclaration(self, node, *args):
        ft, vt = args
        # Enter new scopes
        ft = ft.enter()
        vt = vt.enter()
        # Ensure the name ID1 is not a type name else error(“cannot use reserved name '” + ID1 + “'”)
        ID1 = getname(node)
        if ID1 in ['int', 'float', 'string']:
            typeCheckError(f'cannot use reserved name {ID1}')
        proc = ft.lookup(ID1)
        if node.params:
            node.params.accept(self, ft, vt)
        # Check the block
        node.b.accept(self, ft, vt)
        # Exit back to original scopes
        ft = ft.exit()
        vt = vt.exit()
        # Return the function’s type
        return proc

    def visitFormalParameters(self, node, *args):
        ft, vt = args
        node.vt = vt
        
        # Ensure none of the names ID1 are a type name else error(“cannot use reserved name '” + ID1 + “'”)
        for id in node.params:
            if id in ['int', 'float', 'string']:
                typeCheckError(f'cannot use reserved name {id}')
        # Return a list/tuple oبf each type
        types = []
        for i in range(0, len(node.params)):
            t = getTypeBinding(node.types[i])
            vt.bind(node.params[i], t)
            types.append(t)
        return types

    def visitAssignmentStatement(self, node, *args):
        ft, vt = args
        node.vt = vt ##
        # Look up the ID, if it does not exist then error(ID + " undeclared")
        ID = getname(node)
        t = vt.lookup(ID)
        if not t:
            typeCheckError(f'{ID} undeclared')
        # Get the type of the expression
        rhs = node.e.accept(self, *args)
        # If the two types do not match, then error(ID + " has type " + t1 + " but trying to assign type " + t2)
        if t != rhs:
            typeCheckError(f'{ID} has type {t} but trying to assign type {rhs}')
        # Otherwise return the type
        return t

    def visitCallExpression(self, node, *args):
        ft, vt = args
        # Lookup the function, if it does not exist then error(ID + " not a procedure")
        ID = getname(node)
        proc = ft.lookup(ID)
        if not proc:
            typeCheckError(f'{ID} not a procedure')
        # Otherwise check the argument types
        argtypes = node.params.accept(self, *args)
        # If the number of arguments does not match the number of parameters, then error("procedure " + ID + " requires " + len(params) + " parameters but given " + len(args))
        if len(argtypes) != len(proc.params):
            typeCheckError(f'procedure {ID} requires {len(proc.params)} parameters but given {len(argtypes)}')
        # Then check each argument type matches its parameter, if one does not then error("argument type does not match")
        for i in range(0, len(proc.params)):
            if argtypes[i] != proc.params[i]:
                typeCheckError('argument type does not match')
        # Finally return the proc’s return type
        return proc.ret

    def visitIfStatement(self, node, *args):
        # Check everything
        t = node.c.accept(self, *args)
        # Ensure condition is bool
        # Else error("condition must be boolean")
        if not isinstance(t, BoolBinding):
            typeCheckError('condition must be boolean')
        node.t.accept(self, *args)
        # Return type of Statement2
        return node.f.accept(self, *args)

    def visitWhileStatement(self, node, *args):
        # Check everything
        t = node.c.accept(self, *args)
        # Ensure condition is bool
        # Else error("condition must be boolean")
        if not isinstance(t, BoolBinding):
            typeCheckError('condition must be boolean')
        # Return type of Statement
        return node.s.accept(self, *args)

    def visitActualParameters(self, node, *args):
        # Check each expression
        types = []
        for e in node.params:
            types.append(e.accept(self, *args))
        # Return a list/tuple of their types
        return types

    def visitCondition(self, node, *args):
        # Check both sides
        lhs = node.lhs.accept(self, *args)
        rhs = node.rhs.accept(self, *args)
        # Ensure they are the same type and return bool
        if lhs != rhs:
        # Else error("operands not same type")
            typeCheckError('operands not same type')
        return BoolBinding()

    def visitExpression(self, node, *args):
        # Check both sides
        lhs = node.t.accept(self, *args)
        if node.e:
            rhs = node.e.accept(self, *args)
        # Ensure they are the same type and return it
            if lhs != rhs:
        # Else error("operands not same type")
                typeCheckError('operands not same type')
        # if the type is not int or float then error(“unsupported operand type for “ + OP)
            if not isinstance(lhs, (IntBinding, FloatBinding)):
                typeCheckError(f'unsupported operand type for {node.op}')
        return lhs

    def visitTerm(self, node, *args):
        # Check both sides
        lhs = node.f.accept(self, *args)
        if node.t:
            rhs = node.t.accept(self, *args)
        # Ensure they are the same type and return it
            if lhs != rhs:
        # Else error("operands not same type")
                typeCheckError('operands not same type')
        # if the type is not int or float then error(“unsupported operand type for “ + OP)
            if not isinstance(lhs, (IntBinding, FloatBinding)):
                typeCheckError(f'unsupported operand type for {node.op}')
        return lhs

    def visitFactor(self, node, *args):
        ft, vt = args
        node.vt = vt
        if node.f:
            return node.f.accept(self, *args)
        if node.call:
            return node.call.accept(self, *args)
        if node.id:
            ID = getname(node)
            # Look up the variable name
            t = vt.lookup(ID)
            # If not declared error(getname(ID) + " undeclared")
            if not t:
                typeCheckError(f'{ID} undeclared')
            # Else return its type
            return t
        if node.int:
            return IntBinding()
        if node.float:
            return FloatBinding()
        if node.str:
            return StrBinding()
