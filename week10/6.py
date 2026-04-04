import pygame

pygame.init()

screen_size = width, height = (600, 600)

screen = pygame.display.set_mode(screen_size)

COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

done = False
is_red = True
circle_x = 100
circle_y = 100
radius = 40

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_red = not is_red
    
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_UP]:
        circle_y -= 1
    if pressed_keys[pygame.K_DOWN]:
        circle_y += 1
    if pressed_keys[pygame.K_LEFT]:
        circle_x -= 1
    if pressed_keys[pygame.K_RIGHT]:
        circle_x += 1

    if is_red:
        screen.fill(COLOR_RED)
        pygame.draw.circle(screen, COLOR_BLUE, (circle_x, circle_y), radius, 4)
    else:
        screen.fill(COLOR_BLUE)
        pygame.draw.circle(screen, COLOR_RED, (circle_x, circle_y), radius, 4)
    pygame.display.flip()

pygame.quit()


