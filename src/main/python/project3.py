"""
CSCE 425/825 Semester Project
Project 3: Type Checking
Author: Robert Dyer <rdyer@unl.edu>
"""
import sys
from antlr4 import FileStream, InputStream
from MambaLexer import MambaLexer
from MambaParser import MambaParser
from Project3Visitor import Project3Visitor
from syms import SymbolTable


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
        p.accept(Project3Visitor(), SymbolTable(), SymbolTable())
        print('OK')
    except Exception as e:
        print(e)
