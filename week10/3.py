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

is_key_pressed = False
is_up = False
is_down = False
is_left = False
is_right = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            is_key_pressed = True
            if event.key == pygame.K_SPACE:
                is_red = not is_red
            if event.key == pygame.K_UP:
                is_up = True
            if event.key == pygame.K_DOWN:
                is_down = True
            if event.key == pygame.K_LEFT:
                is_left = True
            if event.key == pygame.K_RIGHT:
                is_right = True
        if event.type == pygame.KEYUP:
            is_key_pressed = False
            is_up = is_down = is_left = is_right = False
    
    if is_key_pressed:
        if is_up:
            circle_y -= 1
        if is_down:
            circle_y += 1
        if is_left:
            circle_x -= 1
        if is_right:
            circle_x += 1

    if is_red:
        screen.fill(COLOR_RED)
        pygame.draw.circle(screen, COLOR_BLUE, (circle_x, circle_y), radius, 4)
    else:
        screen.fill(COLOR_BLUE)
        pygame.draw.circle(screen, COLOR_RED, (circle_x, circle_y), radius, 4)
    pygame.display.flip()

pygame.quit()


