# semantic.py

symbol_table = {}     # Stores variable types (global variables)
function_table = {}   # Stores function definitions

def semantic_analysis(node, local_scope=None):
    """
    Recursively analyze AST nodes.
    Optionally, a local_scope (dictionary) may be passed for function parameters.
    """
    # Helper function to lookup a variable in local scope first, then global.
    def lookup(var):
        if local_scope and var in local_scope:
            return local_scope[var]
        elif var in symbol_table:
            return symbol_table[var]
        else:
            raise NameError(f"Oops! You forgot to create the variable '{var}' before using it.")

    node_type = node[0]

    if node_type == 'program':
        for stmt in node[1]:
            semantic_analysis(stmt, local_scope)
        return None

    elif node_type == 'assign':
        var_name = node[1]
        expr_type = semantic_analysis(node[2], local_scope)
        if local_scope is not None:
            local_scope[var_name] = expr_type
        else:
            symbol_table[var_name] = expr_type
        return expr_type

    elif node_type == 'binop':
        operator = node[1]
        left_type = semantic_analysis(node[2], local_scope)
        right_type = semantic_analysis(node[3], local_scope)

        if operator == '+':  # Handle addition or string concatenation
            if left_type == "string" or right_type == "string":
                if left_type not in ("string", "int", "float") or right_type not in ("string", "int", "float"):
                    raise TypeError(f"Oops! You can only use numbers or strings with '{operator}'.")
                return "string"
            elif left_type in ('int', 'float') and right_type in ('int', 'float'):
                return 'float' if 'float' in (left_type, right_type) else 'int'
            else:
                raise TypeError(f"Oops! You can only use numbers or strings with '{operator}'.")
        elif operator in ('-', '*', '/'):
            if left_type not in ('int', 'float') or right_type not in ('int', 'float'):
                raise TypeError(f"Oops! You can only use numbers with '{operator}'. Got types {left_type} and {right_type}.")
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

    elif node_type == 'logic':  # For logical operations, similar to binop.
        operator = node[1]
        left_type = semantic_analysis(node[2], local_scope)
        right_type = semantic_analysis(node[3], local_scope)
        if operator in ('&&', '||'):
            if left_type != 'bool' or right_type != 'bool':
                raise TypeError(f"Logical operator '{operator}' requires boolean operands, got {left_type} and {right_type}")
            return 'bool'

    elif node_type == 'number':
        return 'int'  # Assuming number literals are integers

    elif node_type == 'float':
        return 'float'

    elif node_type == 'string':
        return 'string'

    elif node_type == 'var':
        var_name = node[1]
        return lookup(var_name)

    elif node_type == 'expr':
        return semantic_analysis(node[1], local_scope)

    elif node_type == 'print':
        expr_type = semantic_analysis(node[1], local_scope)
        if expr_type not in ('int', 'float', 'string', 'bool'):
            raise TypeError(f"Cannot print value of type {expr_type}")
        return None

    elif node_type == 'not':
        expr_type = semantic_analysis(node[1], local_scope)
        if expr_type != 'bool':
            raise TypeError(f"NOT operation requires boolean, got {expr_type}")
        return 'bool'
    
    elif node_type == 'ifelse':  # Handle if-else statements
        condition_type = semantic_analysis(node[1], local_scope)
        if condition_type not in ('int', 'bool'):
            raise Exception("Condition in 'check' must evaluate to an integer or boolean.")
        for stmt in node[2]:
            semantic_analysis(stmt, local_scope)
        if len(node) > 3:
            for stmt in node[3]:
                semantic_analysis(stmt, local_scope)
        return None

    elif node_type == 'input':
        var_name = node[1]
        if local_scope is not None:
            local_scope[var_name] = 'string'
        else:
            symbol_table[var_name] = 'string'
        return 'string'
    
    elif node_type == 'while':
        condition_type = semantic_analysis(node[1], local_scope)
        if condition_type not in ('bool', 'int'):
            raise TypeError("Condition in 'keep' must evaluate to a boolean or integer.")
        for stmt in node[2]:
            semantic_analysis(stmt, local_scope)
        return None

    elif node_type == 'function':
        func_name = node[1]
        params = node[2]
        body = node[3]
        if func_name in function_table:
            raise NameError(f"Oops! The function '{func_name}' is already defined.")
        function_table[func_name] = {
            "params": params,
            "body": body
        }
        for param in params:
            symbol_table[param] = 'unknown'
        return None

    elif node_type == 'call':
        func_name = node[1]
        args = node[2]
        if func_name not in function_table:
            raise NameError(f"Oops! You tried to call the function '{func_name}', but it is not defined.")
        func_def = function_table[func_name]
        if len(args) != len(func_def["params"]):
            raise TypeError(f"Oops! The function '{func_name}' expects {len(func_def['params'])} arguments, but got {len(args)}.")
        local_call_scope = {}
        for i, param in enumerate(func_def["params"]):
            arg_type = semantic_analysis(args[i], local_scope)
            local_call_scope[param] = arg_type
            symbol_table[param] = arg_type
        ret_type = None
        for stmt in func_def["body"]:
            # If a return statement is found, capture its type.
            if stmt[0] == 'return':
                ret_type = semantic_analysis(stmt, local_call_scope)
                break
            else:
                semantic_analysis(stmt, local_call_scope)
        if ret_type is None:
            ret_type = 'void'
        return ret_type

    elif node_type == 'return':
        expr_type = semantic_analysis(node[1], local_scope)
        return expr_type

    else:
        raise NotImplementedError(f"Semantic analysis not implemented for node type: {node_type}")
