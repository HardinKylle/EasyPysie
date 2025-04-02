import tkinter as tk
from tkinter import scrolledtext
from compiler import compile_code  # Import the updated compiler

def run_compiler():
    # Get the source code from the text area
    source_code = source_text.get("1.0", tk.END).strip()

    # Run the compiler and capture execution output
    output = compile_code(source_code, target="python")  # Change target to "assembly" if needed

    # Display the final execution output in the GUI
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state="disabled")

def show_commands():
    """
    Instead of using a messagebox, create a custom top-level window
    to display the kid-friendly commands with colorful formatting.
    """
    commands_window = tk.Toplevel(root)
    commands_window.title("Kid-Friendly Commands")
    commands_window.configure(bg="#e0f7fa")  # Light pink background

    # Big, bold title label
    title_label = tk.Label(
        commands_window,
        text="Kid-Friendly Commands",
        bg="#fce4ec",
        fg="#ad1457",
        font=("Comic Sans MS", 16, "bold")
    )
    title_label.pack(pady=(10, 5))

    # Scrolled text widget to display commands
    commands_text = scrolledtext.ScrolledText(
        commands_window,
        width=50,
        height=10,
        font=("Comic Sans MS", 12),
        bg="#ffffff",
        wrap=tk.WORD
    )
    commands_text.pack(pady=5, padx=10)

# Insert colorful/emoji-rich text
    commands_text.insert(tk.END, "👋 Hello, Kids! Here are some commands you can try:\n\n")
    commands_text.insert(tk.END, "💬 say(\"Your message\"): Prints a message.\n")
    commands_text.insert(tk.END, "❓ ask(): Prompts the user for input.\n")
    commands_text.insert(tk.END, "🔢 keep (<condition>) { ... }: Simple loops.\n")
    commands_text.insert(tk.END, "🔂 repeat \"word\" <number> times: Repeats a word a set number of times.\n")
    commands_text.insert(tk.END, "💪 create function_name(parameters) { ... }: Defines a function.\n")
    commands_text.insert(tk.END, "✅ check (condition) { ... } otherwise { ... }: Conditional checks.\n\n")
    commands_text.insert(tk.END, "Have fun coding! 🎉\n")

    # Make text read-only
    commands_text.config(state="disabled")

    # A friendly 'Close' button
    close_button = tk.Button(
        commands_window,
        text="Got it!",
        command=commands_window.destroy,
        bg="#2196f3",
        fg="white",
        font=("Comic Sans MS", 12, "bold")
    )
    close_button.pack(pady=10)

# Create the main window with a friendly theme
root = tk.Tk()
root.title("EasyPysie Compiler - Kid Edition")
root.configure(bg="#e0f7fa")

# Create a frame for the source code input
input_frame = tk.Frame(root, bg="#e0f7fa")
input_frame.pack(padx=10, pady=10)

# Label for source code
source_label = tk.Label(
    input_frame,
    text="Enter your source code:",
    bg="#e0f7fa",
    font=("Comic Sans MS", 12, "bold")
)
source_label.pack(anchor="w")

# Scrolled text area for source code input
source_text = scrolledtext.ScrolledText(
    input_frame,
    width=80,
    height=15,
    font=("Comic Sans MS", 11),
    bg="#ffffff"
)
source_text.pack()

# Frame for buttons
button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=5)

# Add a button to run the compiler
run_button = tk.Button(
    button_frame,
    text="Compile",
    command=run_compiler,
    font=("Comic Sans MS", 11),
    bg="#4caf50",
    fg="white"
)
run_button.grid(row=0, column=0, padx=5)

# Button to show kid-friendly commands
commands_button = tk.Button(
    button_frame,
    text="Show Commands",
    command=show_commands,
    font=("Comic Sans MS", 11),
    bg="#2196f3",
    fg="white"
)
commands_button.grid(row=0, column=1, padx=5)

# Create a frame for output
output_frame = tk.Frame(root, bg="#e0f7fa")
output_frame.pack(padx=10, pady=10)

output_label = tk.Label(
    output_frame,
    text="Compiler Output:",
    bg="#e0f7fa",
    font=("Comic Sans MS", 12, "bold")
)
output_label.pack(anchor="w")

output_text = scrolledtext.ScrolledText(
    output_frame,
    width=80,
    height=10,
    font=("Comic Sans MS", 11),
    bg="#ffffff",
    state="disabled"
)
output_text.pack()

# Start the GUI event loop
root.mainloop()
