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

        if operator in ('+', '-', '*', '/'):
            if left_type not in ('int', 'float') or right_type not in ('int', 'float'):
                raise TypeError(f"Operator '{operator}' requires numeric types, got {left_type} and {right_type}")
            return 'float' if left_type == 'float' or right_type == 'float' else 'int'

        elif operator in ('==', '!=', '<', '>', '<=', '>='):
            if left_type != right_type:
                raise TypeError(f"Comparison '{operator}' requires operands of the same type")
            return 'bool'

        elif operator in ('&&', '||'):
            if left_type != 'bool' or right_type != 'bool':
                raise TypeError(f"Logical operator '{operator}' requires boolean operands")
            return 'bool'

        else:
            raise NotImplementedError(f"Unknown operator: {operator}")

    elif node_type == 'number':
        return 'int'  # Assume integers; modify if floats are separately detected

    elif node_type == 'float':
        return 'float'

    elif node_type == 'string':
        return 'string'

    elif node_type == 'var':
        var_name = node[1]
        if var_name not in symbol_table:
            raise NameError(f"Variable '{var_name}' used before assignment")
        return symbol_table[var_name]

    elif node_type == 'expr':
        return semantic_analysis(node[1])

    elif node_type == 'print':
        expr_type = semantic_analysis(node[1])
        if expr_type not in ('int', 'float', 'string', 'bool'):
            raise TypeError(f"Cannot print value of type {expr_type}")
        return None

    elif node_type == 'not':
        expr_type = semantic_analysis(node[1])
        if expr_type != 'bool':
            raise TypeError(f"NOT operation requires boolean, got {expr_type}")
        return 'bool'

    else:
        raise NotImplementedError(f"Semantic analysis not implemented for node type: {node_type}")
