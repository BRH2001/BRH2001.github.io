import tkinter as tk


class Textgen:

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Data Encrypter")

        self.frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=5)
        self.frm_form.pack()

        self.Labels = [
            "text 1",
            "text 2",
            "text 3",
        ]

        self.text_1 = None
        self.text_2 = None
        self.text_3 = None

    def _save_text(self):

        text_file_1 = open("nl_text_1.txt", "w")
        text_file_1.write(self.text_1.get(1.0, tk.END))
        text_file_1.close()

        text_file_2 = open("nl_text_2.txt", "w")
        text_file_2.write(self.text_2.get(1.0, tk.END))
        text_file_2.close()

        text_file_3 = open("nl_text_3.txt", "w")
        text_file_3.write(self.text_3.get(1.0, tk.END))
        text_file_3.close()

        self.window.destroy()

    def run_gen(self):
        for count, text in enumerate(self.Labels):
            label = tk.Label(master=self.frm_form, text=text)
            label.grid(row=count, column=0, sticky="e")

        self.text_1 = tk.Text(master=self.frm_form, width=50, height=10)
        self.text_1.grid(row=0, column=1)

        self.text_2 = tk.Text(master=self.frm_form, width=50, height=10)
        self.text_2.grid(row=1, column=1)

        self.text_3 = tk.Text(master=self.frm_form, width=50, height=10)
        self.text_3.grid(row=2, column=1)

        frm_buttons = tk.Frame()
        frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

        submit_button = tk.Button(master=frm_buttons, text="Submit", command=self._save_text)
        submit_button.pack(side=tk.RIGHT, padx=10, ipadx=10)

        self.window.mainloop()


if __name__ == "__main__":
    textgen = Textgen()
    textgen.run_gen()
