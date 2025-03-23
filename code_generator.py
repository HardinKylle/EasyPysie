def generate_code(ir_code):
    """
    Translates Intermediate Representation (IR) into Python code.
    """
    python_code = []
    for instr in ir_code:
        python_code.append(instr)  # IR is already close to Python syntax

    return "\n".join(python_code)

def generate_assembly(ir_code):
    """
    Converts Three-Address Code (TAC) into x86-like assembly.
    """
    assembly_code = []
    for instr in ir_code:
        parts = instr.split(" = ")
        if len(parts) == 2:
            left, right = parts
            if "+" in right:
                a, b = right.split(" + ")
                assembly_code.append(f"MOV R1, {a}")
                assembly_code.append(f"ADD R1, {b}")
                assembly_code.append(f"MOV {left}, R1")
            elif "*" in right:
                a, b = right.split(" * ")
                assembly_code.append(f"MOV R1, {a}")
                assembly_code.append(f"MUL R1, {b}")
                assembly_code.append(f"MOV {left}, R1")
            else:
                assembly_code.append(f"MOV {left}, {right}")

    return "\n".join(assembly_code)
