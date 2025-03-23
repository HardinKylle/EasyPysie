# main.py
from lexer import lexer
from parser import parser
from semantic import semantic_analysis, symbol_table
from ir_generator import generate_ir

data = """
a = 3 + 4;
b = a * 2;
"""

# Lexical Analysis
lexer.input(data)
print("\nLexical Analysis:")
for token in lexer:
    print(token)

# Parsing
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
        
        # Intermediate Code Generation (IR)
        print("\nGenerating Intermediate Representation (IR):")
        _, ir_code = generate_ir(ast)
        for instr in ir_code:
            print(instr)

    except Exception as e:
        print("Semantic analysis error:", e)
