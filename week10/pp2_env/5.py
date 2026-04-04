import pygame

pygame.init()

screen_size = width, height = (600, 600)

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

done = False
is_red = True
circle_x = 100
circle_y = 100
dx = 1
dy = 0
radius = 10
speed = 1
FPS = 100

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_red = not is_red
            if event.key == pygame.K_UP:
                dx, dy = 0, -speed
            if event.key == pygame.K_DOWN:
                dx, dy = 0, speed
            if event.key == pygame.K_LEFT:
                dx, dy = -speed, 0
            if event.key == pygame.K_RIGHT:
                dx, dy = speed, 0
            if event.key == pygame.K_1:
                speed += 2
    
    circle_x += dx
    circle_y += dy

    if circle_x > width + radius:
        circle_x = -radius
    if circle_y > height:
        circle_y = -radius
    if circle_x < -radius:
        circle_x = width + radius
    if circle_y < -radius:
        circle_y = height + radius


    if is_red:
        screen.fill(COLOR_RED)
        pygame.draw.circle(screen, COLOR_BLUE, (circle_x, circle_y), radius)
    else:
        screen.fill(COLOR_BLUE)
        pygame.draw.circle(screen, COLOR_RED, (circle_x, circle_y), radius)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()


