# ir_generator.py

temp_counter = 0  # Counter for temporary variables

def new_temp():
    global temp_counter
    temp_counter += 1
    return f"t{temp_counter}"

def generate_ir(node):
    node_type = node[0]
    
    if node_type == 'number':
        return (node[1], [])
    
    elif node_type == 'var':
        return (node[1], [])
    
    elif node_type == 'binop':
        op = node[1]
        left_result, left_code = generate_ir(node[2])
        right_result, right_code = generate_ir(node[3])
        
        temp = new_temp()
        instr = f"{temp} = {left_result} {op} {right_result}"
        return (temp, left_code + right_code + [instr])
    
    elif node_type == 'assign':
        var_name = node[1]
        expr_result, expr_code = generate_ir(node[2])
        instr = f"{var_name} = {expr_result}"
        return (var_name, expr_code + [instr])
    
    elif node_type == 'program':
        code = []
        for stmt in node[1]:
            _, stmt_code = generate_ir(stmt)
            code.extend(stmt_code)
        return (None, code)
    
    else:
        raise NotImplementedError(f"IR generation not implemented for node type: {node_type}")
