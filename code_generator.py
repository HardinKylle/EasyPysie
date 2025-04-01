def generate_code(ir_code):
    python_code = []
    for instr in ir_code:
        if instr.startswith("PRINT "):
            expr = instr.split("PRINT ")[1]
            python_code.append(f"print({expr})")  # Convert IR to Python
        else:
            # Replace logical operators with Python equivalents
            instr = instr.replace("&&", "and").replace("||", "or").replace("!", "not ")
            python_code.append(instr)

    return "\n".join(python_code)


def generate_assembly(ir_code):
    """
    Converts Three-Address Code (TAC) into x86-like assembly.
    """
    assembly_code = []
    
    for instr in ir_code:
        if instr.startswith("PRINT "):  # Handling print statements
            expr = instr.split("PRINT ")[1]
            assembly_code.append(f"OUT {expr}")  # Output instruction in assembly
            continue

        parts = instr.split(" = ")
        if len(parts) == 2:
            left, right = parts
            if " + " in right:
                a, b = right.split(" + ")
                assembly_code.append(f"MOV R1, {a}")
                assembly_code.append(f"ADD R1, {b}")
                assembly_code.append(f"MOV {left}, R1")
            elif " - " in right:  # Subtraction
                a, b = right.split(" - ")
                assembly_code.append(f"MOV R1, {a}")
                assembly_code.append(f"SUB R1, {b}")
                assembly_code.append(f"MOV {left}, R1")
            elif " * " in right:  # Multiplication
                a, b = right.split(" * ")
                assembly_code.append(f"MOV R1, {a}")
                assembly_code.append(f"MUL R1, {b}")
                assembly_code.append(f"MOV {left}, R1")
            elif " / " in right:  # Division
                a, b = right.split(" / ")
                assembly_code.append(f"MOV R1, {a}")
                assembly_code.append(f"DIV R1, {b}")
                assembly_code.append(f"MOV {left}, R1")
            else:
                assembly_code.append(f"MOV {left}, {right}")

    return "\n".join(assembly_code)
