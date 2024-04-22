import tkinter as tk
from tkinter import ttk

class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Editor")
        self.root.geometry("400x250")  # Set initial window size

        # Configure style for background gradient
        style = ttk.Style()
        style.configure("TFrame", background="#000000")

        # Increase font size for scaled-up elements
        font_size = 14

        # Create frame with gradient background
        self.frame = ttk.Frame(self.root, style="TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Label
        self.label = tk.Label(self.frame, text="Enter text:", font=("Arial", font_size), fg="#FFFFFF", bg="#000000")
        self.label.pack()

        # Entry field
        self.text_entry = tk.Entry(self.frame, font=("Arial", font_size))
        self.text_entry.pack()

        # Buttons
        button_frame = tk.Frame(self.frame, bg="#000000")
        button_frame.pack()

        self.full_case_button = tk.Button(button_frame, text="Full Case", command=self.full_case_text, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.full_case_button.pack(side=tk.LEFT, pady=5)

        self.small_case_button = tk.Button(button_frame, text="Small Case", command=self.small_case_text, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.small_case_button.pack(side=tk.LEFT, pady=5)

        self.reverse_button = tk.Button(button_frame, text="Reverse", command=self.reverse_text, font=("Arial", font_size), bg="#808080", fg="#FFFFFF")
        self.reverse_button.pack(side=tk.LEFT, pady=5)

    def full_case_text(self):
        text = self.text_entry.get()
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, text.upper())

    def small_case_text(self):
        text = self.text_entry.get()
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, text.lower())

    def reverse_text(self):
        text = self.text_entry.get()
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, text[::-1])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    editor = TextEditor()
    editor.run()
