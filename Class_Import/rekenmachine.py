import tkinter as tk
from tkinter import ttk

class Rekenmachine:
    """Deze klasse is een eenvoudige rekenmachine"""

    def __init__(self, a, b):
        """Initialiseer de rekenmachine"""
        self.first_number = a
        self.second_number = b

    def som(self):
        """Deze methode berekent de som van a en b"""
        som = self.first_number + self.second_number
        print('De som van ' + str(self.first_number) + ' en ' + str(self.second_number) + ' is ' + str(som))

    def verschil(self):
        """Deze methode berekent het verschil van a en b"""
        verschil = self.first_number - self.second_number
        print('Het verschil van ' + str(self.first_number) + ' en ' + str(self.second_number) + ' is ' + str(verschil))


    def product(self):
        """Deze methode berekent het product van a en b"""
        product = self.first_number * self.second_number
        print('Het product van ' + str(self.first_number) + ' en ' + str(self.second_number) + ' is ' + str(product))

    def change_numbers(self, new_a, new_b):
        """Deze methode verandert de waarden van a en b"""
        self.first_number = new_a
        self.second_number = new_b

class CalculatorUI:
    def __init__(self, calculator):
        self.calculator = calculator

        self.root = tk.Tk()
        self.root.title("Rekenmachine")
        self.root.geometry("400x150")  # Set initial window size

        # Configure style for background gradient
        style = ttk.Style()
        style.configure("TFrame", background="#000000")

        # Increase font size for scaled-up elements.
        font_size = 14

        # Create frame with gradient background
        self.frame = ttk.Frame(self.root, style="TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Label
        self.label = tk.Label(self.frame, text="Voer twee getallen in:", font=("Arial", font_size), fg="#FFFFFF", bg="#000000")
        self.label.pack()

        # Entry fields for numbers
        entry_frame = tk.Frame(self.frame, bg="#000000")
        entry_frame.pack()

        self.first_number_entry = tk.Entry(entry_frame, font=("Arial", font_size), width=10)
        self.first_number_entry.pack(side=tk.LEFT, padx=5)

        self.second_number_entry = tk.Entry(entry_frame, font=("Arial", font_size), width=10)
        self.second_number_entry.pack(side=tk.RIGHT, padx=5)

        # Buttons
        button_frame = tk.Frame(self.frame, bg="#000000")
        button_frame.pack()

        self.sum_button = tk.Button(button_frame, text="Som", command=self.calculate_sum, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.sum_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.difference_button = tk.Button(button_frame, text="Verschil", command=self.calculate_difference, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.difference_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.product_button = tk.Button(button_frame, text="Product", command=self.calculate_product, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.product_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Result label
        self.result_label = tk.Label(self.frame, text="", font=("Arial", font_size), fg="#FFFFFF", bg="#000000")
        self.result_label.pack()

    def calculate_sum(self):
        try:
            first_number = float(self.first_number_entry.get())
            second_number = float(self.second_number_entry.get())
            self.calculator.change_numbers(first_number, second_number)
            self.calculator.som()
            result = first_number + second_number
            self.result_label.config(text=f"De som van {first_number} en {second_number} is {result}", fg="green")
        except ValueError:
            self.result_label.config(text="Voer geldige getallen in.", fg="red")

    def calculate_difference(self):
        try:
            first_number = float(self.first_number_entry.get())
            second_number = float(self.second_number_entry.get())
            self.calculator.change_numbers(first_number, second_number)
            self.calculator.verschil()
            result = first_number - second_number
            self.result_label.config(text=f"Het verschil van {first_number} en {second_number} is {result}", fg="green")
        except ValueError:
            self.result_label.config(text="Voer geldige getallen in.", fg="red")

    def calculate_product(self):
        try:
            first_number = float(self.first_number_entry.get())
            second_number = float(self.second_number_entry.get())
            self.calculator.change_numbers(first_number, second_number)
            self.calculator.product()
            result = first_number * second_number
            self.result_label.config(text=f"Het product van {first_number} en {second_number} is {result}", fg="green")
        except ValueError:
            self.result_label.config(text="Voer geldige getallen in.", fg="red")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    calculator = Rekenmachine(0, 0)
    app = CalculatorUI(calculator)
    app.run()
