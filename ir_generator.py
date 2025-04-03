# ir_generator.py

# Counter for generating unique temporary variables.
temp_counter = 0

def new_temp():
    """
    Generate a new temporary variable name.
    """
    global temp_counter
    temp_counter += 1
    return f"t{temp_counter}"

def generate_ir(node):
    """
    Generate Intermediate Representation (IR) for the given AST node.
    """
    node_type = node[0]

    # Handle number literals.
    if node_type == 'number':
        return (str(node[1]), [])
    
    # Handle input statements.
    elif node_type == 'input':
        var_name = node[1]
        prompt = node[2] if node[2] else '""'
        instr = f"{var_name} = input({prompt})"
        return (var_name, [instr])
    
    # Handle float literals.
    elif node_type == 'float':
        return (node[1], [])
    
    # Handle variable usage.
    elif node_type == 'var':
        return (node[1], [])
    
    # Handle string literals.
    elif node_type == 'string':
        return (f'"{node[1]}"', [])
    
    # Handle binary operations.
    elif node_type == 'binop':
        op = node[1]
        left_result, left_code = generate_ir(node[2])
        right_result, right_code = generate_ir(node[3])
        
        if op == '+':
            # Always convert to strings if either operand is a string or if we can't determine types
            temp = new_temp()
            instr = f"{temp} = str({left_result}) + str({right_result})"
        else:
            temp = new_temp()
            instr = f"{temp} = {left_result} {op} {right_result}"
        
        return (temp, left_code + right_code + [instr])
    
    # Handle variable assignment.
    elif node_type == 'assign':
        var_name = node[1]
        expr_result, expr_code = generate_ir(node[2])
        instr = f"{var_name} = {expr_result}"
        return (var_name, expr_code + [instr])
    
    # Handle logical operations.
    elif node_type == 'logic':
        op = node[1]
        left_result, left_code = generate_ir(node[2])
        right_result, right_code = generate_ir(node[3])
        
        temp = new_temp()
        instr = f"{temp} = {left_result} {op} {right_result}"
        return (temp, left_code + right_code + [instr])
    
    # Handle program node (list of statements).
    elif node_type == 'program':
        code = []
        for stmt in node[1]:
            _, stmt_code = generate_ir(stmt)
            code.extend(stmt_code)
        return (None, code)
    
    # Handle print statements.
    elif node_type == 'print':
        expr_result, expr_code = generate_ir(node[1])
        instr = f"PRINT {expr_result}"
        return (None, expr_code + [instr])
    
    # Handle if-else statements.
    elif node_type == 'ifelse':
        condition_result, condition_code = generate_ir(node[1])  # Generate IR for the condition
        if_block_code = []
        for stmt in node[2]:  # Generate IR for the 'if' block
            stmt_result, stmt_code = generate_ir(stmt)
            if_block_code.extend(stmt_code)
        
        else_block_code = []
        if len(node) > 3:  # If there's an 'otherwise' block
            for stmt in node[3]:
                stmt_result, stmt_code = generate_ir(stmt)
                else_block_code.extend(stmt_code)
        
        # Generate labels for branching
        if_label = new_temp()
        else_label = new_temp()
        end_label = new_temp()
        
        # IR for the if-else structure
        ir_code = condition_code + [
            f"IF_FALSE {condition_result} GOTO {else_label}"
        ] + if_block_code + [
            f"GOTO {end_label}",
            f"LABEL {else_label}"
        ] + else_block_code + [
            f"LABEL {end_label}"
        ]
        
        return (None, ir_code)
    
    # Handle while loops.
    elif node_type == 'while':
        condition_result, condition_code = generate_ir(node[1])
        body_code = []
        for stmt in node[2]:
            _, stmt_code = generate_ir(stmt)
            body_code.extend(stmt_code)

        start_label = new_temp()
        end_label = new_temp()

        ir_code = [
            f"LABEL {start_label}",
            *condition_code,
            f"IF_FALSE {condition_result} GOTO {end_label}",
            *body_code,
            f"GOTO {start_label}",
            f"LABEL {end_label}"
        ]

        return (None, ir_code)
    
    # Handle function declarations.
    elif node_type == 'function':
        func_name = node[1]
        params = node[2]
        body_code = []
        for stmt in node[3]:
            _, stmt_code = generate_ir(stmt)
            body_code.extend(stmt_code)
        func_def = f"def {func_name}({', '.join(params)}):\n"
        if not body_code:
            func_def += "    pass\n"
        else:
            for line in body_code:
                func_def += "    " + line + "\n"
        return (None, [func_def])
    
    # Handle return statements.
    elif node_type == 'return':
        expr_result, expr_code = generate_ir(node[1])
        instr = f"return {expr_result}"
        return (None, expr_code + [instr])
    
    # Handle function calls.
    elif node_type == 'call':
        func_name = node[1]
        args = node[2]
        
        arg_results = []
        arg_code = []
        for arg in args:
            result, code = generate_ir(arg)
            arg_results.append(result)
            arg_code.extend(code)
        
        temp = new_temp()
        instr = f"{temp} = {func_name}({', '.join(arg_results)})"
        return (temp, arg_code + [instr])
    
    # Handle repeat loops.
    elif node_type == 'repeat':
        count_expr = node[1]
        body = node[2]
        
        count_result, count_code = generate_ir(count_expr)
        loop_counter = new_temp()
        init_code = count_code + [f"{loop_counter} = 0"]
        
        condition_temp = new_temp()
        condition_code = [f"{condition_temp} = {loop_counter} < {count_result}"]
        
        body_ir = []
        for stmt in body:
            _, stmt_code = generate_ir(stmt)
            body_ir.extend(stmt_code)
        increment_code = [f"{loop_counter} = {loop_counter} + 1"]
        
        start_label = new_temp()
        end_label = new_temp()
        
        ir_code = init_code + [
            f"LABEL {start_label}",
            *condition_code,
            f"IF_FALSE {condition_temp} GOTO {end_label}",
            *body_ir,
            *increment_code,
            f"GOTO {start_label}",
            f"LABEL {end_label}"
        ]
        return (None, ir_code)
    
    # Raise an error for unsupported node types.
    else:
        raise NotImplementedError(f"IR generation not implemented for node type: {node_type}")
