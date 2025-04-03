#code_generator.py

def generate_code(ir_code):
    """
    Generate Python code from Intermediate Representation (IR).
    """
    python_code = []
    i = 0
    while i < len(ir_code):
        instr = ir_code[i]
        
        # Detect a while loop pattern.
        if instr.startswith("LABEL "):
            label = instr.split()[1]
            # Look ahead: check if the next instruction is an assignment (condition evaluation)
            if i+1 < len(ir_code) and " = " in ir_code[i+1]:
                assign_line = ir_code[i+1]
                parts = assign_line.split(" = ", 1)
                if len(parts) == 2:
                    temp_var, condition_expr = parts
                    # Next instruction should be IF_FALSE using that temporary variable.
                    if i+2 < len(ir_code) and ir_code[i+2].startswith("IF_FALSE"):
                        if_line = ir_code[i+2]
                        if temp_var in if_line:
                            # We have detected our while loop pattern.
                            # Skip these three instructions.
                            i += 3
                            # Now gather the loop body until we reach the GOTO that jumps back to our start label.
                            body_block = []
                            while i < len(ir_code) and not (ir_code[i].startswith("GOTO") and ir_code[i].split()[1] == label):
                                body_block.append(ir_code[i])
                                i += 1
                            # Skip the GOTO instruction.
                            if i < len(ir_code):
                                i += 1
                            # Skip the end label.
                            if i < len(ir_code) and ir_code[i].startswith("LABEL"):
                                i += 1
                            # Emit a proper Python while loop.
                            python_code.append(f"while {condition_expr}:")
                            loop_body = generate_code(body_block)
                            for line in loop_body.split("\n"):
                                python_code.append("    " + line)
                            continue  # Move to next IR instruction after the while loop.
        
        # Existing handling for print statements.
        if instr.startswith("PRINT "):
            expr = instr.split("PRINT ")[1]
            python_code.append(f"print({expr})")
            i += 1
        
        # Handle if-else branching (existing code remains unchanged).
        elif instr.startswith("IF_FALSE"):
            parts = instr.split()
            cond = parts[1]
            label_else = parts[3]
            i += 1
            then_block = []
            while i < len(ir_code) and not ir_code[i].startswith("GOTO"):
                then_block.append(ir_code[i])
                i += 1
            if i < len(ir_code) and ir_code[i].startswith("GOTO"):
                goto_parts = ir_code[i].split()
                label_end = goto_parts[1]
                i += 1
            else:
                label_end = None
            if i < len(ir_code) and ir_code[i].startswith("LABEL"):
                curr_label = ir_code[i].split()[1]
                if curr_label != label_else:
                    raise SyntaxError(f"Expected label {label_else}, got {curr_label}")
                i += 1
            else:
                raise SyntaxError("Expected label for else branch not found.")
            else_block = []
            while i < len(ir_code) and not (ir_code[i].startswith("LABEL") and ir_code[i].split()[1] == label_end):
                else_block.append(ir_code[i])
                i += 1
            if i < len(ir_code):
                i += 1
            then_code = generate_code(then_block)
            else_code = generate_code(else_block) if else_block else ""
            python_code.append(f"if {cond}:")
            for line in then_code.split("\n"):
                python_code.append("    " + line)
            if else_code:
                python_code.append("else:")
                for line in else_code.split("\n"):
                    python_code.append("    " + line)
        
        # Default translation for other instructions.
        else:
            instr_mod = instr.replace("&&", "and").replace("||", "or").replace("! ", "not ")
            python_code.append(instr_mod)
            i += 1

    return "\n".join(python_code)



def generate_assembly(ir_code):
    """
    Generate x86-like assembly code from Intermediate Representation (IR).
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
