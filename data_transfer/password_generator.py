import pygame
import random
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (192, 192, 192)

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
ROW_SIZE = 50
COLUMN_SIZE = 50
CIRCLE_RADIUS = 20
CODE_LENGTH = 4
MAX_ATTEMPTS = 12
MAX_POINTS = 13

class MastermindGame:
    def __init__(self):
        self.colors = [GREEN, PURPLE, BLUE, YELLOW, ORANGE, RED]
        self.secret_code = [random.choice(self.colors) for _ in range(CODE_LENGTH)]
        self.max_attempts = MAX_ATTEMPTS
        self.points = MAX_POINTS
        self.selected_colors = []
        self.current_row = 0
        self.attempts_left = self.max_attempts
        self.result_board = []

        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mastermind")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 18)
        self.big_font = pygame.font.SysFont(None, 36)

        self.create_board()

    def create_board(self):
        self.create_guess_board()

    def create_guess_board(self):
        self.guess_board = []
        for i in range(MAX_ATTEMPTS):
            row = [BLACK] * CODE_LENGTH
            self.guess_board.append(row)

    def draw_board(self):
        self.screen.fill(GRAY)

        # Draw guess rows
        for row_index, row in enumerate(self.guess_board):
            for col_index, color in enumerate(row):
                pygame.draw.circle(self.screen, color, ((col_index + 1) * COLUMN_SIZE + COLUMN_SIZE // 2, (row_index + 1) * ROW_SIZE + ROW_SIZE // 2), CIRCLE_RADIUS)

            # Draw response dots
            for i in range(4):
                if row_index < self.current_row:
                    response_color = self.result_board[row_index][i]
                    pygame.draw.circle(self.screen, response_color, (CODE_LENGTH * COLUMN_SIZE + COLUMN_SIZE * i + COLUMN_SIZE // 2 + 300, (row_index + 1) * ROW_SIZE + ROW_SIZE // 2), 5)

        # Draw color palette
        for i, color in enumerate(self.colors):
            pygame.draw.circle(self.screen, color, (SCREEN_WIDTH - 200 + (i % 2) * 100, SCREEN_HEIGHT - 200 + (i // 2) * 50), CIRCLE_RADIUS)

        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and self.attempts_left > 0:
            pos = pygame.mouse.get_pos()
            if pos[1] < SCREEN_HEIGHT - 200:
                # Check if the click is within the color palette
                if SCREEN_WIDTH - 200 <= pos[0] < SCREEN_WIDTH - 100 and SCREEN_HEIGHT - 200 <= pos[1] < SCREEN_HEIGHT - 100:
                    color_index = (pos[1] - (SCREEN_HEIGHT - 200)) // 50 * 2 + (pos[0] - (SCREEN_WIDTH - 200)) // 100
                    selected_color = self.colors[color_index]
                    if len(self.selected_colors) < CODE_LENGTH:
                        self.selected_colors.append(selected_color)
                        self.update_guess_board(selected_color)
                        pygame.display.update()  # Update display after selecting a color

    def update_guess_board(self, selected_color):
        row_index = self.current_row
        for col_index, color in enumerate(self.guess_board[row_index]):
            if color == BLACK:
                self.guess_board[row_index][col_index] = selected_color
                break
        if len(self.selected_colors) == CODE_LENGTH:
            self.check_guess()

    def check_guess(self):
        exact_matches = sum(1 for x, y in zip(self.guess_board[self.current_row], self.secret_code) if x == y)
        color_matches = sum(min(self.guess_board[self.current_row].count(color), self.secret_code.count(color)) for color in set(self.guess_board[self.current_row])) - exact_matches

        self.result_board.append([RED]*exact_matches + [WHITE]*color_matches + [BLACK]*(CODE_LENGTH - exact_matches - color_matches))
        self.attempts_left -= 1
        self.current_row += 1
        self.selected_colors = []

        if exact_matches == CODE_LENGTH:
            self.points = max(self.points - (MAX_ATTEMPTS - self.attempts_left), 1)
            self.show_message("Congratulations!", f"You cracked the code with {self.attempts_left} attempts left.")
        elif self.attempts_left == 0:
            self.show_message("Game Over", "You ran out of attempts. Better luck next time.")

    def show_message(self, title, message):
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    def play(self):
        while True:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw_board()
            self.clock.tick(60)

if __name__ == "__main__":
    game = MastermindGame()
    game.play()
