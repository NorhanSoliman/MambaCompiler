#!/bin/sh

export CLASSPATH=".:\"$(pwd)/lib/antlr-4.13.0-complete.jar\":$CLASSPATH"
alias antlr4="java -jar \"$(pwd)/lib/antlr-4.13.0-complete.jar\""

antlr4 -Dlanguage=Python3 src/antlr/MambaLexer.g4 -o gen
