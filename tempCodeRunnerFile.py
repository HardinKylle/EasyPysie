import ply.yacc as yacc
from lexer import tokens

# Precedence and associativity rules.
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Dictionary for variable storage, if needed.
names = {}

# Program: a list of statements.
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
                 | expression_statement
                 | print_statement
                 | if_statement
                 | while_statement
                 | for_statement
                 | function_declaration
                 | return_statement
                 | input_statement'''
    p[0] = p[1]

def p_assignment_statement(p):
    'assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON'
    p[0] = ('assign', p[1], p[3])

def p_expression_statement(p):
    'expression_statement : expression SEMICOLON'
    p[0] = ('expr', p[1])

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = ('print', p[3])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('ifelse', p[3], p[6], p[10])

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE'
    p[0] = ('while', p[3], p[6])

def p_for_statement(p):
    'for_statement : FOR LPAREN assignment_statement expression SEMICOLON expression RPAREN LBRACE statement_list RBRACE'
    p[0] = ('for', p[3], p[4], p[6], p[9])

def p_function_declaration(p):
    'function_declaration : FUNCTION IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list RBRACE'
    p[0] = ('function', p[2], p[4], p[7])

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA IDENTIFIER
                      | IDENTIFIER
                      | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression
                     | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_expression_function_call(p):
    'expression : IDENTIFIER LPAREN argument_list RPAREN'
    p[0] = ('call', p[1], p[3])

def p_return_statement(p):
    'return_statement : RETURN expression SEMICOLON'
    p[0] = ('return', p[2])

def p_input_statement(p):
    'input_statement : IDENTIFIER ASSIGN INPUT LPAREN RPAREN SEMICOLON'
    p[0] = ('input', p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression GT expression
                  | expression LEQ expression
                  | expression GEQ expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_logic(p):
    '''expression : expression AND expression
                  | expression OR expression'''
    p[0] = ('logic', p[2], p[1], p[3])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = ('not', p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])

def p_expression_float(p):
    'expression : FLOAT'
    p[0] = ('float', p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = ('string', p[1])

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ('var', p[1])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF")

def p_empty(p):
    'empty :'
    p[0] = None

# Build the parser.
parser = yacc.yacc()

if __name__ == "__main__":
    data = """
    function add(a, b) {
        return a + b;
    }
    a = 3 + 4;
    b = add(a, 2);
    print("Result: " + b);
    
    if (a < 10) {
        print("a is less than 10");
    } else {
        print("a is 10 or more");
    }
    
    while (a > 0) {
        a = a - 1;
    }
    
    for (i = 0; i < 10; i = i + 1) {
        print(i);
    }
    
    c = input();
    """
    result = parser.parse(data)
    if result is None:
        print("Parsing failed: No result returned.")
    else:
        print("Parsing succeeded:")
        print(result)
