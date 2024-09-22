// java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor Luppolo.g4

grammar Luppolo;

program: function+ EOF;

function: ID LROUND (ID (COMMA ID)*)? RROUND block;

block: LCURLY instruction* RCURLY;

instruction
    : ID ASSIGN expression           # declarationInstruction
    | FOREACH ID IN expression block # foreachInstruction
    | IF condition block ELSE block  # ifElseInstruction
    | IF condition block             # ifInstruction
    | REPEAT expression block        # repeatInstruction
    | RETURN expression              # returnInstruction
    | WHILE condition block          # whileInstruction;

expression
    : <assoc = right> expression op = POW expression # pow
    | expression op = (MUL | DIV) expression         # mulDiv
    | op = (PLUS | MINUS) expression                 # unary
    | expression op = (PLUS | MINUS) expression      # addSub
    | call                                           # callExpression
    | NAT                                            # nat
    | SYM                                            # sym
    | ID                                             # id
    | LROUND expression RROUND                       # expressionParens;

condition
    : NOT condition                                           # not
    | condition AND condition                                 # and
    | condition OR condition                                  # or
    | expression op = (LTEQ | LT | EQ | GT | GTEQ) expression # comparison
    | BOOLEAN                                                 # boolean
    | LROUND condition RROUND                                 # conditionParens;

call: ID LROUND (expression (COMMA expression)*)? RROUND;

NAT: '0' | [1-9] NUMBER*;
SYM: LOWERCASE;
ID:  UPPERCASE (UPPERCASE | LOWERCASE)*;

BOOLEAN: TRUE | FALSE;

ASSIGN: '=';
COMMA:  ',';

LROUND: '(';
RROUND: ')';
LCURLY: '{';
RCURLY: '}';

TRUE:  'true';
FALSE: 'false';
NOT:   '!';
AND:   'and';
OR:    'or';
LTEQ:  '<=';
LT:    '<';
EQ:    '==';
GT:    '>';
GTEQ:  '>=';

PLUS:  '+';
MINUS: '-';
MUL:   '*';
DIV:   '/';
POW:   '^';

ELSE:    'else';
FOREACH: 'foreach';
IF:      'if';
IN:      'in';
REPEAT:  'repeat';
RETURN:  'return';
WHILE:   'while';

fragment NUMBER:    [0-9];
fragment UPPERCASE: [A-Z];
fragment LOWERCASE: [a-z];

WS: [ \t\n\r]+ -> skip;

LINE_COMMENT:  '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;