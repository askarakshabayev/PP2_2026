import pygame
import random

pygame.init()
TILE = 20
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - Grid Snake")
clock = pygame.time.Clock()


def draw_background():
    colors = [(30, 30, 30), (40, 40, 40)]
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(
                screen, colors[(r + c) % 2],
                pygame.Rect(c * TILE, r * TILE, TILE, TILE),
            )


class Snake:
    def __init__(self):
        self.body = [[5, 15]]
        self.dx, self.dy = 1, 0
        self.grow = False

    def move(self):
        if self.grow:
            self.body.append(list(self.body[-1]))
            self.grow = False
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]
        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def head(self):
        return self.body[0]

    def hits_self(self):
        return self.body[0] in self.body[1:]

    def hits_wall(self):
        c, r = self.body[0]
        return c < 0 or c >= COLS or r < 0 or r >= ROWS

    def draw(self):
        for c, r in self.body:
            pygame.draw.rect(
                screen, (0, 200, 0),
                pygame.Rect(c * TILE, r * TILE, TILE, TILE),
            )


class Food:
    def __init__(self):
        self.c, self.r = 15, 15

    def respawn(self, blocked):
        while True:
            self.c = random.randint(0, COLS - 1)
            self.r = random.randint(0, ROWS - 1)
            if [self.c, self.r] not in blocked:
                return

    def draw(self):
        pygame.draw.rect(
            screen, (220, 60, 60),
            pygame.Rect(self.c * TILE, self.r * TILE, TILE, TILE),
        )


snake = Snake()
food = Food()
running = True

while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            if event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            if event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1
            if event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1

    snake.move()

    if snake.hits_wall() or snake.hits_self():
        running = False

    if snake.head() == [food.c, food.r]:
        snake.grow = True
        food.respawn(snake.body)

    draw_background()
    snake.draw()
    food.draw()
    pygame.display.flip()

pygame.quit()
