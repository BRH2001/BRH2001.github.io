import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
BAR_WIDTH = 10
NUM_BARS = WIDTH // BAR_WIDTH
COLORS = {
    'background': (0, 0, 0),
    'bar': (100, 100, 255),
    'sorted': (0, 255, 0),
}

# Visualization Behavior
# Initial Setup: The array of bars is drawn on the screen, each bar representing a record in the unsorted database table.
# Quick sort Process:
# The process starts by selecting a pivot record from the unsorted database.
# Records are then partitioned into two groups: those less than the pivot and those greater than or equal to the pivot.
# This partitioning step ensures that the pivot record is in its final sorted position.
# The process is then recursively applied to the two partitions until all records are sorted.
# Sorted State:
# Once the sorting process is complete, all bars are colored green to indicate that the database records are fully sorted.

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Database Sorting Visualization")

# Generate random data
data = [random.randint(1, HEIGHT) for _ in range(NUM_BARS)]

def draw_bars(data, color_positions={}):
    screen.fill(COLORS['background'])
    for i, value in enumerate(data):
        color = COLORS['bar']
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(screen, color, (i * BAR_WIDTH, HEIGHT - value, BAR_WIDTH, value))
    pygame.display.flip()

def database_sort_visual(data):
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                draw_bars(data, {i: COLORS['sorted'], j: COLORS['sorted']})
                pygame.time.delay(50)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        draw_bars(data, {i + 1: COLORS['sorted'], high: COLORS['sorted']})
        pygame.time.delay(50)
        return i + 1

    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    quick_sort(data, 0, len(data) - 1)

def main():
    running = True
    sorted_data = data[:]  # Copy of data to be sorted
    database_sort_visual(sorted_data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_bars(sorted_data, {i: COLORS['sorted'] for i in range(len(sorted_data))})
        pygame.time.delay(500)

    pygame.quit()

if __name__ == "__main__":
    main()
