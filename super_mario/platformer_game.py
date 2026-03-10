import pygame
import random
import sys
import os
import math

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Mario Color Palette
MARIO_SKY = (107, 140, 255)  
MARIO_RED = (231, 76, 60)
MARIO_BLUE = (41, 128, 185)
MARIO_SKIN = (255, 230, 200)
MARIO_BROWN = (139, 69, 19)
GRASS_GREEN = (40, 180, 99)
PIPE_GREEN = (39, 174, 96)
PIPE_DARK = (30, 132, 73)
GOLD = (241, 196, 15)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPRING_RED = (200, 0, 0)

# Physics
GRAVITY = 0.6
WALK_ACCEL = 0.8
FRICTION = 0.85
MAX_SPEED = 7
JUMP_FORCE = -14
SPRING_FORCE = -24 
LEVEL_WIDTH = 8000 # Reduced map size

# --- Classes ---

class Scenery:
    def __init__(self):
        self.elements = []
        for i in range(25): # Reduced for smaller map
            self.elements.append({'type': 'mtn', 'x': i * 800 + random.randint(0, 400), 'w': random.randint(300, 600), 'h': random.randint(200, 400)})
            self.elements.append({'type': 'tree', 'x': i * 400 + random.randint(0, 300), 'h': random.randint(70, 120)})
            self.elements.append({'type': 'cloud', 'x': i * 350 + random.randint(0, 200), 'y': random.randint(40, 180)})

    def draw(self, screen, camera_x):
        for e in self.elements:
            if e['type'] == 'mtn':
                mx = int((e['x'] - camera_x * 0.2) % (LEVEL_WIDTH + 1000)) - 500
                pygame.draw.polygon(screen, (93, 173, 226), [(mx, SCREEN_HEIGHT - 60), (mx + e['w']//2, SCREEN_HEIGHT - 60 - e['h']), (mx + e['w'], SCREEN_HEIGHT - 60)])
                pygame.draw.polygon(screen, (46, 134, 193), [(mx + e['w']//2, SCREEN_HEIGHT - 60 - e['h']), (mx + e['w'], SCREEN_HEIGHT - 60), (mx + e['w']//2, SCREEN_HEIGHT - 60)])
        for e in self.elements:
            if e['type'] == 'cloud':
                cx = int((e['x'] - camera_x * 0.3) % (LEVEL_WIDTH + 1000)) - 500
                pygame.draw.circle(screen, WHITE, (cx, e['y']), 35)
                pygame.draw.circle(screen, WHITE, (cx + 40, e['y']), 50)
                pygame.draw.circle(screen, WHITE, (cx + 80, e['y']), 35)
        for e in self.elements:
            if e['type'] == 'tree':
                tx = int((e['x'] - camera_x * 0.6) % (LEVEL_WIDTH + 1000)) - 500
                pygame.draw.rect(screen, (101, 67, 33), (tx + 18, SCREEN_HEIGHT - 60 - e['h'], 14, e['h']))
                pygame.draw.circle(screen, (34, 153, 84), (tx + 25, SCREEN_HEIGHT - 60 - e['h']), 40)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width, self.height = 40, 52
        self.frames_right = [self.create_mario_surface(False, f) for f in [0, 1, 2]]
        self.frames_left = [self.create_mario_surface(True, f) for f in [0, 1, 2]]
        self.image = self.frames_right[0]
        self.rect = self.image.get_rect()
        self.reset_pos()
        self.vel_x, self.vel_y = 0, 0
        self.on_ground = False
        self.lives = 3
        self.score = 0
        self.is_dead = False
        self.death_timer = 0
        self.direction = "right"
        self.walk_frame = 0
        self.walk_timer = 0

    def reset_pos(self):
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 250
        self.vel_x, self.vel_y = 0, 0

    def create_mario_surface(self, flip, frame):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, MARIO_RED, (10, 0, 25, 10)) 
        pygame.draw.rect(surf, MARIO_RED, (25 if flip else 5, 5, 12, 5)) 
        pygame.draw.rect(surf, MARIO_SKIN, (12, 10, 20, 15)) 
        eye_x = 15 if flip else 25
        pygame.draw.rect(surf, BLACK, (eye_x, 13, 3, 6)) 
        pygame.draw.rect(surf, MARIO_BLUE, (10, 25, 20, 20)) 
        pygame.draw.circle(surf, GOLD, (15, 30), 2) 
        pygame.draw.circle(surf, GOLD, (25, 30), 2) 
        lc = MARIO_BROWN
        if frame == 0:
            pygame.draw.rect(surf, lc, (8, 45, 10, 7))
            pygame.draw.rect(surf, lc, (22, 45, 10, 7))
        elif frame == 1:
            pygame.draw.rect(surf, lc, (12, 42, 10, 7))
            pygame.draw.rect(surf, lc, (25, 45, 10, 7))
        else:
            pygame.draw.rect(surf, lc, (5, 45, 10, 7))
            pygame.draw.rect(surf, lc, (18, 42, 10, 7))
        return surf

    def update(self, solids, game):
        if self.is_dead:
            self.death_timer -= 1
            self.rect.y += 8
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x -= WALK_ACCEL
            self.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x += WALK_ACCEL
            self.direction = "right"
        else:
            self.vel_x *= FRICTION
            if abs(self.vel_x) < 0.2: self.vel_x = 0
        
        self.vel_x = max(-MAX_SPEED, min(MAX_SPEED, self.vel_x))
        self.vel_y += GRAVITY

        # Vertical
        self.rect.y += self.vel_y
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, solids, False)
        for b in hits:
            if self.vel_y > 0 and self.rect.bottom < b.rect.centery + 15:
                self.rect.bottom = b.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:
                self.rect.top = b.rect.bottom
                self.vel_y = 0
                if hasattr(b, "hit"): b.hit()

        # Horizontal
        self.rect.x += self.vel_x
        hits = pygame.sprite.spritecollide(self, solids, False)
        for b in hits:
            if self.vel_x > 0: self.rect.right = b.rect.left
            elif self.vel_x < 0: self.rect.left = b.rect.right
            self.vel_x = 0

        if self.on_ground and abs(self.vel_x) > 0.5:
            self.walk_timer += abs(self.vel_x)
            if self.walk_timer > 15:
                self.walk_frame = (self.walk_frame % 2) + 1
                self.walk_timer = 0
        else: self.walk_frame = 0
        self.image = (self.frames_left if self.direction == "left" else self.frames_right)[self.walk_frame]

        if self.rect.y > SCREEN_HEIGHT: self.trigger_death(game)

    def trigger_death(self, game):
        if not self.is_dead:
            self.is_dead, self.death_timer = True, 80
            self.lives -= 1
            game.play_sound('hit')

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y, limit_left, limit_right):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (150, 75, 0), (0, 0, 40, 30))
        pygame.draw.rect(self.image, (245, 222, 179), (10, 20, 20, 15))
        pygame.draw.circle(self.image, WHITE, (15, 10), 4); pygame.draw.circle(self.image, WHITE, (25, 10), 4)
        pygame.draw.circle(self.image, BLACK, (15, 10), 2); pygame.draw.circle(self.image, BLACK, (25, 10), 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dir = 1
        self.l, self.r = limit_left, limit_right
        self.vel_y = 0

    def update(self, solids):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        hits = pygame.sprite.spritecollide(self, solids, False)
        for b in hits:
            if self.vel_y > 0:
                self.rect.bottom = b.rect.top
                self.vel_y = 0
        self.rect.x += 2 * self.dir
        hits = pygame.sprite.spritecollide(self, solids, False)
        if hits:
            for b in hits:
                if self.dir > 0: self.rect.right = b.rect.left
                else: self.rect.left = b.rect.right
                self.dir *= -1
                break
        if self.rect.x < self.l or self.rect.right > self.r:
            self.dir *= -1

class Piranha(pygame.sprite.Sprite):
    def __init__(self, x, pipe_y):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, MARIO_RED, (5, 10, 30, 40))
        pygame.draw.circle(self.image, WHITE, (15, 20), 4)
        pygame.draw.circle(self.image, WHITE, (30, 35), 3)
        pygame.draw.rect(self.image, WHITE, (10, 30, 20, 6)) 
        self.rect = self.image.get_rect(midbottom=(x, pipe_y))
        self.base_y = pipe_y
        self.timer = 0
        self.state = "down" 

    def is_dangerous(self):
        return self.rect.bottom < self.base_y - 5

    def update(self, player_x):
        self.timer += 1
        dist = abs(player_x - self.rect.centerx)
        if self.state == "down":
            self.rect.y = self.base_y 
            if self.timer > 150 and dist > 120:
                self.state = "up"; self.timer = 0
        elif self.state == "up":
            if self.rect.bottom > self.base_y - 35: 
                self.rect.y -= 2
            else:
                if self.timer > 100: self.state = "returning"
        elif self.state == "returning":
            if self.rect.bottom < self.base_y:
                self.rect.y += 3
            else:
                self.state = "down"; self.timer = 0

class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLACK, (5, 35, 30, 5)) 
        for i in range(3):
            pygame.draw.arc(self.image, SPRING_RED, (10, 10 + i*8, 20, 15), 0, 3.14, 3)
        pygame.draw.rect(self.image, SPRING_RED, (5, 5, 30, 5)) 
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, player, game):
        if self.rect.colliderect(player.rect) and player.vel_y > 0 and player.rect.bottom < self.rect.centery + 10:
            player.vel_y = SPRING_FORCE
            player.on_ground = False
            game.play_sound('jump')

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, type="ground"):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.rect = pygame.Rect(x, y, w, h)
        if type == "ground":
            self.image.fill(MARIO_BROWN)
            pygame.draw.rect(self.image, GRASS_GREEN, (0, 0, w, 10))
            for _ in range(int(w*h/500)):
                pygame.draw.rect(self.image, (100, 50, 10), (random.randint(0, w), random.randint(15, h), 3, 3))
        elif type == "pipe":
            self.image.fill(PIPE_GREEN)
            pygame.draw.rect(self.image, WHITE, (5, 0, 5, h)) 
            pygame.draw.rect(self.image, PIPE_DARK, (w-15, 0, 10, h)) 
            pygame.draw.rect(self.image, BLACK, (0, 0, w, h), 2) 
            pygame.draw.rect(self.image, PIPE_GREEN, (0, 0, w, 25))
            pygame.draw.rect(self.image, BLACK, (0, 0, w, 25), 2)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, type="brick", game=None):
        super().__init__()
        self.game, self.type = game, type
        self.image = pygame.Surface((40, 40))
        self.rect = pygame.Rect(x, y, 40, 40)
        self.used = False
        self.draw_block()

    def draw_block(self):
        c = (200, 100, 50) if self.type == "brick" else GOLD
        if self.used: c = (100, 100, 100)
        self.image.fill(c)
        pygame.draw.rect(self.image, BLACK, (0, 0, 40, 40), 1)
        if self.type == "question" and not self.used:
            font = pygame.font.SysFont("Arial", 30, bold=True)
            txt = font.render("?", True, BLACK); self.image.blit(txt, (12, 5))

    def hit(self):
        if not self.used:
            self.used = True; self.draw_block()
            if self.type == "question":
                if random.random() < 0.7:
                    self.game.spawn_visual_coin(self.rect.x + 10, self.rect.y - 40)
                    self.game.player.score += 100
                else:
                    self.game.spawn_enemy_from_block(self.rect.x, self.rect.y - 40)

class VisualCoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GOLD, (10, 10), 10)
        pygame.draw.circle(self.image, WHITE, (10, 10), 6, 1)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.timer = 0
        self.alpha = 255

    def update(self):
        self.rect.y -= 4
        self.timer += 1
        if self.timer > 15:
            self.alpha = max(0, self.alpha - 15)
            self.image.set_alpha(self.alpha)
        if self.timer > 30: self.kill()

# --- Game ---

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512); pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Gemini Mario: World 1")
        self.clock = pygame.time.Clock(); self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.sounds = {}
        for s in ['jump', 'coin', 'hit', 'win', 'powerup']:
            if os.path.exists(f"{s}.wav"): self.sounds[s] = pygame.mixer.Sound(f"{s}.wav")
        self.reset()

    def reset(self):
        self.player = Player(); self.scenery = Scenery()
        self.solids = pygame.sprite.Group() 
        self.enemies = pygame.sprite.Group()
        self.pipe_enemies = pygame.sprite.Group()
        self.springs = pygame.sprite.Group()
        self.visuals = pygame.sprite.Group()
        self.camera_x = 0.0; self.game_over, self.won = False, False
        self.build_level()

    def build_level(self):
        curr_x = 0
        while curr_x < LEVEL_WIDTH:
            w = random.randint(800, 1500)
            g = Tile(curr_x, SCREEN_HEIGHT - 60, w, 60, "ground")
            self.solids.add(g)
            if random.random() > 0.7:
                self.springs.add(Spring(curr_x + 300, SCREEN_HEIGHT - 100))
            if random.random() > 0.4:
                px = curr_x + 500; ph = random.choice([80, 120])
                p = Tile(px, SCREEN_HEIGHT - 60 - ph, 80, ph, "pipe"); self.solids.add(p)
                self.pipe_enemies.add(Piranha(px + 40, SCREEN_HEIGHT - 60 - ph))
            bx = curr_x + 700
            for i in range(random.randint(2, 5)):
                blk = Block(bx + i*80, 350, "question" if i%2==0 else "brick", self); self.solids.add(blk)
            for _ in range(random.randint(1, 2)):
                ex = curr_x + random.randint(200, w-200)
                self.enemies.add(Goomba(ex, SCREEN_HEIGHT - 100, curr_x, curr_x + w))
            curr_x += w + random.randint(150, 300)
        self.goal_rect = pygame.Rect(LEVEL_WIDTH - 400, 0, 10, SCREEN_HEIGHT)

    def spawn_visual_coin(self, x, y): 
        self.visuals.add(VisualCoin(x, y))
        self.play_sound('coin')

    def spawn_enemy_from_block(self, x, y): 
        self.enemies.add(Goomba(x, y, x - 200, x + 200))
        self.play_sound('powerup')

    def play_sound(self, name):
        if name in self.sounds: self.sounds[name].play()

    def update(self):
        if self.game_over or self.won: return
        if self.player.is_dead:
            if self.player.death_timer <= 0:
                if self.player.lives > 0: self.player.reset_pos(); self.player.is_dead = False; self.camera_x = 0
                else: self.game_over = True
            else: self.player.update(self.solids, self)
            return
        self.player.update(self.solids, self)
        self.enemies.update(self.solids)
        self.visuals.update()
        for s in self.springs: s.update(self.player, self)
        for p in self.pipe_enemies: p.update(self.player.rect.centerx)
        self.camera_x += (self.player.rect.centerx - SCREEN_WIDTH//2 - self.camera_x) * 0.1
        self.camera_x = max(0.0, min(self.camera_x, LEVEL_WIDTH - SCREEN_WIDTH))
        for e in self.enemies:
            if self.player.rect.colliderect(e.rect):
                if self.player.vel_y > 0 and self.player.rect.bottom < e.rect.centery + 10:
                    # KILL ENEMY EFFECT
                    self.spawn_visual_coin(e.rect.x + 10, e.rect.y - 20)
                    e.kill(); self.player.vel_y = -10; self.player.score += 200
                else: self.player.trigger_death(self)
        for p in self.pipe_enemies:
            if self.player.rect.colliderect(p.rect) and p.is_dangerous(): self.player.trigger_death(self)
        if self.player.rect.colliderect(self.goal_rect): self.won = True; self.play_sound('win')

    def draw(self):
        self.screen.fill(MARIO_SKY); self.scenery.draw(self.screen, self.camera_x)
        cx = int(self.camera_x)
        for p in self.pipe_enemies: self.screen.blit(p.image, (p.rect.x - cx, p.rect.y))
        for s in self.solids: self.screen.blit(s.image, (s.rect.x - cx, s.rect.y))
        for s in self.springs: self.screen.blit(s.image, (s.rect.x - cx, s.rect.y))
        for e in self.enemies: self.screen.blit(e.image, (e.rect.x - cx, e.rect.y))
        for v in self.visuals: self.screen.blit(v.image, (v.rect.x - cx, v.rect.y))
        pygame.draw.rect(self.screen, BLACK, (LEVEL_WIDTH - 400 - cx, 100, 10, 440))
        pygame.draw.polygon(self.screen, MARIO_RED, [(LEVEL_WIDTH - 400 - cx + 10, 100), (LEVEL_WIDTH - 300 - cx, 140), (LEVEL_WIDTH - 400 - cx + 10, 180)])
        if not (self.player.is_dead and self.player.death_timer % 10 < 5):
            self.screen.blit(self.player.image, (self.player.rect.x - cx, self.player.rect.y))
        self.draw_ui(); pygame.display.flip()

    def draw_ui(self):
        s_txt = self.font.render(f"SCORE: {self.player.score:06}", True, WHITE)
        l_txt = self.font.render(f"LIVES: {self.player.lives}", True, WHITE)
        self.screen.blit(s_txt, (30, 30)); self.screen.blit(l_txt, (SCREEN_WIDTH - 180, 30))
        if self.game_over: self.screen.blit(self.font.render("GAME OVER - PRESS R", True, WHITE), (SCREEN_WIDTH//2-140, 300))
        if self.won: self.screen.blit(self.font.render("YOU WIN! - PRESS R", True, WHITE), (SCREEN_WIDTH//2-120, 300))

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: self.reset()
                    if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                        if not self.player.is_dead and self.player.on_ground:
                            self.player.vel_y = JUMP_FORCE; self.play_sound('jump')
            self.update(); self.draw()

if __name__ == "__main__":
    Game().run()
