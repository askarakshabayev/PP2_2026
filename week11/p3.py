import pygame

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Example sprite")

clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    def __init__(self, cent_x, cent_y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (cent_x, cent_y)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)

class Ball_1(pygame.sprite.Sprite):
    def __init__(self, cent_x, cent_y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (cent_x, cent_y)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(5, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, 5)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, -5)


ball1 = Ball(W // 2, H // 2)
ball2 = Ball(50, 50)
ball3 = Ball_1(300, 80)
ball4 = Ball_1(50, 500)
all_sprites = pygame.sprite.Group()
all_sprites.add(ball1)
all_sprites.add(ball2)
all_sprites.add(ball3)
all_sprites.add(ball4)


is_over = False
while not is_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_over = True
    
    all_sprites.update()
    screen.fill("black")
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()