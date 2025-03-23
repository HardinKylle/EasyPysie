import sys
from io import StringIO

def compile_code(source_code, target="python"):
    """
    Executes the given Python source code and captures its output.
    """
    try:
        # Redirect stdout to capture execution output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        # Execute the code safely
        exec_env = {}  # Separate environment for execution
        exec(source_code, {}, exec_env)

        # Get the captured execution output
        sys.stdout = old_stdout
        return captured_output.getvalue()

    except Exception as e:
        sys.stdout = old_stdout  # Restore stdout
        return f"Execution Error: {e}"
