import pygame
import random 

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Example sprite")

clock = pygame.time.Clock()
is_over = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((56, 67, 134))
        self.rect = self.image.get_rect()
        self.rect.center = (W // 2, H - 40)
        self.speed = 6
    
    def update(self):
        keys = pygame.key.get_pressed()
        # print(keys[pygame.K_LEFT])
        # print(keys[pygame.K_RIGHT])
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((34, 87, 98))
        self.rect = self.image.get_rect()
        self.speed = 5
        self._reset()

    def _reset(self):
        self.rect.left = random.randint(0, W - self.rect.width)
        self.rect.bottom = 0
    
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > H:
            self._reset()

player = Player()
enemy = Enemy()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

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