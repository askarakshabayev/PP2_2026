import pygame
import random

# USEREVENT — custom timed events.
# pygame.time.set_timer(event_type, interval_ms) fires that event every interval.
# sprite.kill() removes the sprite from ALL groups it belongs to.

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("05 - USEREVENT + kill()")
clock = pygame.time.Clock()

SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, 1500)   # fire every 1.5 seconds

COLORS = ["red", "blue", "orange", "purple", "cyan"]


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(random.choice(COLORS))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(15, WIDTH - 15)
        self.rect.bottom = 0
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()     # removes from ALL groups; Python garbage-collects it


cars = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_CAR:
            cars.add(Car())

    cars.update()

    screen.fill((50, 50, 50))
    cars.draw(screen)

    count = pygame.font.SysFont("Verdana", 20).render(
        f"Cars: {len(cars)}", True, "white"
    )
    screen.blit(count, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
