import pygame
import random 

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Example sprite")

clock = pygame.time.Clock()
is_over = False

class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(4, 12)
        self.image = pygame.Surface((size, size))
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, W)
        self.rect.y = random.randint(0, H)
        self.speed = random.randint(1, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > H:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, W)

stars = pygame.sprite.Group()
for _ in range(60):
    stars.add(Star())

while not is_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_over = True
    stars.update()
    screen.fill("black")
    stars.draw(screen)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()