import pygame
import random 

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Example sprite")

clock = pygame.time.Clock()
is_over = False

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 15))
        self.image.fill((45, 65, 87))
        self.rect = self.image.get_rect()

    def reset_position(self):
        self.rect.x = random.randint(0, W - 20)
        self.rect.y = random.randrange(-300, -20)

    def update(self):
        self.rect.y += 3
        if self.rect.top > H:
            self.reset_position()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 15))
        self.image.fill("red")
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

block_group = pygame.sprite.Group()
for _ in range(50):
    block = Block()
    block.rect.x = random.randint(0, W)
    block.rect.y = random.randint(0, H)
    block_group.add(block)

player = Player()
all_sprites = pygame.sprite.Group(block_group, player)

score = 0
while not is_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_over = True
    hit_lists = pygame.sprite.spritecollide(player, block_group, True)
    for block in hit_lists:
        block.reset_position()
        score += 1
        print(score)
    all_sprites.update()
    screen.fill("black")
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()