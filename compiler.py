import sys
from lexer import lexer
from parser import parser
from semantic import semantic_analysis
from ir_generator import generate_ir
from code_generator import generate_code, generate_assembly

def compile_code(source_code, target="python"):
    """
    Main compiler function to process the source code.
    """
    # 🔹 Step 1: Lexical Analysis
    lexer.input(source_code)
    print("\n🔹 Lexical Analysis:")
    for tok in lexer:
        print(tok)

    # 🔹 Step 2: Parsing
    ast = parser.parse(source_code)
    if not ast:
        print("\n❌ Parsing failed!")
        return
    
    print("\n🔹 Parsing Succeeded:")
    print(ast)

    # 🔹 Step 3: Semantic Analysis
    try:
        semantic_analysis(ast)
        print("\n✅ Semantic Analysis Passed!")
    except Exception as e:
        print("\n❌ Semantic Analysis Error:", e)
        return

    # 🔹 Step 4: Intermediate Representation (IR)
    _, ir_code = generate_ir(ast)
    print("\n🔹 Intermediate Representation (IR):")
    for instr in ir_code:
        print(instr)

    # 🔹 Step 5: Code Generation
    if target == "python":
        final_code = generate_code(ir_code)
        print("\n🔹 Generated Python Code:")
    elif target == "assembly":
        final_code = generate_assembly(ir_code)
        print("\n🔹 Generated Assembly Code:")
    else:
        print("\n❌ Unsupported target language!")
        return

    print(final_code)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            source_code = f.read()
    else:
        # Default sample program:
        source_code = """
        a = 3 + 4;
        b = a * 2;
        """

    target_language = "assembly"  # Change to "assembly" for assembly output
    compile_code(source_code, target_language)
