import tkinter as tk
import math

class StyledCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("280x440")
        self.root.configure(bg="#1e1e2f")
        self.root.resizable(False, False)
        self.expression = ""
        self.result = ""
        self.memory = 0.0
        self.angle_mode = "DEG"

        self.input_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.status_var = tk.StringVar()

        # Status display
        self.status_label = tk.Label(root, textvariable=self.status_var,
            font=("Segoe UI", 10), bg="#1e1e2f", fg="#aaaaaa", anchor="w", pady=5)
        self.status_label.pack(fill="x")

        # Input and result display
        tk.Label(root, textvariable=self.input_var, font=("Segoe UI", 18),
                 bg="#1e1e2f", fg="#ffffff", anchor="e", height=2).pack(fill="both")
        tk.Label(root, textvariable=self.result_var, font=("Segoe UI", 24),
                 bg="#2e2e3f", fg="#00ffcc", anchor="e", height=2).pack(fill="both")

        self.create_buttons()
        self.bind_keys()
        self.update_status()

    def create_buttons(self):
        layout = [
            ['C', 'MC', 'MR', 'M+', 'M-'],
            ['π', 'e', 'cos', 'tan', 'exp'],
            ['(', ')', '^', '!', 'DEG'],
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', 'log'],
            ['1', '2', '3', '-', 'sin'],
            ['0', '.', '=', '+', '⌫'],
        ]

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(expand=True, fill="both")

        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                if not char:
                    continue
                color = self.get_color(char)
                btn = tk.Button(frame, text=char, font=("Segoe UI", 11),
                                bg=color['bg'], fg=color['fg'],
                                activebackground=color['activebg'],
                                activeforeground=color['activefg'],
                                width=3, height=1, relief="flat",
                                command=lambda ch=char: self.on_click(ch))
                btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

        for i in range(6):
            frame.columnconfigure(i, weight=1)
        for i in range(len(layout)):
            frame.rowconfigure(i, weight=1)

    def get_color(self, char):
        if char in "0123456789.":
            return {"bg": "#2c3e50", "fg": "#ffffff", "activebg": "#34495e", "activefg": "#00ffcc"}
        elif char in "+-*/^=!()":
            return {"bg": "#8e44ad", "fg": "#ffffff", "activebg": "#9b59b6", "activefg": "#ffffff"}
        elif char in ["C", "⌫", "="]:
            return {"bg": "#e74c3c", "fg": "#ffffff", "activebg": "#c0392b", "activefg": "#ffffff"}
        elif char in ["M+", "M-", "MR", "MC"]:
            return {"bg": "#f39c12", "fg": "#ffffff", "activebg": "#e67e22", "activefg": "#ffffff"}
        elif char == "DEG" or char == "RAD":
            return {"bg": "#2980b9", "fg": "#ffffff", "activebg": "#3498db", "activefg": "#ffffff"}
        else:
            return {"bg": "#16a085", "fg": "#ffffff", "activebg": "#1abc9c", "activefg": "#ffffff"}

    def bind_keys(self):
        self.root.bind("<Return>", lambda e: self.on_click('='))
        self.root.bind("<KP_Enter>", lambda e: self.on_click('='))
        self.root.bind("<BackSpace>", lambda e: self.on_click('⌫'))
        self.root.bind("<Escape>", lambda e: self.on_click('C'))

        for key in "0123456789+-*/().":
            self.root.bind(key, lambda e, k=key: self.on_click(k))

        numpad_keys = {
            "KP_0": "0", "KP_1": "1", "KP_2": "2", "KP_3": "3",
            "KP_4": "4", "KP_5": "5", "KP_6": "6", "KP_7": "7",
            "KP_8": "8", "KP_9": "9", "KP_Decimal": ".", "KP_Add": "+",
            "KP_Subtract": "-", "KP_Multiply": "*", "KP_Divide": "/"
        }
        for keysym, char in numpad_keys.items():
            self.root.bind(f"<{keysym}>", lambda e, k=char: self.on_click(k))

    def update_status(self):
        mode_char = "D" if self.angle_mode == "DEG" else "R"
        self.status_var.set(f" M = {self.memory:.2f}   Mode: {mode_char}")

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
            self.result = ""
        elif char == '⌫':
            self.expression = self.expression[:-1]
        elif char == '=':
            try:
                expr = self.expression.replace('π', str(math.pi)).replace('e', str(math.e))
                expr = expr.replace('^', '**')
                expr = expr.replace('sqrt', 'math.sqrt')
                expr = expr.replace('log', 'math.log10')
                if self.angle_mode == "DEG":
                    expr = expr.replace('sin', 'math.sin(math.radians')
                    expr = expr.replace('cos', 'math.cos(math.radians')
                    expr = expr.replace('tan', 'math.tan(math.radians')
                    close_paren = ')' if 'math.radians' in expr else ''
                else:
                    expr = expr.replace('sin', 'math.sin(')
                    expr = expr.replace('cos', 'math.cos(')
                    expr = expr.replace('tan', 'math.tan(')
                    close_paren = ''
                expr = expr.replace('exp', 'math.exp')
                if '!' in expr:
                    num = expr.split('!')[0]
                    expr = f"math.factorial(int({num}))"
                    close_paren = ''
                self.result = str(eval(expr + close_paren))
            except Exception as e:
                self.result = "Error"
        elif char == 'DEG' or char == 'RAD':
            self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        elif char == 'M+':
            try:
                self.memory += float(eval(self.result))
            except:
                pass
        elif char == 'M-':
            try:
                self.memory -= float(eval(self.result))
            except:
                pass
        elif char == 'MR':
            self.expression += str(self.memory)
        elif char == 'MC':
            self.memory = 0.0
        else:
            self.expression += char

        self.input_var.set(self.expression)
        self.result_var.set(self.result)
        self.update_status()

# Run the app
root = tk.Tk()
icon = tk.PhotoImage(file="calc.png")  # PNG works on Linux
root.iconphoto(True, icon)
app = StyledCalc(root)
root.mainloop()

