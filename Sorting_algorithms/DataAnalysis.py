import pygame
import random

# Visualization Behavior
# Initial Setup: The array of bars is drawn on the screen, each bar representing an element in the unsorted list.
# Merge Sort Process:
# The process starts by dividing the unsorted list into n sublists, each containing one element (a single element is considered as sorted).
# Then, it repeatedly merges sublists to produce new sorted sublists until there is only one sublist remaining.
# During each merge, elements from the sublists are compared and merged into a single sorted sublist.
# The sorting process continues until there is only one sorted sublist remaining, which represents the sorted list.
# Sorted State:
# Once the sorting process is complete, all bars are colored green to indicate that the list is fully sorted.

# Constants
WIDTH, HEIGHT = 800, 600
BAR_WIDTH = 10
NUM_BARS = WIDTH // BAR_WIDTH
COLORS = {
    'background': (0, 0, 0),
    'bar': (100, 100, 255),
    'sorted': (0, 255, 0),
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Data Analysis and Visualization with Sorting")

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

def merge_sort_visual(data, start, end):
    if end - start > 1:
        mid = (start + end) // 2
        merge_sort_visual(data, start, mid)
        merge_sort_visual(data, mid, end)
        merge(data, start, mid, end)

def merge(data, start, mid, end):
    left = data[start:mid]
    right = data[mid:end]
    k = start
    i = j = 0
    while start + i < mid and mid + j < end:
        if left[i] < right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        k += 1
        draw_bars(data, {k: COLORS['sorted']})
        pygame.time.delay(50)
    while start + i < mid:
        data[k] = left[i]
        i += 1
        k += 1
        draw_bars(data, {k: COLORS['sorted']})
        pygame.time.delay(50)
    while mid + j < end:
        data[k] = right[j]
        j += 1
        k += 1
        draw_bars(data, {k: COLORS['sorted']})
        pygame.time.delay(50)

def main():
    running = True
    sorted_data = data[:]  # Copy of data to be sorted
    merge_sort_visual(sorted_data, 0, len(sorted_data))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_bars(sorted_data, {i: COLORS['sorted'] for i in range(len(sorted_data))})
        pygame.time.delay(500)

    pygame.quit()

if __name__ == "__main__":
    main()
