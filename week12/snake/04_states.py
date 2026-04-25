import pygame
import random

pygame.init()
TILE = 20
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("04 - Game States")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("Verdana", 48)
font_small = pygame.font.SysFont("Verdana", 20)


class State:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [[15, 15]]
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
        self.c, self.r = 10, 10

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


def draw_background():
    colors = [(30, 30, 30), (40, 40, 40)]
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(
                screen, colors[(r + c) % 2],
                pygame.Rect(c * TILE, r * TILE, TILE, TILE),
            )


def draw_center(text, font, y, color=(255, 255, 255)):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)


snake = Snake()
food = Food()
state = State.MENU

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == State.MENU and event.key == pygame.K_RETURN:
                state = State.PLAYING
            elif state == State.PLAYING:
                if event.key == pygame.K_SPACE:
                    state = State.PAUSED
                elif event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx, snake.dy = 0, -1
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx, snake.dy = 0, 1
            elif state == State.PAUSED and event.key == pygame.K_SPACE:
                state = State.PLAYING
            elif state == State.GAME_OVER and event.key == pygame.K_RETURN:
                snake.reset()
                food.respawn(snake.body)
                state = State.PLAYING

    if state == State.PLAYING:
        snake.move()
        if snake.hits_wall() or snake.hits_self():
            state = State.GAME_OVER
        elif snake.head() == [food.c, food.r]:
            snake.grow = True
            food.respawn(snake.body)

    draw_background()
    food.draw()
    snake.draw()

    if state == State.MENU:
        draw_center("SNAKE", font_big, HEIGHT // 2 - 40)
        draw_center("Press ENTER to play", font_small, HEIGHT // 2 + 20)
    elif state == State.PAUSED:
        draw_center("PAUSED", font_big, HEIGHT // 2 - 20)
        draw_center("Press SPACE to resume", font_small, HEIGHT // 2 + 30)
    elif state == State.GAME_OVER:
        draw_center("GAME OVER", font_big, HEIGHT // 2 - 40)
        draw_center(f"Length: {len(snake.body)}", font_small, HEIGHT // 2 + 20)
        draw_center("Press ENTER to restart", font_small, HEIGHT // 2 + 50)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
