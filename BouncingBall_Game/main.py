import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 66

# Colors
LIGHT_GREEN = (144, 238, 144)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_LILAC = (221, 160, 221)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 

# Brick dimensions
BRICK_ROWS = 6
BRICK_COLS = 11
BRICK_WIDTH = SCREEN_WIDTH // BRICK_COLS
BRICK_HEIGHT = 30

# Paddle dimensions
PADDLE_WIDTH = SCREEN_WIDTH // 7
PADDLE_HEIGHT = 20
PADDLE_SPEED = 12

# Ball dimensions
BALL_RADIUS = 9
BALL_INITIAL_SPEED = 6

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Brick Breaker")

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(LIGHT_GREEN)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
        self.speed = PADDLE_SPEED

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS*2, BALL_RADIUS*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = BALL_INITIAL_SPEED
        self.direction = pygame.Vector2(0, -1).rotate(45)

    def update(self, paddle, bricks):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Collision with walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction.x = -self.direction.x
        if self.rect.top <= 0:
            self.direction.y = -self.direction.y
        if self.rect.bottom >= SCREEN_HEIGHT:
            return 'miss'

        # Collision with paddle
        if self.rect.colliderect(paddle.rect):
            self.direction.y = -self.direction.y
            self.rect.bottom = paddle.rect.top
            self.speed += 0.5  # Increase ball speed after hitting the paddle

        # Collision with bricks
        hit_brick = pygame.sprite.spritecollideany(self, bricks)
        if hit_brick:
            self.direction.y = -self.direction.y
            hit_brick.kill()
            return 'hit'

        return None

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Main menu
def main_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Start", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    text = font.render("Arrow Keys to Move, P to Pause", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
    screen.blit(text, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# Pause menu
def pause_menu():
    paused = True
    font = pygame.font.Font(None, 36)
    text = font.render("Paused - Press P to Resume", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

# Game over screen
def game_over(points):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over! Points: {points}/66", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    text = font.render("Press SPACE to Restart", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
    screen.blit(text, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# Main game function
def main():
    clock = pygame.time.Clock()
    paddle = Paddle()
    ball = Ball()

    bricks = pygame.sprite.Group()
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            color = LIGHT_BLUE if (row + col) % 2 == 0 else LIGHT_LILAC
            brick = Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, color)
            bricks.add(brick)

    all_sprites = pygame.sprite.Group(paddle, ball)
    points = 0
    lives = 3

    running = True
    started = False

    main_menu()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_menu()
                if event.key == pygame.K_SPACE:
                    started = True

        keys = pygame.key.get_pressed()
        paddle.update(keys)

        if started:
            result = ball.update(paddle, bricks)
            if result == 'hit':
                points += 1
            elif result == 'miss':
                lives -= 1
                ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball.direction = pygame.Vector2(0, -1).rotate(45)
                ball.speed = BALL_INITIAL_SPEED
                started = False
                if lives <= 0:
                    game_over(points)
                    main()
                    return

        screen.fill(BLACK)
        all_sprites.draw(screen)
        bricks.draw(screen)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Points: {points}/66", True, WHITE)
        screen.blit(text, (10, 10))

        text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - 120, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
