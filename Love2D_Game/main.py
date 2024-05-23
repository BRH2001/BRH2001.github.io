import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Orb Dodger")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
class Player:
    def __init__(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.radius = 20
        self.speed = 300
        self.direction = pygame.Vector2(0, 1)
        self.invincibility = 2
        self.invincible = True

    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed * dt

        # Boundary checks
        if self.x < self.radius:
            self.x = self.radius
        elif self.x > screen_width - self.radius:
            self.x = screen_width - self.radius
        if self.y < self.radius:
            self.y = self.radius
        elif self.y > screen_height - self.radius:
            self.y = screen_height - self.radius

    def draw(self):
        color = BLACK if self.invincible else BLUE
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        if self.invincible:
            pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius + 1, 1)


class Coin:
    def __init__(self):
        self.x = random.randint(50, screen_width - 50)
        self.y = random.randint(50, screen_height - 50)
        self.radius = 10

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)


class Enemy:
    def __init__(self, direction):
        self.x = random.randint(50, screen_width - 50)
        self.y = random.randint(50, screen_height - 50)
        self.radius = 15
        self.speed = 150
        self.direction = direction
        self.color = RED

    def move(self, dt):
        self.x += self.speed * self.direction.x * dt
        self.y += self.speed * self.direction.y * dt

        if self.x < self.radius or self.x > screen_width - self.radius:
            self.direction.x = -self.direction.x
        if self.y < self.radius or self.y > screen_height - self.radius:
            self.direction.y = -self.direction.y

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
def check_collision(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance < r1 + r2

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    player = Player()
    coins = [Coin() for _ in range(20)]
    enemies = [Enemy(pygame.Vector2(1, 0) if random.random() < 0.5 else pygame.Vector2(-1, 0)) for _ in range(10)]
    enemies += [Enemy(pygame.Vector2(0, 1) if random.random() < 0.5 else pygame.Vector2(0, -1)) for _ in range(10)]
    enemies += [Enemy(pygame.Vector2(1 if random.random() < 0.5 else -1, 1 if random.random() < 0.5 else -1)) for _ in range(6)]

    game_state = "menu"
    coins_collected = 0
    high_score = 0
    pause = False

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state == "play":
            if player.invincibility > 0:
                player.invincibility -= dt
                if player.invincibility <= 0:
                    player.invincible = False
                    player.invincibility = 2

            if not pause:
                player.move(dt)
                for enemy in enemies:
                    enemy.move(dt)

                for enemy in enemies:
                    if not player.invincible and check_collision(player.x, player.y, player.radius, enemy.x, enemy.y, enemy.radius):
                        game_state = "game_over"
                        high_score = max(high_score, coins_collected)

                coins = [coin for coin in coins if not check_collision(player.x, player.y, player.radius, coin.x, coin.y, coin.radius)]
                coins_collected = 20 - len(coins)

                if len(coins) == 0:
                    game_state = "you_win"
                    high_score = max(high_score, coins_collected)

        # Drawing
        screen.fill(BLACK)

        if game_state == "play":
            player.draw()
            for coin in coins:
                coin.draw()
            for enemy in enemies:
                enemy.draw()

            draw_text(f"Coins: {coins_collected}", font, WHITE, 10, 10)
            draw_text(f"High Score: {high_score}", font, WHITE, 10, 40)

        else:
            if game_state == "menu":
                draw_text("Press SPACE to Start", font, WHITE, screen_width // 2 - 100, screen_height // 2)
            elif game_state == "game_over":
                draw_text("Game Over", font, WHITE, screen_width // 2 - 100, screen_height // 2 - 20)
                draw_text(f"High Score: {high_score}", font, WHITE, screen_width // 2 - 100, screen_height // 2)
                draw_text("Press SPACE to Try Again", font, WHITE, screen_width // 2 - 100, screen_height // 2 + 20)
            elif game_state == "you_win":
                draw_text("You Win!", font, WHITE, screen_width // 2 - 100, screen_height // 2 - 20)
                draw_text(f"High Score: {high_score}", font, WHITE, screen_width // 2 - 100, screen_height // 2)
                draw_text("Press SPACE to Play Again", font, WHITE, screen_width // 2 - 100, screen_height // 2 + 20)

        if pause:
            draw_text("Paused", font, WHITE, screen_width // 2 - 50, screen_height // 2)

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if game_state in ["menu", "game_over", "you_win"]:
                game_state = "play"
                player = Player()
                coins = [Coin() for _ in range(20)]
                enemies = [Enemy(pygame.Vector2(1, 0) if random.random() < 0.5 else pygame.Vector2(-1, 0)) for _ in range(10)]
                enemies += [Enemy(pygame.Vector2(0, 1) if random.random() < 0.5 else pygame.Vector2(0, -1)) for _ in range(10)]
                enemies += [Enemy(pygame.Vector2(1 if random.random() < 0.5 else -1, 1 if random.random() < 0.5 else -1)) for _ in range(6)]
                coins_collected = 0
                pause = False
            elif game_state == "play" and keys[pygame.K_p]:
                pause = not pause

    pygame.quit()

if __name__ == "__main__":
    main()
