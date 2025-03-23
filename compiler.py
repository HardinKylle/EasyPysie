import sys
from io import StringIO
from lexer import lexer
from parser import parser
from semantic import semantic_analysis
from ir_generator import generate_ir
from code_generator import generate_code, generate_assembly

def compile_code(source_code, target="python"):
    """
    Full compilation pipeline: Lexing, Parsing, Semantic Analysis, IR, Code Generation.
    The final execution output is returned for the GUI.
    """
    try:
        # 🔹 Step 1: Lexical Analysis
        lexer.input(source_code)
        print("\n🔹 Lexical Analysis:")
        for tok in lexer:
            print(tok)

        # 🔹 Step 2: Parsing
        ast = parser.parse(source_code)
        if not ast:
            print("\n❌ Parsing failed!")
            return "Parsing failed!"

        print("\n🔹 Parsing Succeeded:")
        print(ast)

        # 🔹 Step 3: Semantic Analysis
        try:
            semantic_analysis(ast)
            print("\n✅ Semantic Analysis Passed!")
        except Exception as e:
            print("\n❌ Semantic Analysis Error:", e)
            return f"Semantic Analysis Error: {e}"

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
            return "Unsupported target language!"

        print(final_code)

        # 🔹 Step 6: Execute Python Code and Capture Output (Only for Python target)
        if target == "python":
            return execute_code(final_code)
        else:
            return "Compilation succeeded! (Check terminal for assembly code)"

    except Exception as e:
        return f"Compilation Error: {e}"

def execute_code(code):
    """
    Executes the given Python code and captures its output.
    """
    try:
        # Redirect stdout to capture execution output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        # Execute the code safely
        exec_env = {}
        exec(code, {}, exec_env)

        # Get captured output
        sys.stdout = old_stdout
        return f"Compilation succeeded!\n\n{captured_output.getvalue()}"

    except Exception as e:
        sys.stdout = old_stdout
        return f"Execution Error: {e}"
