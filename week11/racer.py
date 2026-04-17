import pygame
import random
import sys
import time

# Racer game demo — puts everything together:
#   sprites, groups, move_ip, spritecollideany, USEREVENT speed increase, score

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
FPS = 60

font_big   = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# Load assets once before the game loop
image_background = pygame.image.load("resources/AnimatedStreet.png")
image_player     = pygame.image.load("resources/Player.png")
image_enemy      = pygame.image.load("resources/Enemy.png")

pygame.mixer.music.load("resources/background.wav")
pygame.mixer.music.play(-1)   # loop forever

sound_crash = pygame.mixer.Sound("resources/crash.wav")

SPEED = 5       # global enemy speed (increases over time)
SCORE = 0

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)   # speed up every second


# ── Sprites ──────────────────────────────────────────────────────────────────

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        # clamp to screen
        if self.rect.left < 0:      self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self._reset()

    def _reset(self):
        global SCORE
        SCORE += 1
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0   # just above the screen

    def update(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self._reset()


# ── Setup ─────────────────────────────────────────────────────────────────────

player = Player()
enemy1 = Enemy()
enemy2 = Enemy()
enemy2.rect.bottom = -HEIGHT // 2   # stagger so they don't start at same y

all_sprites   = pygame.sprite.Group(player, enemy1, enemy2)
enemy_sprites = pygame.sprite.Group(enemy1, enemy2)

# ── Game loop ─────────────────────────────────────────────────────────────────

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == INC_SPEED:
            SPEED += 0.5

    all_sprites.update()

    # Draw background, then sprites, then HUD
    screen.blit(image_background, (0, 0))
    all_sprites.draw(screen)

    score_surf = font_small.render(
        f"Score: {int(SCORE)}   Speed: {SPEED:.1f}", True, "black"
    )
    screen.blit(score_surf, (10, 10))

    # Collision check
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        screen.fill("red")
        go_surf = font_big.render("Game Over", True, "black")
        go_rect = go_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        sc_surf = font_small.render(f"Final score: {int(SCORE)}", True, "black")
        sc_rect = sc_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(go_surf, go_rect)
        screen.blit(sc_surf, sc_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(FPS)
