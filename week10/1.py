import pygame

pygame.init()

screen_size = width, height = (600, 600)

screen = pygame.display.set_mode(screen_size)

done = False

while not done:
    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            done = True

pygame.quit()


