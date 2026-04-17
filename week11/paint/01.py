import pygame

# Mouse events:
#   MOUSEBUTTONDOWN  — button pressed  (event.button: 1=LMB, 2=MMB, 3=RMB)
#   MOUSEMOTION      — mouse moved     (event.pos, event.rel)
#   MOUSEBUTTONUP    — button released (event.button)

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - Mouse Events")
clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("LMB pressed!")
            LMBpressed = True

        if event.type == pygame.MOUSEMOTION:
            print(f"pos: {event.pos}  LMB: {LMBpressed}")

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            print("LMB released!")
            LMBpressed = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
                print(f"thickness: {THICKNESS}")
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
                print(f"thickness: {THICKNESS}")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
