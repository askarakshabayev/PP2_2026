import pygame

# Rectangle drawing tool.
# Problem: pygame.Rect(x, y, w, h) requires POSITIVE width and height.
# If the user drags up or left, w/h become negative → rect doesn't draw.
# Solution: calculate_rect() always returns a valid rect regardless of drag direction.

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - Rectangle Tool")
clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 3

startX = startY = 0
currX  = currY  = 0


def calculate_rect(x1, y1, x2, y2):
    """Return a valid Rect from any two corner points (handles negative w/h)."""
    return pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x1 - x2),
        abs(y1 - y2)
    )


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            startX, startY = event.pos

        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos
                # draw preview while dragging (leaves trail — see 04.py for fix)
                pygame.draw.rect(
                    screen, "red",
                    calculate_rect(startX, startY, currX, currY),
                    THICKNESS
                )

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            pygame.draw.rect(
                screen, "red",
                calculate_rect(startX, startY, currX, currY),
                THICKNESS
            )

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
            if event.key == pygame.K_c:
                screen.fill("black")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
