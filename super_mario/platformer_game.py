import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 82, 45)
RED = (230, 0, 0)
DARK_RED = (150, 0, 0)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 150)
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)

# Physics
GRAVITY = 0.5
PLAYER_JUMP = -12
PLAYER_SPEED = 5
ENEMY_SPEED = 2

# Level
LEVEL_WIDTH = 3000

# --- Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(RED)
        # Add eyes for "graphics"
        pygame.draw.rect(self.image, WHITE, (5, 10, 10, 10))
        pygame.draw.rect(self.image, WHITE, (25, 10, 10, 10))
        pygame.draw.rect(self.image, BLACK, (10, 15, 5, 5))
        pygame.draw.rect(self.image, BLACK, (30, 15, 5, 5))
        
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 150
        
        self.change_x = 0
        self.change_y = 0
        self.lives = 3
        self.score = 0
        self.is_jumping = False

    def update(self, platforms):
        # Apply gravity
        self.change_y += GRAVITY
        
        # Move horizontal
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Move vertical
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y = 0
                self.is_jumping = False
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                self.change_y = 0

        # Boundary checks
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > SCREEN_HEIGHT:
            self.die()

    def jump(self):
        if not self.is_jumping:
            self.change_y = PLAYER_JUMP
            self.is_jumping = True

    def die(self):
        self.lives -= 1
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 200
        self.change_x = 0
        self.change_y = 0
        if self.lives < 0:
            self.lives = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        # Top outline for better visual
        pygame.draw.rect(self.image, LIGHT_BROWN, (0, 0, width, 5))
        # Dirt patterns
        for _ in range(int(width * height / 200)):
            px = random.randint(2, width-5)
            py = random.randint(7, height-5)
            pygame.draw.rect(self.image, LIGHT_BROWN, (px, py, 3, 3))
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, limit_left, limit_right):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(DARK_RED)
        # Angry eyes
        pygame.draw.line(self.image, WHITE, (5, 5), (15, 15), 2)
        pygame.draw.line(self.image, WHITE, (35, 5), (25, 15), 2)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.limit_left = limit_left
        self.limit_right = limit_right

    def update(self):
        self.rect.x += ENEMY_SPEED * self.direction
        if self.rect.x <= self.limit_left or self.rect.right >= self.limit_right:
            self.direction *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GOLD, (10, 10), 10)
        pygame.draw.circle(self.image, YELLOW, (7, 7), 3) # Shine
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bob_dir = 1
        self.bob_count = 0

    def update(self):
        self.bob_count += 1
        if self.bob_count % 10 == 0:
            self.rect.y += self.bob_dir
            if abs(self.bob_count) > 50:
                self.bob_dir *= -1
                self.bob_count = 0

class GoalFlag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 200), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLACK, (0, 0, 5, 200)) # Pole
        pygame.draw.polygon(self.image, GREEN, [(5, 0), (40, 25), (5, 50)]) # Flag
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 150

# --- Game Class ---

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Gemini Mario")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.large_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.reset()

    def reset(self):
        self.player = Player()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        
        self.camera_x = 0
        self.game_over = False
        self.won = False
        
        # Build Level
        # Ground
        ground = Platform(0, SCREEN_HEIGHT - 50, LEVEL_WIDTH, 50)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # Platforms
        plat_configs = [
            (300, 450, 200, 30),
            (600, 350, 150, 30),
            (900, 450, 250, 30),
            (1200, 300, 200, 30),
            (1500, 450, 200, 30),
            (1800, 350, 150, 30),
            (2100, 400, 300, 30),
            (2500, 300, 200, 30),
        ]
        for p in plat_configs:
            plat = Platform(*p)
            self.platforms.add(plat)
            self.all_sprites.add(plat)
            
            # Add enemies on some platforms
            if random.random() > 0.4:
                enemy = Enemy(p[0] + 10, p[1] - 40, p[0], p[0] + p[2])
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)
                
            # Add coins on platforms
            coin = Coin(p[0] + p[2]//2, p[1] - 40)
            self.coins.add(coin)
            self.all_sprites.add(coin)

        # Some ground enemies
        for i in range(5):
            ex = 500 + i * 500
            enemy = Enemy(ex, SCREEN_HEIGHT - 90, ex - 100, ex + 100)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # Goal Flag
        self.goal = GoalFlag(LEVEL_WIDTH - 100, SCREEN_HEIGHT - 50)
        self.goals.add(self.goal)
        self.all_sprites.add(self.goal)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                if not self.game_over and not self.won:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.change_x = -PLAYER_SPEED
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.change_x = PLAYER_SPEED
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.player.change_x < 0:
                        self.player.change_x = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.player.change_x > 0:
                        self.player.change_x = 0

    def update(self):
        if self.game_over or self.won:
            return

        self.player.update(self.platforms)
        self.enemies.update()
        self.coins.update()
        
        # Camera scrolling
        if self.player.rect.x > SCREEN_WIDTH // 2:
            self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        if self.camera_x > LEVEL_WIDTH - SCREEN_WIDTH:
            self.camera_x = LEVEL_WIDTH - SCREEN_WIDTH
            
        # Collision with coins
        coin_hit_list = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hit_list:
            self.player.score += 10
            
        # Collision with enemies
        enemy_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in enemy_hit_list:
            # Check if jumping on top
            if self.player.change_y > 0 and self.player.rect.bottom < enemy.rect.bottom:
                enemy.kill()
                self.player.score += 20
                self.player.change_y = PLAYER_JUMP / 2 # Bounce
            else:
                self.player.die()
                if self.player.lives == 0:
                    self.game_over = True

        # Collision with Goal
        if pygame.sprite.spritecollide(self.player, self.goals, False):
            self.won = True
            self.player.score += 100

    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw clouds for depth
        for i in range(5):
            pygame.draw.circle(self.screen, WHITE, (200 + i*600 - int(self.camera_x * 0.2) % 600, 100), 40)
            pygame.draw.circle(self.screen, WHITE, (240 + i*600 - int(self.camera_x * 0.2) % 600, 100), 50)
            pygame.draw.circle(self.screen, WHITE, (280 + i*600 - int(self.camera_x * 0.2) % 600, 100), 40)

        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))
        
        # Draw player
        self.screen.blit(self.player.image, (self.player.rect.x - self.camera_x, self.player.rect.y))
        
        # UI
        score_text = self.font.render(f"Score: {self.player.score}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))
        
        if self.game_over:
            msg = self.large_font.render("GAME OVER", True, DARK_RED)
            restart = self.font.render("Press R to Restart", True, BLACK)
            self.screen.blit(msg, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(restart, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50))
            
        if self.won:
            msg = self.large_font.render("YOU WIN!", True, DARK_GREEN)
            restart = self.font.render("Press R to Restart", True, BLACK)
            self.screen.blit(msg, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(restart, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
