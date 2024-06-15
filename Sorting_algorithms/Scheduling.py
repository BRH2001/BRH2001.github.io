import pygame
import random

# Visualization Behavior
# Initial Setup: The array of bars is drawn on the screen, each bar representing a task's priority or deadline in the unsorted list.
# Heap Sort Process:
# The process starts by building a max heap from the unsorted list of tasks.
# The largest element (root of the heap) is swapped with the last element of the heap.
# The heap size is reduced, and the heapify process is called to restore the heap property.
# This process is repeated until all elements are sorted.
# Sorted State:
# Once the sorting process is complete, all bars are colored green to indicate that the tasks are fully sorted by priority or deadline.

# Constants
WIDTH, HEIGHT = 800, 600
BAR_WIDTH = 10
NUM_BARS = WIDTH // BAR_WIDTH
COLORS = {
    'background': (0, 0, 0),
    'bar': (100, 100, 255),
    'heap': (255, 0, 0),
    'sorted': (0, 255, 0),
    'comparing': (255, 255, 0),
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Task Scheduling Visualization")

# Generate random task priorities/deadlines
data = [random.randint(1, HEIGHT) for _ in range(NUM_BARS)]

def draw_bars(data, color_positions={}):
    screen.fill(COLORS['background'])
    for i, value in enumerate(data):
        color = COLORS['bar']
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(screen, color, (i * BAR_WIDTH, HEIGHT - value, BAR_WIDTH, value))
    pygame.display.flip()

def heapify(data, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and data[i] < data[left]:
        largest = left

    if right < n and data[largest] < data[right]:
        largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        draw_bars(data, {i: COLORS['comparing'], largest: COLORS['comparing']})
        pygame.time.delay(100)
        heapify(data, n, largest)

def heap_sort(data):
    n = len(data)

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        draw_bars(data, {i: COLORS['sorted'], 0: COLORS['heap']})
        pygame.time.delay(100)
        heapify(data, i, 0)

def main():
    running = True
    sorted_data = data[:]  # Copy of data to be sorted
    heap_sort(sorted_data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_bars(sorted_data, {i: COLORS['sorted'] for i in range(len(sorted_data))})
        pygame.time.delay(500)

    pygame.quit()

if __name__ == "__main__":
    main()
