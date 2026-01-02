import customtkinter as ctk
import tkinter.filedialog as filedialog
import random
import string
import hashlib
import os
import sys

# --- Tooltip Class for Hover Instructions ---
class Tooltip(ctk.CTkToplevel):
    def __init__(self, widget, text):
        super().__init__(widget)
        self.widget = widget
        self.text = text
        
        self.withdraw() # Hide initially
        self.overrideredirect(True) # No window decorations
        
        self.label = ctk.CTkLabel(self, text=self.text, corner_radius=5,
                                  fg_color=("#333333", "#444444"), text_color="white",
                                  padx=10, pady=5)
        self.label.pack()
        
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Button-1>", self.hide_tooltip) # Hide on click

    def show_tooltip(self, event):
        self.deiconify()
        x = self.widget.winfo_rootx() + (self.widget.winfo_width() / 2) - (self.label.winfo_width() / 2)
        y = self.widget.winfo_rooty() - self.label.winfo_height() - 5
        self.geometry(f"+{int(x)}+{int(y)}")

    def hide_tooltip(self, event):
        self.withdraw()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ToolkitPro")
        self.geometry("700x550") # Increased size for new tools
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.tab_view = ctk.CTkTabview(self, width=250)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Add new tabs first to feature them
        self.tab_view.add("Calculator")
        self.tab_view.add("Unit Converter")
        self.tab_view.add("Password Generator")
        self.tab_view.add("File Hasher")
        self.tab_view.add("Notes")

        # Create all tabs
        self.create_calculator_tab()
        self.create_unit_converter_tab()
        self.create_password_generator_tab()
        self.create_file_hasher_tab()
        self.create_notes_tab()
        
        self.tab_view.set("Calculator") # Set default tab

    def create_password_generator_tab(self):
        tab = self.tab_view.tab("Password Generator")
        tab.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(tab, font=("", 14), width=300)
        self.password_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew", columnspan=2)
        Tooltip(self.password_entry, "Generated password will appear here")

        self.copy_button = ctk.CTkButton(tab, text="Copy", command=self.copy_password)
        self.copy_button.grid(row=0, column=2, padx=10, pady=(20, 10))
        Tooltip(self.copy_button, "Copy the password to the clipboard")

        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        options_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(options_frame, text="Length:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.length_var = ctk.IntVar(value=16)
        self.length_slider = ctk.CTkSlider(options_frame, from_=8, to=64, number_of_steps=56, variable=self.length_var, command=lambda v: self.length_label.configure(text=f"{int(v)}"))
        self.length_slider.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        Tooltip(self.length_slider, "Set the desired password length (8-64)")
        self.length_label = ctk.CTkLabel(options_frame, text="16")
        self.length_label.grid(row=0, column=2, padx=10, pady=10)

        self.uppercase_var = ctk.BooleanVar(value=True)
        self.numbers_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(options_frame, text="Uppercase (A-Z)", variable=self.uppercase_var).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkCheckBox(options_frame, text="Numbers (0-9)", variable=self.numbers_var).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkCheckBox(options_frame, text="Symbols (!@#$)", variable=self.symbols_var).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        generate_button = ctk.CTkButton(tab, text="Generate Password", command=self.generate_password)
        generate_button.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
        Tooltip(generate_button, "Generate a new password with the selected options")

    def create_file_hasher_tab(self):
        tab = self.tab_view.tab("File Hasher")
        tab.grid_columnconfigure(0, weight=1)
        
        self.file_path_var = ctk.StringVar()
        file_label = ctk.CTkLabel(tab, text="No file selected.", wraplength=500)
        file_label.grid(row=0, column=0, padx=20, pady=(10,0), sticky="w")
        select_button = ctk.CTkButton(tab, text="Select File", command=lambda: self.select_file(file_label))
        select_button.grid(row=1, column=0, padx=20, pady=(5,10), sticky="w")
        Tooltip(select_button, "Select a file to calculate its checksum hash")

        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        options_frame.grid_columnconfigure(1, weight=1)

        self.hash_algo_var = ctk.StringVar(value="SHA-256")
        ctk.CTkLabel(options_frame, text="Algorithm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        hash_menu = ctk.CTkOptionMenu(options_frame, variable=self.hash_algo_var, values=["SHA-256", "MD5", "SHA-1"])
        hash_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        Tooltip(hash_menu, "Select the hashing algorithm")

        calc_button = ctk.CTkButton(tab, text="Calculate Hash", command=self.calculate_hash)
        calc_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        Tooltip(calc_button, "Run the hash calculation on the selected file")
        
        self.hash_result_entry = ctk.CTkEntry(tab, font=("", 12), width=400)
        self.hash_result_entry.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")
        Tooltip(self.hash_result_entry, "The calculated hash will be displayed here")

    def create_notes_tab(self):
        tab = self.tab_view.tab("Notes")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        notes_textbox = ctk.CTkTextbox(tab, wrap="word")
        notes_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        Tooltip(notes_textbox, "A simple scratchpad for your notes.")

    def create_calculator_tab(self):
        tab = self.tab_view.tab("Calculator")
        tab.grid_columnconfigure((0, 1, 2, 3), weight=1)
        tab.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)

        self.calc_expression = ""
        self.calc_display_var = ctk.StringVar()
        
        display = ctk.CTkEntry(tab, textvariable=self.calc_display_var, font=("", 24), justify="right", state="readonly")
        display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="ew")
        Tooltip(display, "Calculator display")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
            ('=', 5, 0)
        ]

        for (text, row, col) in buttons:
            if text == 'C':
                btn = ctk.CTkButton(tab, text=text, command=self.clear_calc_display)
                Tooltip(btn, "Clear the display")
            elif text == '=':
                btn = ctk.CTkButton(tab, text=text, command=self.calculate_result, fg_color="#24a0ed", hover_color="#1f8ad1")
                btn.grid(row=row, column=col, columnspan=4, padx=5, pady=5, sticky="nsew")
                Tooltip(btn, "Calculate the result")
                continue
            else:
                btn = ctk.CTkButton(tab, text=text, command=lambda t=text: self.on_calc_button_press(t))
            
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def create_unit_converter_tab(self):
        tab = self.tab_view.tab("Unit Converter")
        tab.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.conversions = {
            "Length": {"Meters": 1, "Kilometers": 1000, "Miles": 1609.34, "Feet": 0.3048, "Inches": 0.0254},
            "Weight": {"Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495},
            "Temperature": {"Celsius": 0, "Fahrenheit": 0, "Kelvin": 0}
        }
        
        ctk.CTkLabel(tab, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.conv_category_var = ctk.StringVar(value="Length")
        category_menu = ctk.CTkOptionMenu(tab, variable=self.conv_category_var, values=list(self.conversions.keys()), command=self.update_units)
        category_menu.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        Tooltip(category_menu, "Select the type of unit to convert")

        # Input Frame
        input_frame = ctk.CTkFrame(tab)
        input_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        self.conv_from_unit_var = ctk.StringVar()
        self.from_unit_menu = ctk.CTkOptionMenu(input_frame, variable=self.conv_from_unit_var, command=lambda _: self.convert_units())
        self.from_unit_menu.grid(row=0, column=0, padx=10, pady=10)
        
        self.conv_input_var = ctk.StringVar()
        self.conv_input_entry = ctk.CTkEntry(input_frame, textvariable=self.conv_input_var)
        self.conv_input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.conv_input_var.trace_add("write", lambda *args: self.convert_units())

        # Output Frame
        output_frame = ctk.CTkFrame(tab)
        output_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        output_frame.grid_columnconfigure(1, weight=1)
        
        self.conv_to_unit_var = ctk.StringVar()
        self.to_unit_menu = ctk.CTkOptionMenu(output_frame, variable=self.conv_to_unit_var, command=lambda _: self.convert_units())
        self.to_unit_menu.grid(row=0, column=0, padx=10, pady=10)

        self.conv_result_label = ctk.CTkLabel(output_frame, text="Result", font=("", 14))
        self.conv_result_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.update_units() # Initialize unit menus

    def generate_password(self):
        length = self.length_var.get()
        use_upper = self.uppercase_var.get()
        use_numbers = self.numbers_var.get()
        use_symbols = self.symbols_var.get()

        chars = string.ascii_lowercase
        if use_upper: chars += string.ascii_uppercase
        if use_numbers: chars += string.digits
        if use_symbols: chars += string.punctuation

        if not chars:
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, "Select at least one character set")
            return

        password = "".join(random.choice(chars) for _ in range(length))
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

    def copy_password(self):
        self.clipboard_clear()
        self.clipboard_append(self.password_entry.get())

    def select_file(self, label_widget):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.file_path_var.set(filepath)
            label_widget.configure(text=os.path.basename(filepath))
        else:
            self.file_path_var.set("")
            label_widget.configure(text="No file selected.")

    def calculate_hash(self):
        filepath = self.file_path_var.get()
        if not filepath:
            self.hash_result_entry.delete(0, "end")
            self.hash_result_entry.insert(0, "Please select a file first.")
            return

        algo = self.hash_algo_var.get().lower()
        hasher = hashlib.new(algo)
        
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192): hasher.update(chunk)
            self.hash_result_entry.delete(0, "end")
            self.hash_result_entry.insert(0, hasher.hexdigest())
        except Exception as e:
            self.hash_result_entry.delete(0, "end")
            self.hash_result_entry.insert(0, f"Error: {e}")

    def on_calc_button_press(self, symbol):
        self.calc_expression += str(symbol)
        self.calc_display_var.set(self.calc_expression)

    def calculate_result(self):
        try:
            # IMPORTANT: eval() is a security risk if used with untrusted input.
            # Here it's reasonably safe as input only comes from trusted buttons.
            result = str(eval(self.calc_expression))
            self.calc_display_var.set(result)
            self.calc_expression = result
        except:
            self.calc_display_var.set("Error")
            self.calc_expression = ""

    def clear_calc_display(self):
        self.calc_expression = ""
        self.calc_display_var.set("")
        
    def update_units(self, *args):
        category = self.conv_category_var.get()
        units = list(self.conversions[category].keys())
        self.conv_from_unit_var.set(units[0])
        self.conv_to_unit_var.set(units[1] if len(units) > 1 else units[0])
        
        self.from_unit_menu.configure(values=units)
        self.to_unit_menu.configure(values=units)
        self.convert_units()

    def convert_units(self):
        try:
            input_val = float(self.conv_input_var.get())
            from_unit = self.conv_from_unit_var.get()
            to_unit = self.conv_to_unit_var.get()
            category = self.conv_category_var.get()

            if category == "Temperature":
                # Special handling for temperature
                if from_unit == "Celsius":
                    if to_unit == "Fahrenheit": result = (input_val * 9/5) + 32
                    elif to_unit == "Kelvin": result = input_val + 273.15
                    else: result = input_val
                elif from_unit == "Fahrenheit":
                    if to_unit == "Celsius": result = (input_val - 32) * 5/9
                    elif to_unit == "Kelvin": result = (input_val - 32) * 5/9 + 273.15
                    else: result = input_val
                elif from_unit == "Kelvin":
                    if to_unit == "Celsius": result = input_val - 273.15
                    elif to_unit == "Fahrenheit": result = (input_val - 273.15) * 9/5 + 32
                    else: result = input_val
            else:
                # Standard conversion using base unit (Meters/Kilograms)
                base_value = input_val * self.conversions[category][from_unit]
                result = base_value / self.conversions[category][to_unit]

            self.conv_result_label.configure(text=f"{result:.4f}")
        except (ValueError, ZeroDivisionError):
            self.conv_result_label.configure(text="Result") # Reset on invalid input
        except Exception:
            self.conv_result_label.configure(text="Error")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()