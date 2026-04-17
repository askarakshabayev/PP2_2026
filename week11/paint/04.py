import pygame

# Rubber-band rectangle preview using a base_layer Surface.
#
# Problem in 03.py: every MOUSEMOTION draws a new rect on top of the last one
# → the screen fills with overlapping rectangles during drag.
#
# Bad fix: screen.fill() before each preview → erases everything the user drew.
#
# Correct fix: base_layer
#   - base_layer stores the "committed" canvas (only finished rectangles)
#   - on MOUSEMOTION: restore screen from base_layer, then draw the current preview
#   - on MOUSEBUTTONUP: draw the final rect, then save screen → base_layer

pygame.init()

WIDTH, HEIGHT = 800, 600
screen     = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))   # starts black (all zeros)
pygame.display.set_caption("04 - Rubber-band Preview (base_layer)")
clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 3

startX = startY = 0
currX  = currY  = 0


def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))


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
                # Step 1: restore the committed canvas
                screen.blit(base_layer, (0, 0))
                # Step 2: draw the live preview on top
                pygame.draw.rect(
                    screen, "red",
                    calculate_rect(startX, startY, currX, currY),
                    THICKNESS
                )

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            # Draw the final rectangle
            pygame.draw.rect(
                screen, "red",
                calculate_rect(startX, startY, currX, currY),
                THICKNESS
            )
            # Commit: save the current screen into base_layer
            base_layer.blit(screen, (0, 0))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
            if event.key == pygame.K_c:
                screen.fill("black")
                base_layer.fill("black")   # clear both layers!

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
