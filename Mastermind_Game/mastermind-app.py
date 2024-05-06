import tkinter as tk
import random

# Define colors
WHITE = "white"
BLACK = "black"
RED = "red"
DARK_GREY = "#333333"
LIGHT_GREY = "#CCCCCC"

# Define constants
ROW_SIZE = 50
COLUMN_SIZE = 50
DOT_RADIUS = 5
MAX_ATTEMPTS = 12
INITIAL_POINTS = 13
GUESS_TIMEOUT = 6  

class MastermindGame:
    def __init__(self, root, code_length=4, time_limit=False):
        self.colors_4 = ["red", "yellow", "green", "blue", "purple", "pink"]
        self.colors_6 = ["red", "yellow", "green", "blue", "purple", "pink", "#FF4500", "brown"]
        self.secret_code = random.sample(self.colors_4 if code_length == 4 else self.colors_6, k=code_length)
        self.points = INITIAL_POINTS
        self.attempts_left = MAX_ATTEMPTS
        self.game_over = False  
        self.time_limit = time_limit

        self.root = root
        self.root.title("Mastermind")
        self.root.configure(bg=DARK_GREY)

        # Set the initial window size and position
        window_width = 20 * COLUMN_SIZE + 600  
        window_height = MAX_ATTEMPTS * ROW_SIZE + 350
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2  
        y_coordinate = (screen_height - window_height) // 6
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Adjust window size and grid dimensions for 6 colors
        if code_length == 6:
            window_width = 14 * COLUMN_SIZE + 900
            self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.create_board(code_length)
        self.create_feedback_grid(code_length)

        # Set current row index
        self.current_row_index = 0

        # Initialize chosen colors for each row
        self.chosen_colors = []

        # Display initial points
        self.points_label = tk.Label(self.root, text=f"Points: {self.points}", bg=BLACK, fg=WHITE)
        self.points_label.place(x=566 // 0.6, y=root.winfo_screenheight() - 212)
        self.create_color_palette()

        # Initialize timer variables based on code_length
        if code_length == 4:
            self.timer_label = tk.Label(self.root, text="", bg=DARK_GREY, fg=WHITE, font=("Helvetica", 16))
            self.timer_label.place(relx=0.59, rely=0.86, anchor=tk.CENTER)
            self.remaining_time = GUESS_TIMEOUT
        elif code_length == 6:
            self.timer_label = tk.Label(self.root, text="", bg=DARK_GREY, fg=WHITE, font=("Helvetica", 16))
            self.timer_label.place(relx=0.62, rely=0.864, anchor=tk.CENTER)  
            self.remaining_time = 9  
        else:
            raise ValueError("Invalid code length")

        self.timer_running = False
        self.start_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if not self.game_over and self.time_limit and self.remaining_time > 0:
            self.timer_label.config(text=f"Time left: {self.remaining_time}")
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.root.after(1000, self.update_timer)
        elif not self.game_over and self.time_limit:  
            self.end_game("You lose.")  
            
            for widget in self.palette_frame.winfo_children():
                widget.configure(state="disabled")

    def reset_timer(self):
        if len(self.secret_code) == 6:
            self.remaining_time = 9  
        else:
            self.remaining_time = GUESS_TIMEOUT  

    def create_board(self, code_length):
        self.board_frame = tk.Frame(self.root, bg=BLACK)
        self.board_frame.pack(side=tk.LEFT, padx=(555, 10), expand=False)

        self.rows = []
        for _ in range(MAX_ATTEMPTS):
            row = tk.Frame(self.board_frame, bg=DARK_GREY)
            row.pack(side=tk.TOP)
            self.rows.insert(0, row)

            for _ in range(code_length):
                board_widget = tk.Canvas(row, width=COLUMN_SIZE, height=ROW_SIZE, bg=BLACK, highlightbackground=WHITE)
                board_widget.pack(side=tk.LEFT)

    def create_feedback_grid(self, code_length):
        self.feedback_frame = tk.Frame(self.root, bg=DARK_GREY)
        self.feedback_frame.pack(side=tk.LEFT, padx=(10, 200), expand=False)

        for _ in range(3):  
            empty_row = tk.Frame(self.feedback_frame, bg=WHITE)
            empty_row.pack(side=tk.TOP)

        self.feedback_rows = []
        for _ in range(MAX_ATTEMPTS):
            row = tk.Frame(self.feedback_frame, bg=WHITE)
            row.pack(side=tk.TOP)
            self.feedback_rows.insert(0, row)

            for _ in range(code_length):
                feedback_widget = tk.Canvas(row, width=COLUMN_SIZE, height=ROW_SIZE, bg=BLACK, highlightbackground=WHITE)
                feedback_widget.pack(side=tk.LEFT)

    def create_color_palette(self):
        self.palette_frame = tk.Frame(self.root, bg=LIGHT_GREY)
        self.palette_frame.place(x=1350 // 2, y=822)

        colors = self.colors_4 if len(self.secret_code) == 4 else self.colors_6
        for color in colors:
            color_button = tk.Button(self.palette_frame, width=3, height=1, bg=color, command=lambda c=color: self.on_color_click(c))
            color_button.pack(side=tk.LEFT, padx=0.3)

    def on_color_click(self, color):
        if self.attempts_left > 0 and not self.game_over:  
            row_index = self.current_row_index
            if len(self.chosen_colors) < len(self.secret_code):
                if color not in self.chosen_colors:
                    self.chosen_colors.append(color)
                    board_widgets = self.rows[row_index].winfo_children()
                    for widget in board_widgets:
                        if widget["bg"] == BLACK:
                            widget.configure(bg=color)
                            break

                    if len(self.chosen_colors) == len(self.secret_code):
                        self.evaluate_guess()
                else:
                    # Color already chosen, do nothing
                    pass
        else:
            # Game is over, disable color palette buttons
            for widget in self.palette_frame.winfo_children():
                widget.configure(state="disabled")

    def evaluate_guess(self):
        self.reset_timer()  
        guess = [widget["bg"] for widget in self.rows[self.current_row_index].winfo_children()]
        exact_matches = 0
        color_matches = 0
        secret_matched_indices = []
        guess_matched_indices = []

        for i in range(len(self.secret_code)):
            if guess[i] == self.secret_code[i]:
                exact_matches += 1
                secret_matched_indices.append(i)
                guess_matched_indices.append(i)

        # Count the occurrences of each color in the secret code and guess
        secret_color_count = {color: self.secret_code.count(color) for color in self.secret_code}
        guess_color_count = {color: guess.count(color) for color in self.secret_code}

        for color, count in guess_color_count.items():
            if color in secret_color_count:
                color_matches += min(count, secret_color_count[color])

        # Subtract exact matches from color matches
        color_matches -= exact_matches

        feedback_widgets = self.feedback_rows[self.current_row_index].winfo_children()
        feedback = []

        for i in range(len(self.secret_code)):
            if i in guess_matched_indices:
                feedback.append(RED)
            elif guess[i] in self.secret_code and guess[i] != self.secret_code[i]:
                feedback.append(WHITE)
            else:
                feedback.append(BLACK)

        for i, color in enumerate(feedback):
            canvas = feedback_widgets[i]
            self.draw_circle(canvas, ROW_SIZE / 2, ROW_SIZE / 2, DOT_RADIUS, fill=color)

        self.attempts_left -= 1
        self.points -= 1
        self.points_label.config(text=f"Points: {self.points}")

        if exact_matches == len(self.secret_code):
            self.game_over = True
            self.end_game("YOU WIN!")
        elif self.attempts_left == 0:
            self.game_over = True
            self.end_game("YOU LOSE.")

        self.current_row_index += 1
        self.chosen_colors = []

    def draw_circle(self, canvas, x, y, r, **kwargs):
        return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def end_game(self, message):
        if len(self.secret_code) == 4:
            end_message = tk.Label(self.root, text=message, bg=DARK_GREY, fg=WHITE, font=("Helvetica", 16))
            end_message.place(relx=0.59, rely=0.9, anchor=tk.CENTER, y=-40)
        else:
            end_message = tk.Label(self.root, text=message, bg=DARK_GREY, fg=WHITE, font=("Helvetica", 16))
            end_message.place(relx=0.617, rely=0.905, anchor=tk.CENTER, y=-40)
        self.timer_label.config(text="")

class MastermindMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind Menu")
        self.root.configure(bg=BLACK)

        # Set the window size and position
        window_width = 450
        window_height = 250
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Initialize variables for selected options
        self.selected_code_length = 4
        self.time_limit = False

        self.create_menu()

    def create_menu(self):
        title_label = tk.Label(self.root, text="MASTERMIND Web-App", fg="white", bg="black", font=("Helvetica", 24))
        title_label.pack(pady=20)

        code_length_label = tk.Label(self.root, text="Select code length:", fg="white", bg="black", font=("Helvetica", 14))
        code_length_label.pack()

        code_length_frame = tk.Frame(self.root, bg="black")
        code_length_frame.pack()

        four_colors_button = tk.Button(code_length_frame, text="4 colors", bg="grey", fg="black", command=self.set_code_length_4)
        four_colors_button.pack(side=tk.LEFT, padx=10)

        six_colors_button = tk.Button(code_length_frame, text="6 colors", bg="grey", fg="black", command=self.set_code_length_6)
        six_colors_button.pack(side=tk.LEFT)

        # Highlight the selected code length button
        if self.selected_code_length == 4:
            four_colors_button.config(bg="light grey")
        else:
            six_colors_button.config(bg="light grey")

        time_limit_label = tk.Label(self.root, text="Select time limit:", fg="white", bg="black", font=("Helvetica", 14))
        time_limit_label.pack()

        time_limit_frame = tk.Frame(self.root, bg="black")
        time_limit_frame.pack()

        time_limit_off_button = tk.Button(time_limit_frame, text="Off", bg="grey", fg="black", command=self.set_time_limit_off)
        time_limit_off_button.pack(side=tk.LEFT, padx=10)

        time_limit_on_button = tk.Button(time_limit_frame, text="On", bg="grey", fg="black", command=self.set_time_limit_on)
        time_limit_on_button.pack(side=tk.LEFT)

        # Highlight the selected time limit button
        if self.time_limit:
            time_limit_on_button.config(bg="light grey")
        else:
            time_limit_off_button.config(bg="light grey")

        start_game_button = tk.Button(self.root, text="Start Game", bg="grey", fg="black", command=self.start_game)
        start_game_button.pack(pady=20)

    def set_code_length_4(self):
        self.selected_code_length = 4
        # Update button colors to reflect the selection
        self.update_menu()

    def set_code_length_6(self):
        self.selected_code_length = 6
        # Update button colors to reflect the selection
        self.update_menu()

    def set_time_limit_off(self):
        self.time_limit = False
        # Update button colors to reflect the selection
        self.update_menu()

    def set_time_limit_on(self):
        self.time_limit = True
        # Update button colors to reflect the selection
        self.update_menu()

    def update_menu(self):
        # Refresh the menu to update button colors
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_menu()

    def start_game(self):
        self.root.destroy()
        root = tk.Tk()
        game = MastermindGame(root, code_length=self.selected_code_length, time_limit=self.time_limit)
        if self.selected_code_length == 6:
            game.board_frame.configure(width=game.board_frame.winfo_width() // 4)
            game.feedback_frame.configure(width=game.feedback_frame.winfo_width() // 4)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    menu = MastermindMenu(root)
    root.mainloop()
