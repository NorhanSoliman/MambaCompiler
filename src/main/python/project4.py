"""
CSCE 425/825 Semester Project
Project 4: Code Generation

Author: Robert Dyer <rdyer@unl.edu>
"""
import sys
from antlr4 import FileStream, InputStream
from MambaLexer import MambaLexer
from MambaParser import MambaParser
from Project3Visitor import Project3Visitor
from Project4Visitor import Project4Visitor
from syms import FloatBinding, IntBinding, ProcBinding, StrBinding, SymbolTable, VoidBinding


def main(logger, inputfile=None, inputstr=None):
    if inputfile is not None:
        input_stream = FileStream(inputfile)
    elif inputstr is not None:
        input_stream = InputStream(inputstr)
    else:
        logger.error('must specify either inputfile or inputstr')
        sys.exit(-2)

    lexer = MambaLexer(input_stream)
    parser = MambaParser(lexer)
    p = parser.parseProgram()

    if parser.err:
        print(parser.err)
        sys.exit(-3)

    try:
        # add the built-in/global functions
        ft = SymbolTable()
        ft.bind('out', ProcBinding([StrBinding()], VoidBinding()))
        ft.bind('int', ProcBinding([FloatBinding()], IntBinding()))
        ft.bind('float', ProcBinding([IntBinding()], FloatBinding()))
        ft.bind('string', ProcBinding([FloatBinding()], StrBinding()))

        p.accept(Project3Visitor(), ft, SymbolTable())
    except Exception as e:
        print(e)
        sys.exit(-4)

    try:
        print(p.accept(Project4Visitor()))
    except Exception as e:
        print(e)
        sys.exit(-5)