import pygame
import random

pygame.init()

screen_size = width, height = (600, 600)

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

font = pygame.font.SysFont("comicsansms", 72)
image = pygame.image.load("ball.png")
done = False
FPS = 100
drawing = False
prev_pos = None
color = COLOR_BLUE
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            prev_pos = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if drawing:
        pos = pygame.mouse.get_pos()
        if prev_pos is None:
            prev_pos = pos
        print(pos, prev_pos)
        pygame.draw.line(screen, color, prev_pos, pos, 5)
        prev_pos = pos
        # pygame.draw.circle(screen, COLOR_BLUE, pos, 5)
    text = font.render("Hello KBTU", True, (0, 0, 255))
    screen.blit(text, (100, 100))
    screen.blit(image, (200, 200))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
