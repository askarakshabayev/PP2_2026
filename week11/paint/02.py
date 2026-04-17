import pygame

# Freehand drawing using smooth lines.
# Problem with dots (rect): gaps appear when mouse moves fast.
# Solution: draw a LINE from (prevX, prevY) to (currX, currY) every frame.

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - Freehand Lines")
clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5

currX = currY = 0
prevX = prevY = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            # on first press, prev = curr to avoid line from (0,0)
            prevX, prevY = event.pos
            currX, currY = event.pos

        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos   # update current position

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
            if event.key == pygame.K_c:
                screen.fill("black")

    if LMBpressed:
        pygame.draw.line(screen, "red", (prevX, prevY), (currX, currY), THICKNESS)

    # save current as previous for next frame
    prevX, prevY = currX, currY

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
