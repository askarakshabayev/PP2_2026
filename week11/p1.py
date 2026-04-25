import pygame

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Example 1")

clock = pygame.time.Clock()

is_over = False

mouse_pressed = False
cur_x = cur_y = prev_x = prev_y = 0
t = 1

while not is_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                t += 1
            if event.key == pygame.K_MINUS:
                if t > 1:
                    t -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            cur_x, cur_y = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
        if event.type == pygame.MOUSEMOTION:
            if mouse_pressed:
                prev_x, prev_y = cur_x, cur_y
                cur_x, cur_y = event.pos
                pygame.draw.line(screen, (50, 34, 134), (prev_x, prev_y), (cur_x, cur_y), t)
    pygame.display.flip()
    clock.tick(60)            
            
pygame.quit()