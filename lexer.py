#lexer.py

# Import the PLY library for lexical analysis.
import ply.lex as lex

# List of token names used in the language.
tokens = [
    # Basic tokens for numbers, strings, and identifiers.
    'NUMBER', 'FLOAT', 'STRING', 'IDENTIFIER',
    # Arithmetic operators.
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    # Comparison operators.
    'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ',
    # Logical operators.
    'AND', 'OR', 'NOT',
    # Assignment operator.
    'ASSIGN',
    # Parentheses and braces.
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    # Punctuation.
    'SEMICOLON', 'COMMA'
]

# Reserved keywords with kid-friendly syntax.
reserved = {
    'check': 'CHECK',        # if → check
    'otherwise': 'OTHERWISE',# else → otherwise
    'keep': 'KEEP',          # while → keep
    'repeat': 'REPEAT',      # for → repeat
    'create': 'CREATE',      # function → create
    'say': 'SAY',            # print → say
    'ask': 'ASK',            # input → ask
    'give': 'GIVE',          # return → give
    'is': 'IS'               # assignment → is
}

# Combine tokens and reserved keywords.
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

# Rule for floating-point numbers.
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)  # Convert to float.
    return t

# Rule for integer numbers.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convert to integer.
    return t

# Rule for string literals.
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove quotes.
    return t

# Rule for identifiers and reserved words.
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check if it's a reserved word.
    return t

# Rule for handling newlines.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # Update line number.

# Characters to ignore (spaces and tabs).
t_ignore = ' \t'

# Error handling rule for illegal characters.
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer.
lexer = lex.lex()

# Test the lexer with sample input.
if __name__ == "__main__":
    data = '''
    create add(a, b) {
        give a + b;
    }
    say("Result: " + add(3, 4));
    check (a < 10) {
        say("a is less than 10");
    } otherwise {
        say("a is 10 or more");
    }
    keep (a > 0) {
        a = a - 1;
    }
    '''
    lexer.input(data)
    for tok in lexer:
        print(tok)
