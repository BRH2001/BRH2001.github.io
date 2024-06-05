import pygame
import random

# Visualization Behavior
# Initial Setup: The array of bars is drawn on the screen, each bar representing a database record's index in the unsorted list.
# Insertion Sort Process:
# The process starts by picking the second element of the array and compares it with the elements before it, inserting it into its correct position.
# This process is repeated for each element until the array is sorted.
# Sorted State:
# Once the sorting process is complete, all bars are colored green to indicate that the database records are fully sorted by index.

# Constants
WIDTH, HEIGHT = 800, 600
BAR_WIDTH = 10
NUM_BARS = WIDTH // BAR_WIDTH
COLORS = {
    'background': (0, 0, 0),
    'bar': (100, 100, 255),
    'sorted': (0, 255, 0),
    'comparing': (255, 255, 0),
    'inserting': (255, 0, 0),
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Database Record Sorting Visualization")

# Generate random database record indexes
data = [random.randint(1, HEIGHT) for _ in range(NUM_BARS)]

def draw_bars(data, color_positions={}):
    screen.fill(COLORS['background'])
    for i, value in enumerate(data):
        color = COLORS['bar']
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(screen, color, (i * BAR_WIDTH, HEIGHT - value, BAR_WIDTH, value))
    pygame.display.flip()

def insertion_sort_visual(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            draw_bars(data, {j: COLORS['comparing'], i: COLORS['inserting']})
            pygame.time.delay(50)
        data[j + 1] = key
        draw_bars(data, {j + 1: COLORS['inserting'], i: COLORS['comparing']})
        pygame.time.delay(50)

def main():
    running = True
    sorted_data = data[:]  # Copy of data to be sorted
    insertion_sort_visual(sorted_data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_bars(sorted_data, {i: COLORS['sorted'] for i in range(len(sorted_data))})
        pygame.time.delay(500)

    pygame.quit()

if __name__ == "__main__":
    main()
