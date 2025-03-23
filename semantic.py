# semantic.py

symbol_table = {}  # Stores variable types

def semantic_analysis(node):
    """Recursively analyze AST nodes."""
    node_type = node[0]

    if node_type == 'program':
        for stmt in node[1]:
            semantic_analysis(stmt)
        return None

    elif node_type == 'assign':
        var_name = node[1]
        expr_type = semantic_analysis(node[2])
        symbol_table[var_name] = expr_type  # Store variable type
        return expr_type

    elif node_type == 'binop':
        operator = node[1]
        left_type = semantic_analysis(node[2])
        right_type = semantic_analysis(node[3])

        if left_type not in ('int', 'float') or right_type not in ('int', 'float'):
            raise TypeError(f"Operator '{operator}' requires numeric types, got {left_type} and {right_type}")

        return 'float' if left_type == 'float' or right_type == 'float' else 'int'

    elif node_type == 'number':
        return 'int'  

    elif node_type == 'var':
        var_name = node[1]
        if var_name not in symbol_table:
            raise NameError(f"Variable '{var_name}' used before assignment")
        return symbol_table[var_name]

    elif node_type == 'expr':
        return semantic_analysis(node[1])

    else:
        raise NotImplementedError(f"Semantic analysis not implemented for node type: {node_type}")
