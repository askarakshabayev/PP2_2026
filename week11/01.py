import pygame

# A Sprite = game object with two required attributes:
#   .image  — the Surface that gets drawn
#   .rect   — the position / bounding box on screen

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - Basic Sprite")
clock = pygame.time.Clock()


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()                                      # required
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]: self.rect.move_ip(5, 0)
        if keys[pygame.K_UP]:    self.rect.move_ip(0, -5)
        if keys[pygame.K_DOWN]:  self.rect.move_ip(0, 5)


ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(ball)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()        # calls update() on every sprite in the group

    screen.fill("black")
    all_sprites.draw(screen)    # draws every sprite using .image at .rect position
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
