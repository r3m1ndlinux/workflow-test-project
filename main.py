import tkinter as tk
from tkinter import ttk

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operation = operation_var.get()
        
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            result = num1 / num2 if num2 != 0 else "Error: Div by 0"
        
        result_label.config(text=f"Result: {result}")
    except ValueError:
        result_label.config(text="Error: Invalid input")

# Create main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x250")

# Input fields
ttk.Label(root, text="Number 1:").pack(pady=5)
entry1 = ttk.Entry(root)
entry1.pack(pady=5)

ttk.Label(root, text="Number 2:").pack(pady=5)
entry2 = ttk.Entry(root)
entry2.pack(pady=5)

# Operation selector
ttk.Label(root, text="Operation:").pack(pady=5)
operation_var = tk.StringVar(value="+")
operations = ttk.Combobox(root, textvariable=operation_var, values=["+", "-", "*", "/"])
operations.pack(pady=5)

# Calculate button
calc_button = ttk.Button(root, text="Calculate", command=calculate)
calc_button.pack(pady=10)

# Result label
result_label = ttk.Label(root, text="Result: ", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()