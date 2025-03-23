# main.py
from lexer import lexer
from parser import parser
from semantic import semantic_analysis, symbol_table

# Sample input program
data = """
a = 3 + 4;
b = a * 2;
"""

# Lexical Analysis (Tokenization)
lexer.input(data)
print("\nLexical Analysis:")
for token in lexer:
    print(token)

# Parsing (Syntax Analysis)
print("\nParsing:")
ast = parser.parse(data)

if ast is None:
    print("Parsing failed.")
else:
    print("Parsing succeeded. Now performing semantic analysis...")
    
    # Semantic Analysis
    try:
        semantic_analysis(ast)
        print("Semantic analysis passed! Symbol table:", symbol_table)
    except Exception as e:
        print("Semantic analysis error:", e)
