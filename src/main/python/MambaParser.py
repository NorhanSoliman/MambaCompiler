"""
This is the manually defined recursive descent parser, as required by the
project.

Note that my solution is overly complex when handling errors, because I
wanted to just parse what I could and *then* print the tree.  It is much
easier if you print while trying to parse!
"""
from antlr4 import Token
from asts import Program, Block, VariableDeclaration, ProcedureDeclaration, FormalParameters,\
    Statement, AssignmentStatement, ActualParameters, ReturnStatement, IfStatement, WhileStatement,\
    Condition, Expression, Term, Factor, ParenthesisFactor, CallExpression
from MambaLexer import MambaLexer


class MambaParser:
    err = None

    lexer = None
    curToken = None

    def __init__(self, lexer):
        self.lexer = lexer
        self.curToken = lexer.nextToken()

    def error(self):
        if not self.err:
            self.err = "Error: unexpected token '" + self.curToken.text + "'"
        raise Exception(self.err)

    def accept(self, expected):
        if self.curToken.type != expected:
            return False
        self.curToken = self.lexer.nextToken()
        return True

    def expect(self, expected):
        cur = self.curToken
        if self.accept(expected):
            return cur
        self.error()
        return None

    def parseProgram(self):
        if self.err:
            return
        node = Program()
        try:
            node.b = self.parseBlock()
            self.expect(Token.EOF)
        finally:
            return node

    def parseBlock(self):
        if self.err:
            return
        node = Block()
        try:
            while not self.err and self.curToken.type in [MambaLexer.VAR, MambaLexer.PROC, MambaLexer.ID, MambaLexer.RET, MambaLexer.IF, MambaLexer.WHILE]:
                if self.curToken.type == MambaLexer.VAR:
                    node.children.append(self.parseVariableDeclaration())
                elif self.curToken.type == MambaLexer.PROC:
                    node.children.append(self.parseProcedureDeclaration())
                elif self.curToken.type in [MambaLexer.ID, MambaLexer.RET, MambaLexer.IF, MambaLexer.WHILE]:
                    node.children.append(self.parseStatement())
                else:
                    self.error()
        finally:
            return node

    def parseVariableDeclaration(self):
        if self.err:
            return
        node = VariableDeclaration()
        try:
            self.expect(MambaLexer.VAR)
            node.id = self.curToken.text
            self.expect(MambaLexer.ID)
            self.expect(MambaLexer.COLON)
            if self.curToken.type == MambaLexer.ID:
                node.type = self.curToken.text
                self.expect(MambaLexer.ID)
            self.expect(MambaLexer.ASSIGN)
            node.rhs = self.parseExpression()
            if self.curToken.type == MambaLexer.SEMICOLON:
                self.expect(MambaLexer.SEMICOLON)
        finally:
            return node

    def parseProcedureDeclaration(self):
        if self.err:
            return
        node = ProcedureDeclaration()
        try:
            self.expect(MambaLexer.PROC)
            node.id = self.curToken.text
            self.expect(MambaLexer.ID)
            self.expect(MambaLexer.LPAREN)
            if self.curToken.type == MambaLexer.ID:
                node.params = self.parseFormalParameters()
            self.expect(MambaLexer.RPAREN)
            if self.curToken.type == MambaLexer.COLON:
                self.expect(MambaLexer.COLON)
                node.ret = self.curToken.text
                self.expect(MambaLexer.ID)
            node.b = self.parseBlock()
            self.expect(MambaLexer.CORP)
        finally:
            return node

    def parseFormalParameters(self):
        if self.err:
            return
        node = FormalParameters()
        try:
            node.params.append(self.curToken.text)
            self.expect(MambaLexer.ID)
            self.expect(MambaLexer.COLON)
            node.types.append(self.curToken.text)
            self.expect(MambaLexer.ID)
            while not self.err and self.curToken.type == MambaLexer.COMMA:
                self.expect(MambaLexer.COMMA)
                node.params.append(self.curToken.text)
                self.expect(MambaLexer.ID)
                self.expect(MambaLexer.COLON)
                node.types.append(self.curToken.text)
                self.expect(MambaLexer.ID)
        finally:
            return node

    def parseStatement(self):
        if self.err:
            return
        node = Statement()
        try:
            if self.curToken.type == MambaLexer.ID:
                nodeid = self.curToken.text
                self.expect(MambaLexer.ID)
                if self.curToken.type == MambaLexer.ASSIGN:
                    node.assign = self.parseAssignmentStatement(nodeid)
                elif self.curToken.type == MambaLexer.LPAREN:
                    node.call = self.parseCallExpression(nodeid)
                else:
                    self.error()
                if self.curToken.type == MambaLexer.SEMICOLON:
                    self.expect(MambaLexer.SEMICOLON)
            elif self.curToken.type == MambaLexer.RET:
                node.ret = self.parseReturnStatement()
                if self.curToken.type == MambaLexer.SEMICOLON:
                    self.expect(MambaLexer.SEMICOLON)
            elif self.curToken.type == MambaLexer.IF:
                node.ifs = self.parseIfStatement()
                if self.curToken.type == MambaLexer.SEMICOLON:
                    self.expect(MambaLexer.SEMICOLON)
            elif self.curToken.type == MambaLexer.WHILE:
                node.whiles = self.parseWhileStatement()
                if self.curToken.type == MambaLexer.SEMICOLON:
                    self.expect(MambaLexer.SEMICOLON)
            else:
                self.error()
        finally:
            return node

    def parseStatement2(self, nodeid):
        if self.err:
            return
        if self.curToken.type == MambaLexer.ASSIGN:
            return self.parseAssignmentStatement(nodeid)
        if self.curToken.type == MambaLexer.LPAREN:
            return self.parseCallExpression(nodeid)
        self.error()

    def parseAssignmentStatement(self, nodeid):
        if self.err:
            return
        node = AssignmentStatement()
        try:
            node.id = nodeid
            self.expect(MambaLexer.ASSIGN)
            node.e = self.parseExpression()
        finally:
            return node

    def parseReturnStatement(self):
        if self.err:
            return
        node = ReturnStatement()
        try:
            self.expect(MambaLexer.RET)
            node.e = self.parseExpression()
        finally:
            return node

    def parseActualParameters(self):
        if self.err:
            return
        node = ActualParameters()
        try:
            node.params.append(self.parseExpression())
            while not self.err and self.curToken.type == MambaLexer.COMMA:
                self.expect(MambaLexer.COMMA)
                node.params.append(self.parseExpression())
        finally:
            return node

    def parseIfStatement(self):
        if self.err:
            return
        node = IfStatement()
        try:
            self.expect(MambaLexer.IF)
            node.c = self.parseCondition()
            self.expect(MambaLexer.THEN)
            node.t = self.parseStatement()
            self.expect(MambaLexer.ELSE)
            node.f = self.parseStatement()
            self.expect(MambaLexer.FI)
        finally:
            return node

    def parseWhileStatement(self):
        if self.err:
            return
        node = WhileStatement()
        try:
            self.expect(MambaLexer.WHILE)
            node.c = self.parseCondition()
            self.expect(MambaLexer.DO)
            node.s = self.parseStatement()
            self.expect(MambaLexer.END)
        finally:
            return node

    def parseCondition(self):
        if self.err:
            return
        node = Condition()
        try:
            node.lhs = self.parseExpression()
            node.op = self.curToken.text
            if self.curToken.type == MambaLexer.EQ:
                self.expect(MambaLexer.EQ)
            elif self.curToken.type == MambaLexer.NE:
                self.expect(MambaLexer.NE)
            elif self.curToken.type == MambaLexer.LT:
                self.expect(MambaLexer.LT)
            elif self.curToken.type == MambaLexer.LTE:
                self.expect(MambaLexer.LTE)
            elif self.curToken.type == MambaLexer.GT:
                self.expect(MambaLexer.GT)
            elif self.curToken.type == MambaLexer.GTE:
                self.expect(MambaLexer.GTE)
            else:
                self.error()
            node.rhs = self.parseExpression()
        finally:
            return node

    def parseExpression(self):
        if self.err:
            return
        node = Expression()
        try:
            node.t = self.parseTerm()
            if self.curToken.type == MambaLexer.PLUS:
                node.op = self.curToken.text
                self.expect(MambaLexer.PLUS)
                node.e = self.parseExpression()
            elif self.curToken.type == MambaLexer.MINUS:
                node.op = self.curToken.text
                self.expect(MambaLexer.MINUS)
                node.e = self.parseExpression()
        finally:
            return node

    def parseTerm(self):
        if self.err:
            return
        node = Term()
        try:
            node.f = self.parseFactor()
            if self.curToken.type == MambaLexer.MULT:
                node.op = self.curToken.text
                self.expect(MambaLexer.MULT)
                node.t = self.parseTerm()
            elif self.curToken.type == MambaLexer.DIV:
                node.op = self.curToken.text
                self.expect(MambaLexer.DIV)
                node.t = self.parseTerm()
        finally:
            return node

    def parseFactor(self):
        if self.err:
            return
        node = Factor()
        try:
            if self.curToken.type == MambaLexer.ID:
                nodeid = self.curToken.text
                self.expect(MambaLexer.ID)
                if self.curToken.type == MambaLexer.LPAREN:
                    node.call = self.parseCallExpression(nodeid)
                else:
                    node.id = nodeid
            elif self.curToken.type == MambaLexer.NUM_INT:
                node.int = self.curToken.text
                self.expect(MambaLexer.NUM_INT)
            elif self.curToken.type == MambaLexer.NUM_FLOAT:
                node.float = self.curToken.text
                self.expect(MambaLexer.NUM_FLOAT)
            elif self.curToken.type == MambaLexer.STR:
                node.str = self.curToken.text
                self.expect(MambaLexer.STR)
            elif self.curToken.type == MambaLexer.LPAREN:
                node.f = self.parseParenthesisFactor()
            else:
                self.error()
        finally:
            return node

    def parseParenthesisFactor(self):
        if self.err:
            return
        node = ParenthesisFactor()
        try:
            self.expect(MambaLexer.LPAREN)
            node.e = self.parseExpression()
            self.expect(MambaLexer.RPAREN)
        finally:
            return node

    def parseCallExpression(self, nodeid):
        if self.err:
            return
        node = CallExpression()
        node.params = ActualParameters()
        try:
            node.id = nodeid
            self.expect(MambaLexer.LPAREN)
            if self.curToken.type in [MambaLexer.ID, MambaLexer.NUM_INT, MambaLexer.NUM_FLOAT, MambaLexer.LPAREN]:
                node.params = self.parseActualParameters()
            self.expect(MambaLexer.RPAREN)
        finally:
            return node
