import pygame

from food import Food
from snake import Snake
from wall import Wall

TILE = 20
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE


def draw_background(screen):
    colors = [(30, 30, 30), (40, 40, 40)]
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(
                screen, colors[(r + c) % 2],
                pygame.Rect(c * TILE, r * TILE, TILE, TILE),
            )


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("03 - OOP Snake with Walls")
    clock = pygame.time.Clock()

    snake = Snake(TILE)
    food = Food(TILE, COLS, ROWS)
    wall = Wall(TILE)

    running = True
    while running:
        events = []
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            else:
                events.append(e)

        snake.process_input(events)
        snake.move()

        head = snake.head()
        out_of_bounds = head.c < 0 or head.c >= COLS or head.r < 0 or head.r >= ROWS
        if out_of_bounds or snake.hits_self() or wall.hits(head):
            running = False

        if food.can_eat(head):
            snake.grow = True
            food.respawn(snake.points + wall.points)
            if len(snake.points) % 3 == 0:
                wall.next_level()

        draw_background(screen)
        wall.draw(screen)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.flip()
        clock.tick(8)

    pygame.quit()


if __name__ == "__main__":
    main()
