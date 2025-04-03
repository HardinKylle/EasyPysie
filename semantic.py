# semantic.py

# Global symbol table for variable types.
symbol_table = {}

# Global function table for function definitions.
function_table = {}

def semantic_analysis(node, local_scope=None):
    """
    Perform semantic analysis on the given AST node.
    Ensures type correctness and validates variable/function usage.
    """
    # Helper function to look up a variable in local or global scope.
    def lookup(var):
        """
        Look up a variable in the local scope first, then global scope.
        Raises an error if the variable is not found.
        """
        if local_scope and var in local_scope:
            return local_scope[var]
        elif var in symbol_table:
            return symbol_table[var]
        else:
            raise NameError(f"Oops! You forgot to create the variable '{var}' before using it.")

    node_type = node[0]

    # Handle the program node (list of statements).
    if node_type == 'program':
        """
        Process a program node, which contains a list of statements.
        """
        for stmt in node[1]:
            semantic_analysis(stmt, local_scope)
        return None

    # Handle variable assignment.
    elif node_type == 'assign':
        """
        Process an assignment node, assigning a value to a variable.
        """
        var_name = node[1]
        expr_type = semantic_analysis(node[2], local_scope)
        if local_scope is not None:
            local_scope[var_name] = expr_type
        else:
            symbol_table[var_name] = expr_type
        return expr_type

    # Handle binary operations (e.g., +, -, *, /).
    elif node_type == 'binop':
        """
        Process a binary operation node, ensuring type correctness.
        """
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

    # Handle logical operations (e.g., &&, ||).
    elif node_type == 'logic':
        """
        Process a logical operation node, ensuring boolean operands.
        """
        operator = node[1]
        left_type = semantic_analysis(node[2], local_scope)
        right_type = semantic_analysis(node[3], local_scope)
        if operator in ('&&', '||'):
            if left_type != 'bool' or right_type != 'bool':
                raise TypeError(f"Logical operator '{operator}' requires boolean operands, got {left_type} and {right_type}")
            return 'bool'

    # Handle number literals.
    elif node_type == 'number':
        """
        Process a number literal node, returning its type as 'int'.
        """
        return 'int'  # Assuming number literals are integers

    # Handle float literals.
    elif node_type == 'float':
        """
        Process a float literal node, returning its type as 'float'.
        """
        return 'float'

    # Handle string literals.
    elif node_type == 'string':
        """
        Process a string literal node, returning its type as 'string'.
        """
        return 'string'

    # Handle variable usage.
    elif node_type == 'var':
        """
        Process a variable node, looking up its type in the symbol table.
        """
        var_name = node[1]
        return lookup(var_name)

    # Handle expressions.
    elif node_type == 'expr':
        """
        Process an expression node, evaluating its type.
        """
        return semantic_analysis(node[1], local_scope)

    # Handle print statements.
    elif node_type == 'print':
        """
        Process a print statement node, ensuring the value can be printed.
        """
        expr_type = semantic_analysis(node[1], local_scope)
        if expr_type not in ('int', 'float', 'string', 'bool'):
            raise TypeError(f"Cannot print value of type {expr_type}")
        return None

    # Handle NOT logical operation.
    elif node_type == 'not':
        """
        Process a NOT operation node, ensuring the operand is boolean.
        """
        expr_type = semantic_analysis(node[1], local_scope)
        if expr_type != 'bool':
            raise TypeError(f"NOT operation requires boolean, got {expr_type}")
        return 'bool'
    
    # Handle if-else statements.
    elif node_type == 'ifelse':
        """
        Process an if-else statement node, validating the condition and statements.
        """
        condition_type = semantic_analysis(node[1], local_scope)
        if condition_type not in ('int', 'bool'):
            raise Exception("Condition in 'check' must evaluate to an integer or boolean.")
        for stmt in node[2]:
            semantic_analysis(stmt, local_scope)
        if len(node) > 3:
            for stmt in node[3]:
                semantic_analysis(stmt, local_scope)
        return None

    # Handle input statements.
    elif node_type == 'input':
        """
        Process an input statement node, assigning a string type to the variable.
        """
        var_name = node[1]
        if local_scope is not None:
            local_scope[var_name] = 'string'
        else:
            symbol_table[var_name] = 'string'
        return 'string'
    
    # Handle while loops.
    elif node_type == 'while':
        """
        Process a while loop node, validating the condition and loop body.
        """
        condition_type = semantic_analysis(node[1], local_scope)
        if condition_type not in ('bool', 'int'):
            raise TypeError("Condition in 'keep' must evaluate to a boolean or integer.")
        for stmt in node[2]:
            semantic_analysis(stmt, local_scope)
        return None

    # Handle function declarations.
    elif node_type == 'function':
        """
        Process a function declaration node, storing its definition in the function table.
        """
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

    # Handle function calls.
    elif node_type == 'call':
        """
        Process a function call node, validating arguments and executing the function body.
        """
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

    # Handle return statements.
    elif node_type == 'return':
        """
        Process a return statement node, evaluating the return value type.
        """
        expr_type = semantic_analysis(node[1], local_scope)
        return expr_type
    
    # Handle repeat loops.
    elif node_type == 'repeat':
        """
        Process a repeat loop node, ensuring the count is an integer.
        """
        count_type = semantic_analysis(node[1], local_scope)
        if count_type != 'int':
            raise TypeError(f"Repeat count must be an integer, got {count_type}")
        for stmt in node[2]:
            semantic_analysis(stmt, local_scope)
        return None

    # Raise an error for unsupported node types.
    else:
        raise NotImplementedError(f"Semantic analysis not implemented for node type: {node_type}")
