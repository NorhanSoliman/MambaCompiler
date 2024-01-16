from asts import AbstractVisitor


class Project2Visitor(AbstractVisitor):
    indent = 0

    def printIndent(self):
        for i in range(self.indent):
            print("    ", end='')

    def visitProgram(self, node, arg):
        self.printIndent()
        print("Program")
        self.indent += 1
        super().visitProgram(node, arg)
        self.indent -= 1

    def visitBlock(self, node, arg):
        self.printIndent()
        print("Block")
        self.indent += 1
        super().visitBlock(node, arg)
        self.indent -= 1

    def visitDeclaration(self, node, arg):
        self.printIndent()
        print("Declaration")
        self.indent += 1
        super().visitDeclaration(node, arg)
        self.indent -= 1

    def visitVariableDeclaration(self, node, arg):
        self.printIndent()
        print("VariableDeclaration")
        self.indent += 1
        super().visitVariableDeclaration(node, arg)
        self.indent -= 1

    def visitProcedureDeclaration(self, node, arg):
        self.printIndent()
        print("ProcedureDeclaration")
        self.indent += 1
        super().visitProcedureDeclaration(node, arg)
        self.indent -= 1

    def visitFormalParameters(self, node, arg):
        self.printIndent()
        print("FormalParameters")
        self.indent += 1
        super().visitFormalParameters(node, arg)
        self.indent -= 1

    def visitStatement(self, node, arg):
        self.printIndent()
        print("Statement")
        self.indent += 1
        super().visitStatement(node, arg)
        self.indent -= 1

    def visitAssignmentStatement(self, node, arg):
        self.printIndent()
        print("AssignmentStatement")
        self.indent += 1
        super().visitAssignmentStatement(node, arg)
        self.indent -= 1

    def visitReturnStatement(self, node, arg):
        self.printIndent()
        print("ReturnStatement")
        self.indent += 1
        super().visitReturnStatement(node, arg)
        self.indent -= 1

    def visitIfStatement(self, node, arg):
        self.printIndent()
        print("IfStatement")
        self.indent += 1
        super().visitIfStatement(node, arg)
        self.indent -= 1

    def visitWhileStatement(self, node, arg):
        self.printIndent()
        print("WhileStatement")
        self.indent += 1
        super().visitWhileStatement(node, arg)
        self.indent -= 1

    def visitActualParameters(self, node, arg):
        self.printIndent()
        print("ActualParameters")
        self.indent += 1
        super().visitActualParameters(node, arg)
        self.indent -= 1

    def visitCondition(self, node, arg):
        self.printIndent()
        print("Condition")
        self.indent += 1
        super().visitCondition(node, arg)
        self.indent -= 1

    def visitExpression(self, node, arg):
        self.printIndent()
        print("Expression")
        self.indent += 1
        super().visitExpression(node, arg)
        self.indent -= 1

    def visitTerm(self, node, arg):
        self.printIndent()
        print("Term")
        self.indent += 1
        super().visitTerm(node, arg)
        self.indent -= 1

    def visitFactor(self, node, arg):
        self.printIndent()
        print("Factor")
        self.indent += 1
        super().visitFactor(node, arg)
        self.indent -= 1

    def visitParenthesisFactor(self, node, arg):
        self.printIndent()
        print("ParenthesisFactor")
        self.indent += 1
        super().visitParenthesisFactor(node, arg)
        self.indent -= 1

    def visitCallExpression(self, node, arg):
        self.printIndent()
        print("CallExpression")
        self.indent += 1
        super().visitCallExpression(node, arg)
        self.indent -= 1
