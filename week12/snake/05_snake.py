import pygame
import random
import os

pygame.init()
TILE = 20
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + 40  # +40 HUD strip on top
GRID_TOP = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("05 - Snake with Score Manager")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("Verdana", 48)
font_small = pygame.font.SysFont("Verdana", 20)

HIGHSCORE_FILE = "highscore.txt"


class State:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class ScoreManager:
    def __init__(self, path=HIGHSCORE_FILE):
        self.path = path
        self.current = 0
        self.high = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return 0
        try:
            with open(self.path) as f:
                return int(f.read().strip() or 0)
        except ValueError:
            return 0

    def _save(self):
        with open(self.path, "w") as f:
            f.write(str(self.high))

    def add(self, points):
        self.current += points
        if self.current > self.high:
            self.high = self.current
            self._save()

    def reset(self):
        self.current = 0


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [[15, 15]]
        self.dx, self.dy = 1, 0
        self.grow = False
        self.speed = 8

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
        for i, (c, r) in enumerate(self.body):
            color = (0, 220, 0) if i == 0 else (0, 170, 0)
            pygame.draw.rect(
                screen, color,
                pygame.Rect(c * TILE, GRID_TOP + r * TILE, TILE, TILE),
            )


class Food:
    def __init__(self):
        self.c, self.r = 10, 10
        self.points = 1

    def respawn(self, blocked, length):
        while True:
            self.c = random.randint(0, COLS - 1)
            self.r = random.randint(0, ROWS - 1)
            if [self.c, self.r] not in blocked:
                break
        # occasional bonus food — worth 5 points
        self.points = 5 if random.random() < 0.2 else 1

    def draw(self):
        color = (255, 215, 0) if self.points == 5 else (220, 60, 60)
        pygame.draw.rect(
            screen, color,
            pygame.Rect(self.c * TILE, GRID_TOP + self.r * TILE, TILE, TILE),
        )


def draw_background():
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(0, 0, WIDTH, GRID_TOP))
    colors = [(30, 30, 30), (40, 40, 40)]
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(
                screen, colors[(r + c) % 2],
                pygame.Rect(c * TILE, GRID_TOP + r * TILE, TILE, TILE),
            )


def draw_hud(score):
    s = font_small.render(f"Score: {score.current}", True, (255, 255, 255))
    h = font_small.render(f"High:  {score.high}", True, (255, 215, 0))
    screen.blit(s, (10, 8))
    screen.blit(h, (WIDTH - h.get_width() - 10, 8))


def draw_center(text, font, y, color=(255, 255, 255)):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)


snake = Snake()
food = Food()
score = ScoreManager()
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
                score.reset()
                food.respawn(snake.body, len(snake.body))
                state = State.PLAYING

    if state == State.PLAYING:
        snake.move()
        if snake.hits_wall() or snake.hits_self():
            state = State.GAME_OVER
        elif snake.head() == [food.c, food.r]:
            snake.grow = True
            score.add(food.points)
            if len(snake.body) % 5 == 0:
                snake.speed += 1
            food.respawn(snake.body, len(snake.body))

    draw_background()
    food.draw()
    snake.draw()
    draw_hud(score)

    if state == State.MENU:
        draw_center("SNAKE", font_big, HEIGHT // 2 - 40)
        draw_center("Press ENTER to play", font_small, HEIGHT // 2 + 20)
    elif state == State.PAUSED:
        draw_center("PAUSED", font_big, HEIGHT // 2 - 20)
        draw_center("Press SPACE to resume", font_small, HEIGHT // 2 + 30)
    elif state == State.GAME_OVER:
        draw_center("GAME OVER", font_big, HEIGHT // 2 - 60)
        draw_center(f"Score: {score.current}", font_small, HEIGHT // 2)
        draw_center(f"High Score: {score.high}", font_small, HEIGHT // 2 + 30)
        draw_center("Press ENTER to restart", font_small, HEIGHT // 2 + 70)

    pygame.display.flip()
    clock.tick(snake.speed)

pygame.quit()
