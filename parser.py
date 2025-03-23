import ply.yacc as yacc
from lexer import tokens  # Assume your lexer file is named lexer.py

# Define the precedence and associativity of operators if needed
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Dictionary to hold names (for simple variable storage, etc.)
names = {}

# Start symbol: a program is a list of statements.
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : assignment_statement
                 | expression_statement'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = ('expr', p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1])

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = ('var', p[1])

# Error rule for syntax errors.
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Build the parser.
parser = yacc.yacc()

# Test the parser with a simple input.
data = """
a = 3 + 4;
b = a * 2;
"""
result = parser.parse(data)

if result is None:
    print("Parsing failed: No result returned.")
else:
    print("Parsing succeeded:")
    print(result)

