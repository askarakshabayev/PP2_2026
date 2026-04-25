import pygame

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
base_layer = pygame.Surface((W, H))
pygame.display.set_caption("Example 1")

clock = pygame.time.Clock()

is_over = False

mouse_pressed = False
cur_x = cur_y = prev_x = prev_y = 0
t = 1

def calculate_rect(x1, y1, x2, y2):
    return min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)

tool = "PEN"
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
            if event.key == pygame.K_p:
                tool = "PEN"
            if event.key == pygame.K_r:
                tool = "RECT"
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            if tool == "RECT":
                prev_x, prev_y = event.pos
            if tool == "PEN":
                cur_x, cur_y = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            if tool == "RECT":
                cur_x, cur_y = event.pos
                pygame.draw.rect(base_layer, (50, 24, 150), calculate_rect(prev_x, prev_y, cur_x, cur_y), t)
        if event.type == pygame.MOUSEMOTION:
            if mouse_pressed:
                screen.blit(base_layer, (0, 0))
                if tool == "RECT":
                    cur_x, cur_y = event.pos
                    pygame.draw.rect(screen, (50, 24, 150), calculate_rect(prev_x, prev_y, cur_x, cur_y), t)
                if tool == "PEN":
                    prev_x, prev_y = cur_x, cur_y
                    cur_x, cur_y = event.pos
                    pygame.draw.line(base_layer, (34, 76, 56), (prev_x, prev_y), (cur_x, cur_y), t)
    pygame.display.flip()
    clock.tick(60)            
            
pygame.quit()