import customtkinter as ctk
import tkinter.filedialog as filedialog
import random
import string
import hashlib
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ToolkitPro")
        self.geometry("600x450")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.tab_view = ctk.CTkTabview(self, width=250)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view.add("Password Generator")
        self.tab_view.add("File Hasher")
        self.tab_view.add("Notes")

        self.create_password_generator_tab()
        self.create_file_hasher_tab()
        self.create_notes_tab()

    def create_password_generator_tab(self):
        tab = self.tab_view.tab("Password Generator")
        tab.grid_columnconfigure(0, weight=1)

        # Password display
        self.password_entry = ctk.CTkEntry(tab, font=("", 14), width=300)
        self.password_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew", columnspan=2)

        self.copy_button = ctk.CTkButton(tab, text="Copy", command=self.copy_password)
        self.copy_button.grid(row=0, column=2, padx=10, pady=(20, 10))

        # Options Frame
        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        options_frame.grid_columnconfigure(1, weight=1)

        # Length
        ctk.CTkLabel(options_frame, text="Length:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.length_var = ctk.IntVar(value=16)
        self.length_slider = ctk.CTkSlider(options_frame, from_=8, to=64, number_of_steps=56, variable=self.length_var, command=lambda v: self.length_label.configure(text=f"{int(v)}"))
        self.length_slider.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.length_label = ctk.CTkLabel(options_frame, text="16")
        self.length_label.grid(row=0, column=2, padx=10, pady=10)

        # Checkboxes
        self.uppercase_var = ctk.BooleanVar(value=True)
        self.numbers_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(options_frame, text="Uppercase (A-Z)", variable=self.uppercase_var).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkCheckBox(options_frame, text="Numbers (0-9)", variable=self.numbers_var).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkCheckBox(options_frame, text="Symbols (!@#$)", variable=self.symbols_var).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Generate Button
        generate_button = ctk.CTkButton(tab, text="Generate Password", command=self.generate_password)
        generate_button.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

    def create_file_hasher_tab(self):
        tab = self.tab_view.tab("File Hasher")
        tab.grid_columnconfigure(0, weight=1)
        
        # File selection
        self.file_path_var = ctk.StringVar()
        file_label = ctk.CTkLabel(tab, text="No file selected.", wraplength=500)
        file_label.grid(row=0, column=0, padx=20, pady=(10,0), sticky="w")
        select_button = ctk.CTkButton(tab, text="Select File", command=lambda: self.select_file(file_label))
        select_button.grid(row=1, column=0, padx=20, pady=(5,10), sticky="w")

        # Hash options
        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        options_frame.grid_columnconfigure(1, weight=1)

        self.hash_algo_var = ctk.StringVar(value="SHA-256")
        ctk.CTkLabel(options_frame, text="Algorithm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        hash_menu = ctk.CTkOptionMenu(options_frame, variable=self.hash_algo_var, values=["SHA-256", "MD5", "SHA-1"])
        hash_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Calculate button
        calc_button = ctk.CTkButton(tab, text="Calculate Hash", command=self.calculate_hash)
        calc_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Result display
        self.hash_result_entry = ctk.CTkEntry(tab, font=("", 12), width=400)
        self.hash_result_entry.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")

    def create_notes_tab(self):
        tab = self.tab_view.tab("Notes")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        notes_textbox = ctk.CTkTextbox(tab, wrap="word")
        notes_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def generate_password(self):
        length = self.length_var.get()
        use_upper = self.uppercase_var.get()
        use_numbers = self.numbers_var.get()
        use_symbols = self.symbols_var.get()

        chars = string.ascii_lowercase
        if use_upper:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += string.punctuation

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
                while chunk := f.read(8192):
                    hasher.update(chunk)
            
            self.hash_result_entry.delete(0, "end")
            self.hash_result_entry.insert(0, hasher.hexdigest())

        except Exception as e:
            self.hash_result_entry.delete(0, "end")
            self.hash_result_entry.insert(0, f"Error: {e}")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()