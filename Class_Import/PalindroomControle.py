import tkinter as tk
from tkinter import ttk

class PalindromeCheckerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Palindroom Controle")
        self.root.geometry("400x150")

        style = ttk.Style()
        style.configure("TFrame", background="#000000")

        font_size = 14

        self.frame = ttk.Frame(self.root, style="TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Voer een woord in:", font=("Arial", font_size), fg="#FFFFFF", bg="#000000")
        self.label.pack()

        self.word_entry = tk.Entry(self.frame, font=("Arial", font_size))
        self.word_entry.pack()

        self.check_button = tk.Button(self.frame, text="Controleren", command=self.check_palindrome, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.check_button.pack(pady=10)

        self.result_label = tk.Label(self.frame, text="", font=("Arial", font_size), fg="#FFFFFF", bg="#000000")
        self.result_label.pack()

    def check_palindrome(self):
        word = self.word_entry.get()

        if not word.isalpha():
            self.result_label.config(text="Invoerwoord mag alleen letters bevatten.", fg="red")
        else:
            checker = PalindromeChecker()
            if checker.check(word):
                self.result_label.config(text=f'"{word}" is een palindroom!', fg="green")
                self.word_entry.delete(0, tk.END)
                self.word_entry.insert(0, word.upper())
            else:
                self.result_label.config(text=f'"{word}" is geen palindroom.', fg="red")

    def run(self):
        self.root.mainloop()

class PalindromeChecker:
    def __init__(self):
        pass

    def check(self, word):
        if not word.isalpha():
            raise ValueError("Invoerwoord mag alleen letters bevatten.")

        word = word.lower()

        return word == word[::-1]

if __name__ == "__main__":
    app = PalindromeCheckerUI()
    app.run()
