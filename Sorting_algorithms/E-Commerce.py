import pygame
import random

# Visualization Behavior
# Initial Setup: The array of bars is drawn on the screen, each bar representing a product's price in the unsorted list.
# Quick Sort Process:
# The process starts by selecting a pivot element from the unsorted list.
# Elements are then partitioned into two groups: those less than the pivot and those greater than or equal to the pivot.
# This partitioning step ensures that the pivot element is in its final sorted position.
# The process is then recursively applied to the two partitions until all elements are sorted.
# Sorted State:
# Once the sorting process is complete, all bars are colored green to indicate that the products are fully sorted by price.

# Constants
WIDTH, HEIGHT = 800, 600
BAR_WIDTH = 10
NUM_BARS = WIDTH // BAR_WIDTH
COLORS = {
    'background': (0, 0, 0),
    'bar': (100, 100, 255),
    'pivot': (255, 0, 0),
    'sorted': (0, 255, 0),
    'comparing': (255, 255, 0),
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("E-commerce Product Sorting Visualization")

# Generate random product prices
data = [random.randint(1, HEIGHT) for _ in range(NUM_BARS)]

def draw_bars(data, color_positions={}):
    screen.fill(COLORS['background'])
    for i, value in enumerate(data):
        color = COLORS['bar']
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(screen, color, (i * BAR_WIDTH, HEIGHT - value, BAR_WIDTH, value))
    pygame.display.flip()

def quick_sort_visual(data, low, high):
    if low < high:
        pi = partition(data, low, high)
        quick_sort_visual(data, low, pi - 1)
        quick_sort_visual(data, pi + 1, high)

def partition(data, low, high):
    pivot = data[high]
    draw_bars(data, {high: COLORS['pivot']})
    pygame.time.delay(200)
    i = low - 1
    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            draw_bars(data, {i: COLORS['comparing'], j: COLORS['comparing']})
            pygame.time.delay(50)
    data[i + 1], data[high] = data[high], data[i + 1]
    draw_bars(data, {i + 1: COLORS['sorted'], high: COLORS['sorted']})
    pygame.time.delay(50)
    return i + 1

def main():
    running = True
    sorted_data = data[:]  # Copy of data to be sorted
    quick_sort_visual(sorted_data, 0, len(sorted_data) - 1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_bars(sorted_data, {i: COLORS['sorted'] for i in range(len(sorted_data))})
        pygame.time.delay(500)

    pygame.quit()

if __name__ == "__main__":
    main()
