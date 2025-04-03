# Import necessary modules and components.
import tkinter as tk
from tkinter import scrolledtext
from compiler import compile_code  # Import the updated compiler

def run_compiler():
    """
    Compile the source code entered in the UI and display the output.
    """
    source_code = source_text.get("1.0", tk.END).strip()
    output = compile_code(source_code, target="python")  # Change target to "assembly" if needed
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state="disabled")

def show_commands():
    """
    Display a window with a list of kid-friendly commands.
    """
    commands_window = tk.Toplevel(root)
    commands_window.title("Kid-Friendly Commands")
    commands_window.configure(bg="#e0f7fa")
    commands_window.geometry("500x400")

    title_label = tk.Label(
        commands_window,
        text="Kid-Friendly Commands",
        bg="#fce4ec",
        fg="#ad1457",
        font=("Comic Sans MS", 16, "bold")
    )
    title_label.pack(pady=10)

    commands_text = scrolledtext.ScrolledText(
        commands_window,
        width=50,
        height=10,
        font=("Comic Sans MS", 12),
        bg="#ffffff",
        wrap=tk.WORD
    )
    commands_text.pack(pady=5, padx=10)

    commands_text.insert(tk.END, "👋 Hello, Kids! Here are some commands you can try:\n\n")
    commands_text.insert(tk.END, "💬 say(\"Your message\"): Prints a message.\n")
    commands_text.insert(tk.END, "❓ ask(): Prompts the user for input.\n")
    commands_text.insert(tk.END, "✅ check (condition) { ... } otherwise { ... }: Conditional checks.\n\n")
    commands_text.insert(tk.END, "🔢 keep (<condition>) { ... }: Simple loops.\n")
    commands_text.insert(tk.END, "🔂 repeat \"word\" <number> times: Repeats a word a set number of times.\n")
    commands_text.insert(tk.END, "💪 create function_name(parameters) { ... }: Defines a function.\n")
    commands_text.insert(tk.END, "Have fun coding! 🎉\n")

    commands_text.config(state="disabled")

    close_button = tk.Button(
        commands_window,
        text="Got it!",
        command=commands_window.destroy,
        bg="#2196f3",
        fg="white",
        font=("Comic Sans MS", 12, "bold")
    )
    close_button.pack(pady=10)

# Create the main application window.
root = tk.Tk()
root.title("EasyPysie Compiler - Kid Edition")
root.configure(bg="#e0f7fa")
root.state("zoomed")  # Make the window full screen

input_frame = tk.Frame(root, bg="#e0f7fa")
input_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

source_label = tk.Label(
    input_frame,
    text="Enter your source code:",
    bg="#e0f7fa",
    font=("Comic Sans MS", 14, "bold")
)
source_label.pack(anchor="w")

source_text = scrolledtext.ScrolledText(
    input_frame,
    width=100,
    height=20,
    font=("Comic Sans MS", 12),
    bg="#ffffff"
)
source_text.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=10)

run_button = tk.Button(
    button_frame,
    text="Compile",
    command=run_compiler,
    font=("Comic Sans MS", 12, "bold"),
    bg="#4caf50",
    fg="white",
    width=12
)
run_button.grid(row=0, column=0, padx=10)

commands_button = tk.Button(
    button_frame,
    text="Show Commands",
    command=show_commands,
    font=("Comic Sans MS", 12, "bold"),
    bg="#2196f3",
    fg="white",
    width=12
)
commands_button.grid(row=0, column=1, padx=10)

output_frame = tk.Frame(root, bg="#e0f7fa")
output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

output_label = tk.Label(
    output_frame,
    text="Compiler Output:",
    bg="#e0f7fa",
    font=("Comic Sans MS", 14, "bold")
)
output_label.pack(anchor="w")

output_text = scrolledtext.ScrolledText(
    output_frame,
    width=100,
    height=10,
    font=("Comic Sans MS", 12),
    bg="#ffffff",
    state="disabled"
)
output_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()
