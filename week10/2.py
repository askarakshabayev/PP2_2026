import pygame

pygame.init()

screen_size = width, height = (600, 600)

screen = pygame.display.set_mode(screen_size)

COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

done = False
is_red = True

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_red = not is_red
    if is_red:
        screen.fill(COLOR_RED)
        pygame.draw.circle(screen, COLOR_BLUE, (100, 100), 100, 4)
    else:
        screen.fill(COLOR_BLUE)
        pygame.draw.circle(screen, COLOR_RED, (100, 100), 100, 4)
    pygame.display.flip()

pygame.quit()


