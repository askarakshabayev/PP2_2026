import pygame

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint v01")

clock = pygame.time.Clock()

is_over = False
mouse_pressed = False
cur_x = 0
cur_y = 0
prev_x = 0
prev_y = 0

while not is_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_over = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            cur_x, cur_y = event.pos
        if event.type == pygame.MOUSEMOTION:
            prev_x, prev_y = cur_x, cur_y
            cur_x, cur_y = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

        if mouse_pressed:
            pygame.draw.line(screen, (255, 23, 43), (prev_x, prev_y), (cur_x, cur_y))

    pygame.display.flip()

pygame.quit()
