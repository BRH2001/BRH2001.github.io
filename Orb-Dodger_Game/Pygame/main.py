import pygame
import random
import math

pygame.init()

screen_width, screen_height = 777, 555
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Orb Dodger")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 0, 255)
GREY = (44, 44, 44)


class Player:
    def __init__(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.radius = 20
        self.speed = 300
        self.direction = pygame.Vector2(0, 1)
        self.invincibility = 1
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

        if self.x < self.radius:
            self.x = self.radius
        elif self.x > screen_width - self.radius:
            self.x = screen_width - self.radius
        if self.y < self.radius:
            self.y = self.radius
        elif self.y > screen_height - self.radius:
            self.y = screen_height - self.radius

    def draw(self):
        color = GREY if self.invincible else BLUE
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
    def __init__(self, direction, color):
        self.x = random.randint(50, screen_width - 50)
        self.y = random.randint(50, screen_height - 50)
        self.radius = 15
        self.speed = 150
        self.direction = direction
        self.color = color

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


def generate_enemies(difficulty):
    enemies = []
    if difficulty == "easy":
        for _ in range(8):
            enemies.append(Enemy(pygame.Vector2(1, 0), RED))
            enemies.append(Enemy(pygame.Vector2(0, 1), RED))
    elif difficulty == "medium":
        for _ in range(8):
            enemies.append(Enemy(pygame.Vector2(1, 0), RED))
            enemies.append(Enemy(pygame.Vector2(0, 1), RED))
        for _ in range(4):
            enemies.append(Enemy(pygame.Vector2(1 if random.random() < 0.5 else -1, 1 if random.random() < 0.5 else -1), PINK))
    elif difficulty == "hard":
        for _ in range(10):
            enemies.append(Enemy(pygame.Vector2(1, 0), RED))
            enemies.append(Enemy(pygame.Vector2(0, 1), RED))
        for _ in range(6):
            enemies.append(Enemy(pygame.Vector2(1 if random.random() < 0.5 else -1, 1 if random.random() < 0.5 else -1), PINK))
    return enemies

def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    player = Player()
    coins = [Coin() for _ in range(20)]
    enemies = []
    game_state = "menu"
    coins_collected = 0
    high_score = 0
    pause = False
    difficulty = None

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if game_state in ["menu", "game_over", "you_win"]:
                if difficulty:
                    game_state = "play"
                    player = Player()
                    if difficulty == "easy":
                        coins = [Coin() for _ in range(20)]
                        coins_total = 20
                    elif difficulty == "medium":
                        coins = [Coin() for _ in range(40)]
                        coins_total = 40
                    elif difficulty == "hard":
                        coins = [Coin() for _ in range(80)]
                        coins_total = 80
                    enemies = generate_enemies(difficulty)
                    coins_collected = 0
                    pause = False
            elif game_state == "play" and keys[pygame.K_p]:
                pause = not pause
        elif keys[pygame.K_1]:
            difficulty = "easy"
        elif keys[pygame.K_2]:
            difficulty = "medium"
        elif keys[pygame.K_3]:
            difficulty = "hard"

        if game_state == "play":
            if player.invincibility > 0:
                player.invincibility -= dt
                if player.invincibility <= 0:
                    player.invincible = False
                    player.invincibility = 0

            if not pause:
                player.move(dt)
                for enemy in enemies:
                    enemy.move(dt)

                for coin in coins:
                    if check_collision(player.x, player.y, player.radius, coin.x, coin.y, coin.radius):
                        coins.remove(coin)
                        coins_collected += 1

                for enemy in enemies:
                    if not player.invincible and check_collision(player.x, player.y, player.radius, enemy.x, enemy.y, enemy.radius):
                        game_state = "game_over"
                    high_score = max(high_score, coins_collected)

                if len(coins) == 0:
                    game_state = "you_win"

        screen.fill(GREY)

        if game_state == "play":
            player.draw()
            for coin in coins:
                coin.draw()
            for enemy in enemies:
                enemy.draw()

            draw_text("Coins: " + str(coins_collected) + "/" + str(coins_total), font, WHITE, 10, 10)

            draw_text("High Score: " + str(high_score), font, WHITE, 10, 30)

        elif game_state == "menu":
            draw_text("Press SPACE to Start", font, WHITE, (screen_width - 200) // 2, (screen_height - 36) // 2)
            draw_text("Select Difficulty:", font, WHITE, (screen_width - 200) // 2, (screen_height - 36) // 2 + 25)
            draw_text("1: Easy  2: Medium  3: Hard", font, WHITE, (screen_width - 200) // 2, (screen_height - 36) // 2 + 50)
            if difficulty:
                draw_text(difficulty.capitalize(), font, WHITE, (screen_width - 180) // 2 + 160, (screen_height - 36) // 2 + 25)

        elif game_state in ["game_over", "you_win"]:
            draw_text("Press SPACE to Try Again", font, WHITE, (screen_width - 200) // 2, (screen_height - 36) // 2 + 90)
            draw_text("Select Difficulty:", font, WHITE, (screen_width - 220) // 2, (screen_height - 36) // 2 + 45)
            draw_text("1: Easy  2: Medium  3: Hard", font, WHITE, (screen_width - 220) // 2, (screen_height - 36) // 2 + 65)
            if difficulty:
                draw_text(difficulty.capitalize(), font, WHITE, (screen_width - 180) // 2 + 160, (screen_height - 36) // 2 + 45)
            if game_state == "game_over":
                draw_text("Game Over", font, WHITE, (screen_width - 200) // 2, (screen_height - 36) // 2 + 1)
                draw_text("High Score: " + str(high_score), font, WHITE, (screen_width - 200) // 2, (screen_height - 36) // 2 + 20)
            else:
                draw_text("You Win!", font, WHITE, (screen_width - 200) // 2, (screen_height - 36) // 2 + 1)
                draw_text("High Score: " + str(high_score), font, WHITE, (screen_width - 200) // 2, (screen_height - 36) // 2 + 21)

        if pause:
            draw_text("Paused", font, WHITE, (screen_width - 100) // 2, (screen_height - 36) // 2)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
