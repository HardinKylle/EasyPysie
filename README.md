# EasyPysie Compiler

EasyPysie is a kid-friendly programming language and compiler designed to make coding fun and accessible for beginners. It features a simple syntax, colorful UI, and interactive commands that help kids learn programming concepts in an engaging way.

## Features

- **Kid-Friendly Syntax**: Commands like `say`, `ask`, `repeat`, and `check` make programming intuitive.
- **Interactive Input**: Prompts users for input using a GUI dialog.
- **Loops and Conditionals**: Supports `repeat`, `keep` (while), and `check` (if-else) constructs.
- **Functions**: Define reusable code blocks with `create` and return values using `give`.
- **Semantic Analysis**: Ensures code correctness with detailed error messages.
- **Intermediate Representation (IR)**: Converts code into an intermediate format for further processing.
- **Code Generation**: Outputs Python or assembly code from the IR.
- **GUI Interface**: A colorful and interactive GUI for writing and compiling code.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HardinKylle/EasyPysie
   cd EasyPysie
   ```

2. Install the required Python library `ply`:
   ```bash
   pip install ply
   ```

3. Run the GUI:
   ```bash
   python compiler_ui.py
   ```

## Usage

### Writing Code
Write your EasyPysie code in the provided text area in the GUI. Example:
```plaintext
name is ask("What's your name?");
say("Hello, " + name + "!");
repeat 3 {
   say("Welcome to the program, " + name + "!");
}
```

### Running Code
1. Click the **Compile** button to compile and execute your code.
2. View the output in the **Compiler Output** section.

### Supported Commands
- `say("message");` - Prints a message.
- `ask("prompt");` - Prompts the user for input.
- `repeat <number> { ... }` - Repeats a block of code.
- `check (condition) { ... } otherwise { ... }` - Conditional execution.
- `create functionName(params) { ... }` - Defines a function.
- `give value;` - Returns a value from a function.

## File Structure

- `lexer.py`: Tokenizes the EasyPysie code.
- `parser.py`: Parses the tokens into an Abstract Syntax Tree (AST).
- `semantic.py`: Performs semantic analysis on the AST.
- `ir_generator.py`: Generates Intermediate Representation (IR) code.
- `code_generator.py`: Converts IR into Python or assembly code.
- `compiler.py`: Orchestrates the compilation pipeline.
- `compiler_ui.py`: Provides the GUI for the compiler.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve EasyPysie.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to all contributors and educators who inspired the creation of EasyPysie.