"""
CSCE 425/825 Semester Project
Project 1: Lexical Analysis

Author: Robert Dyer <rdyer@unl.edu>
"""
import sys
from antlr4 import FileStream, InputStream, Token
from MambaLexer import MambaLexer


def main(logger, inputfile=None, inputstr=None):
    if inputfile is not None:
        input_stream = FileStream(inputfile)
    elif inputstr is not None:
        input_stream = InputStream(inputstr)
    else:
        logger.error('must specify either inputfile or inputstr')
        sys.exit(-2)

    lexer = MambaLexer(input_stream)

    while True:
        token = lexer.nextToken()
        if token.type == Token.EOF:
            break

        print(lexer.symbolicNames[token.type])
