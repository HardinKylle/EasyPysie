import sys
from io import StringIO
import tkinter as tk
from tkinter import simpledialog
from lexer import lexer
from parser import parser
from semantic import semantic_analysis
from ir_generator import generate_ir
from code_generator import generate_code, generate_assembly

def my_input(prompt=""):
    # Create a temporary hidden Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    # Show an input dialog to the user
    user_response = simpledialog.askstring(title="Input Required", prompt=prompt)
    root.destroy()  # Destroy the root window after getting input
    return user_response if user_response is not None else ""

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

        print("\n🔹 AST Debug:", ast)
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

            # Handle LABEL and GOTO for while loops (if needed)
            lines = final_code.splitlines()
            python_code = []
            label_map = {}

            for i, line in enumerate(lines):
                if line.startswith("LABEL"):
                    label_name = line.split()[1]
                    label_map[label_name] = i
                elif line.startswith("GOTO"):
                    target_label = line.split()[1]
                    python_code.append(f"# GOTO {target_label}")
                elif line.startswith("IF_FALSE"):
                    condition, target_label = line.split()[1], line.split()[3]
                    python_code.append(f"if not {condition}:")
                    python_code.append(f"    # GOTO {target_label}")
                else:
                    python_code.append(line)

            final_code = "\n".join(python_code)

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
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        # Provide our custom input() function in the execution environment.
        exec_env = {"input": my_input}

        exec(code, exec_env)

        sys.stdout = old_stdout
        return f"Compilation succeeded!\n\n{captured_output.getvalue()}"
    except Exception as e:
        sys.stdout = old_stdout
        return f"Execution Error: {e}"

if __name__ == "__main__":
    source_code = """
    count is 3;
    
    keep (count > 0) { 
        say("Count is: " + count);
        count is count - 1;
    }
    
    name is ask();  
    say("Hello, " + name + "!");
    """
    output = compile_code(source_code, target="python")
    print("\n=== Execution Output ===")
    print(output)
