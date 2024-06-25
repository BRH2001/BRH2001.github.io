import tkinter as tk
from tkinter import ttk
import subprocess
import os

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

        # Search for script files in current directory and its parent directories
        self.script_paths = self.find_script_files()

        # Create buttons dynamically based on found scripts
        for script, script_path in self.script_paths.items():
            button = tk.Button(button_frame, text=script, command=lambda path=script_path: self.run_program(path),
                               font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
            button.pack(pady=5)

        self.exit_button = tk.Button(button_frame, text="Afsluiten", command=self.root.quit,
                                     font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.exit_button.pack(pady=5)

    def find_script_files(self):
        script_files = {
            "Tekst Bewerker": self.find_file_in_directory("tekst-bewerker.py"),
            "Reken Machine": self.find_file_in_directory("reken-machine.py"),
            "Palindroom Controle": self.find_file_in_directory("Palindroom-Controle.py")
        }
        return {key: value for key, value in script_files.items() if value is not None}

    def find_file_in_directory(self, filename):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        # Check current directory and its parent directories
        while current_dir:
            file_path = os.path.join(current_dir, filename)
            if os.path.isfile(file_path):
                return file_path
            # Move to the parent directory
            current_dir = os.path.dirname(current_dir)
        return None

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
