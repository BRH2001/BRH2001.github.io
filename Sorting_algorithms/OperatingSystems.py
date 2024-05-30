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

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radix Sort Visualization")

# Generate random data
data = [random.randint(1, HEIGHT) for _ in range(NUM_BARS)]

def draw_bars(data, sorted_indices=set()):
    screen.fill(COLORS['background'])
    for i, value in enumerate(data):
        color = COLORS['bar']
        if i in sorted_indices:
            color = COLORS['sorted']
        pygame.draw.rect(screen, color, (i * BAR_WIDTH, HEIGHT - value, BAR_WIDTH, value))
    pygame.display.flip()

def counting_sort(data, exp):
    output = [0] * len(data)
    count = [0] * 10

    for i in range(len(data)):
        index = data[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = len(data) - 1
    while i >= 0:
        index = data[i] // exp
        output[count[index % 10] - 1] = data[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(len(data)):
        data[i] = output[i]

def radix_sort(data):
    max_value = max(data)
    exp = 1
    while max_value // exp > 0:
        counting_sort(data, exp)
        draw_bars(data)
        pygame.time.delay(100)
        exp *= 10

def main():
    running = True
    sorted_data = data[:]  # Copy of data to be sorted
    radix_sort(sorted_data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
