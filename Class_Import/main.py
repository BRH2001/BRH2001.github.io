import tkinter as tk
from tkinter import ttk
import subprocess

class HoofdMenuUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hoofdmenu")
        self.root.geometry("450x250")  # Set initial window size

        # Configure style for background gradient
        style = ttk.Style()
        style.configure("TFrame", background="#000000")

        # Increase font size for scaled-up elements
        font_size = 13

        # Create frame with gradient background
        self.frame = ttk.Frame(self.root, style="TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Label
        self.label = tk.Label(self.frame, text="Hoofdmenu", font=("Arial", font_size), fg="#FFFFFF", bg="#000000")
        self.label.pack()

        # Buttons
        button_frame = tk.Frame(self.frame, bg="#000000")
        button_frame.pack()
        
        self.text_editor_button = tk.Button(button_frame, text="Tekst Bewerker", command=self.run_text_editor, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.text_editor_button.pack(pady=5)

        self.calculator_button = tk.Button(button_frame, text="Reken Machine", command=self.run_calculator, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.calculator_button.pack(pady=5)

        self.palindrome_button = tk.Button(button_frame, text="Palindroom Controle", command=self.run_palindrome, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.palindrome_button.pack(pady=5)

        self.exit_button = tk.Button(button_frame, text="Afsluiten", command=self.root.quit, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.exit_button.pack(pady=5)

    def run_palindrome(self):
        self.run_program("Palindroom-Controle.py")

    def run_calculator(self):
        self.run_program("reken-machine.py")

    def run_text_editor(self):
        self.run_program("tekst-bewerker.py")

    def run_program(self, program_file):
        try:
            subprocess.run(["python", program_file])
        except FileNotFoundError:
            print(f"Fout: {program_file} niet gevonden.")
        except Exception as e:
            print(f"Er is een fout opgetreden bij het uitvoeren van {program_file}: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HoofdMenuUI()
    app.run()
