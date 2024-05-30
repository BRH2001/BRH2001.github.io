import pygame
import random


# Visualization Behavior 
# Initial Setup: The array of bars is drawn on the screen, each bar representing an element in the sorted list.
# Binary Search sort Process:
# The search starts by checking the middle element of the entire list (colored red).
# If the middle element is not the target, the search interval is updated to either the left or right half of the list, depending on whether the middle element is less than or greater than the target.
# The process repeats, with the new middle element being highlighted in red during each step.
# Target Found:
# When the middle element is equal to the target, it is colored green to indicate the target has been found.

# Constants
WIDTH, HEIGHT = 800, 600
BAR_WIDTH = 10
NUM_BARS = WIDTH // BAR_WIDTH
COLORS = {
    'background': (0, 0, 0),
    'bar': (100, 100, 255),
    'mid': (255, 0, 0),
    'found': (0, 255, 0),
    'searching': (255, 255, 255),
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Search Visualization")

# Generate sorted data
data = sorted(random.randint(1, HEIGHT) for _ in range(NUM_BARS))

def draw_bars(data, low, high, mid, target):
    screen.fill(COLORS['background'])
    for i, value in enumerate(data):
        color = COLORS['bar']
        if i == mid:
            color = COLORS['mid']  # Highlight the middle element
        elif data[i] == target and low <= i <= high:
            color = COLORS['found']  # Highlight the target when found
        elif low <= i <= high:
            color = COLORS['searching']  # Highlight the current search interval
        pygame.draw.rect(screen, color, (i * BAR_WIDTH, HEIGHT - value, BAR_WIDTH, value))
    pygame.display.flip()

def binary_search_visual(data, target):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        draw_bars(data, low, high, mid, target)
        pygame.time.delay(500)  # Delay to visualize the process
        if data[mid] == target:
            draw_bars(data, low, high, mid, target)
            pygame.time.delay(500)  # Additional delay to show the found state
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def main():
    running = True
    target = random.choice(data)  # Choose a random target from the data
    found_index = -1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if found_index == -1:
            found_index = binary_search_visual(data, target)

        draw_bars(data, 0, len(data) - 1, -1, target)
        pygame.time.delay(500)

    pygame.quit()

if __name__ == "__main__":
    main()
