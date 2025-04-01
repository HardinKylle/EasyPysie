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
    '''assignment_statement : IDENTIFIER IS expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])  # is → assignment

# New nonterminal: assignment expression (without trailing semicolon) for use in the for-loop.
def p_assignment_expression(p):
    'assignment_expression : IDENTIFIER ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

def p_expression_statement(p):
    'expression_statement : expression SEMICOLON'
    p[0] = ('expr', p[1])

def p_print_statement(p):
    'print_statement : SAY LPAREN expression RPAREN SEMICOLON'
    p[0] = ('print', p[3])  # say → print

def p_input_statement(p):
    'input_statement : IDENTIFIER IS ASK LPAREN RPAREN SEMICOLON'
    p[0] = ('input', p[1])  # ask → input

def p_if_statement(p):
    '''if_statement : CHECK LPAREN expression RPAREN LBRACE statement_list RBRACE
                    | CHECK LPAREN expression RPAREN LBRACE statement_list RBRACE OTHERWISE LBRACE statement_list RBRACE'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])  # check → if
    else:
        p[0] = ('ifelse', p[3], p[6], p[10])  # otherwise → else

def p_while_statement(p):
    'while_statement : KEEP LPAREN expression RPAREN LBRACE statement_list RBRACE'
    p[0] = ('while', p[3], p[6])  # keep → while

def p_for_statement(p):
    'for_statement : REPEAT LPAREN assignment_expression SEMICOLON expression SEMICOLON assignment_expression RPAREN LBRACE statement_list RBRACE'
    p[0] = ('for', p[3], p[5], p[7], p[10])  # repeat → for

def p_function_declaration(p):
    'function_declaration : CREATE IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list RBRACE'
    p[0] = ('function', p[2], p[4], p[7])  # create → function

def p_return_statement(p):
    'return_statement : GIVE expression SEMICOLON'
    p[0] = ('return', p[2])  # give → return

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
    p[0] = ('binop', p[2], p[1], p[3])  # plus → addition

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
    create add(a, b) {
        give a + b;
    }
    a is 3 plus 4;
    b = add(a, 2);
    say("Result: " + b);
    
    check (a < 10) {
        say("a is less than 10");
    } otherwise {
        say("a is 10 or more");
    }
    
    keep (a > 0) {
        a = a - 1;
    }
    
    repeat (i = 0; i < 10; i = i + 1) {
        say(i);
    }
    
    c = ask();
    """
    result = parser.parse(data)
    if result is None:
        print("Parsing failed: No result returned.")
    else:
        print("Parsing succeeded:")
        print(result)
