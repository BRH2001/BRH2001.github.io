import tkinter as tk
import random

# Define colors
WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#FF0000"
DARK_GREY = "#333333"
LIGHT_GREY = "#CCCCCC"

# Define constants
ROW_SIZE = 50
COLUMN_SIZE = 50
DOT_RADIUS = 5
CODE_LENGTH = 4
MAX_ATTEMPTS = 12
INITIAL_POINTS = 13

class MastermindGame:
    def __init__(self, root):
        self.colors = ["red", "yellow", "green", "blue", "purple", "pink"]
        self.secret_code = random.sample(self.colors, k=CODE_LENGTH)
        self.points = INITIAL_POINTS
        self.attempts_left = MAX_ATTEMPTS

        self.root = root
        self.root.title("Mastermind")
        self.root.configure(bg=DARK_GREY)

        # Center the window on the screen
        window_width = 4 * COLUMN_SIZE + 200
        window_height = MAX_ATTEMPTS * ROW_SIZE + 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.create_board()
        self.create_feedback_grid()

        # Set current row index
        self.current_row_index = 0

        # Initialize chosen colors for each row
        self.chosen_colors = []

        # Display initial points
        self.points_label = tk.Label(self.root, text=f"Points: {self.points}", bg=LIGHT_GREY, fg=BLACK)
        self.points_label.place(x=270 // 0.6, y=root.winfo_screenheight() - 144)
        self.create_color_palette()

    def create_board(self):
        self.board_frame = tk.Frame(self.root, bg=WHITE)
        self.board_frame.pack(side=tk.LEFT, padx=(447, 10), expand=False)

        self.rows = []
        for _ in range(MAX_ATTEMPTS):
            row = tk.Frame(self.board_frame, bg=WHITE)
            row.pack(side=tk.TOP)
            self.rows.insert(0, row)

            for _ in range(CODE_LENGTH):
                board_widget = tk.Canvas(row, width=COLUMN_SIZE, height=ROW_SIZE, bg=LIGHT_GREY)
                board_widget.pack(side=tk.LEFT)

    def create_feedback_grid(self):
        self.feedback_frame = tk.Frame(self.root, bg=LIGHT_GREY)
        self.feedback_frame.pack(side=tk.RIGHT, padx=(10, 333), expand=False)

        for _ in range(3):  # Adjust the position slightly downwards
            empty_row = tk.Frame(self.feedback_frame, bg=LIGHT_GREY)
            empty_row.pack(side=tk.TOP)

        self.feedback_rows = []
        for _ in range(MAX_ATTEMPTS):
            row = tk.Frame(self.feedback_frame, bg=LIGHT_GREY)
            row.pack(side=tk.TOP)
            self.feedback_rows.insert(0, row)

            for _ in range(CODE_LENGTH):
                feedback_widget = tk.Canvas(row, width=COLUMN_SIZE, height=ROW_SIZE, bg=LIGHT_GREY)
                feedback_widget.pack(side=tk.LEFT)

    def create_color_palette(self):
        self.palette_frame = tk.Frame(self.root, bg=LIGHT_GREY)
        self.palette_frame.place(x=900 // 2, y=850)

        for color in self.colors:
            color_button = tk.Button(self.palette_frame, width=3, height=1, bg=color, command=lambda c=color: self.on_color_click(c))
            color_button.pack(side=tk.LEFT, padx=0)

    def on_color_click(self, color):
        if self.attempts_left > 0:
            row_index = self.current_row_index
            if len(self.chosen_colors) < CODE_LENGTH:
                if color not in self.chosen_colors:
                    self.chosen_colors.append(color)
                    board_widgets = self.rows[row_index].winfo_children()
                    for widget in board_widgets:
                        if widget["bg"] == LIGHT_GREY:
                            widget.configure(bg=color)
                            break

                    if len(self.chosen_colors) == CODE_LENGTH:
                        self.evaluate_guess()
                else:
                    # Color already chosen, do nothing
                    pass

    def evaluate_guess(self):
        guess = [widget["bg"] for widget in self.rows[self.current_row_index].winfo_children()]
        print("Guess:", guess)
        print("Secret code:", self.secret_code)
        exact_matches = 0
        color_matches = 0
        secret_matched_indices = []
        guess_matched_indices = []

        for i in range(CODE_LENGTH):
            if guess[i] == self.secret_code[i]:
                exact_matches += 1
                secret_matched_indices.append(i)
                guess_matched_indices.append(i)
        print("Exact Matches:", exact_matches)

        for i in range(CODE_LENGTH):
            if i not in secret_matched_indices:
                for j in range(CODE_LENGTH):
                    if j not in guess_matched_indices and guess[i] == self.secret_code[j]:
                        color_matches += 1
                        secret_matched_indices.append(j)
                        guess_matched_indices.append(i)
                        break
        print("Color Matches:", color_matches)

        feedback_widgets = self.feedback_rows[self.current_row_index].winfo_children()
        feedback = ["black"] * CODE_LENGTH
        for i in range(exact_matches):
            feedback[i] = RED
        for i in range(exact_matches, exact_matches + color_matches):
            feedback[i] = WHITE

        for i, color in enumerate(feedback):
            canvas = feedback_widgets[CODE_LENGTH - i - 1]
            self.draw_circle(canvas, ROW_SIZE / 2, ROW_SIZE / 2, DOT_RADIUS, fill=color)

        self.attempts_left -= 1
        self.points -= 1
        self.points_label.config(text=f"Points: {self.points}")

        if exact_matches == CODE_LENGTH:
            self.end_game("You win.")
        elif self.attempts_left == 0:
            self.end_game("You lose.")

        self.current_row_index += 1
        self.chosen_colors = []

    def draw_circle(self, canvas, x, y, r, **kwargs):
        return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

def end_game(self, message):
    # Adjust the x-coordinate to change the horizontal position
    end_message = tk.Label(self.root, text=message, bg=LIGHT_GREY, fg=BLACK, font=("Helvetica", 10))
    end_message.place(relx=30)

root = tk.Tk()
game = MastermindGame(root)
root.mainloop()
