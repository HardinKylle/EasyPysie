#compiler_ui.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
from compiler import compile_code  # Import the updated compiler

def run_compiler():
    # Get the source code from the text area
    source_code = source_text.get("1.0", tk.END).strip()

    # Run the compiler and capture execution output
    output = compile_code(source_code, target="python")  # Change target to "assembly" if needed

    # Display the final execution output in the GUI
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)

# Create the main window
root = tk.Tk()
root.title("EasyPysie Compiler")

# Create a frame for the source code input
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

# Label for source code
tk.Label(input_frame, text="Enter your source code:").pack(anchor="w")

# Scrolled text area for source code input
source_text = scrolledtext.ScrolledText(input_frame, width=80, height=15)
source_text.pack()

# Add a button to run the compiler
run_button = tk.Button(root, text="Compile", command=run_compiler)
run_button.pack(pady=5)

# Create a frame for output
output_frame = tk.Frame(root)
output_frame.pack(padx=10, pady=10)

tk.Label(output_frame, text="Compiler Output:").pack(anchor="w")
output_text = scrolledtext.ScrolledText(output_frame, width=80, height=10)
output_text.pack()

# Start the GUI event loop
root.mainloop()
