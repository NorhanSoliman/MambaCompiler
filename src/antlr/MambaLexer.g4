// reference solution for CS 425/825 projects
lexer grammar MambaLexer;

//
// keywords
//

PROC  : 'proc';
CORP  : 'corp';
VAR   : 'var';
RET   : 'ret';
IF    : 'if';
THEN  : 'then';
ELSE  : 'else';
FI    : 'fi';
WHILE : 'while';
DO    : 'do';
END   : 'end';


//
// separators
//

LPAREN    : '(';
RPAREN    : ')';
COMMA     : ',';
COLON     : ':';
SEMICOLON : ';';


//
// operators
//

MULT   : '*';
DIV    : '/';
PLUS   : '+';
MINUS  : '-';
NE     : '<>';
EQ     : '==';
LT     : '<';
GT     : '>';
LTE    : '<=';
GTE    : '>=';
ASSIGN : '=';


//
// literals
//

NUM_INT
	: [1-9] [0-9]*
	| '0'
	;

NUM_FLOAT
	: NUM_INT '.' [0-9]+
	;


//
// strings
//

STR
	: '"' (~[\\"\r\n] | '\\' [trn\\"])* '"'
	;


//
// identifiers
//

ID
	: [a-zA-Z] [a-zA-Z0-9]*
	;


//
// comments
//
ML_COMMENT
	: '/#' .*? '#/' -> skip
	;

SL_COMMENT
	: '#' .*? [\r\n] -> skip
	;


//
// whitespace
//

WS
	: [ \t\r\n]+ -> skip
	;


// a 'match all' class so there are no lexer errors (parser will signal error)
ERR_CHAR
	: .
	;
