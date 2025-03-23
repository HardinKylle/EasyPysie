import ply.lex as lex

# List of token names.
tokens = [
    'NUMBER', 'FLOAT', 'STRING', 'IDENTIFIER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ',
    'AND', 'OR', 'NOT',
    'ASSIGN',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA'
]

# Reserved keywords.
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'function': 'FUNCTION',
    'print': 'PRINT',
    'input': 'INPUT',
    'return': 'RETURN'
}

tokens = tokens + list(reserved.values())

# Regular expression rules for simple tokens.
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_ASSIGN    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'
t_COMMA     = r','

# Multi-character operators.
t_EQ        = r'=='
t_NEQ       = r'!='
t_LEQ       = r'<='
t_GEQ       = r'>='
t_LT        = r'<'
t_GT        = r'>'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOT       = r'!'

# Floating point numbers.
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Integer numbers.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# String literals.
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

# Identifiers and reserved words.
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Newline handling.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters (spaces and tabs).
t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer.
lexer = lex.lex()

if __name__ == "__main__":
    data = '''
    function add(a, b) {
        return a + b;
    }
    print("Result: " + add(3, 4));
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
    '''
    lexer.input(data)
    for tok in lexer:
        print(tok)
