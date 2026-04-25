import pygame
import random

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - Pixel Snake")
clock = pygame.time.Clock()


class Snake:
    def __init__(self, x, y):
        self.elements = [[x, y]]
        self.radius = 10
        self.dx = 5
        self.dy = 0
        self.grow = False

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (0, 200, 0), element, self.radius)

    def move(self):
        if self.grow:
            self.elements.append([0, 0])
            self.grow = False
        for i in range(len(self.elements) - 1, 0, -1):
            self.elements[i][0] = self.elements[i - 1][0]
            self.elements[i][1] = self.elements[i - 1][1]
        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy

    def eat(self, fx, fy):
        x, y = self.elements[0]
        return fx - 10 <= x <= fx + 10 and fy - 10 <= y <= fy + 10


class Food:
    def __init__(self):
        self.gen()

    def gen(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(20, HEIGHT - 20)

    def draw(self):
        pygame.draw.rect(screen, (220, 60, 60), (self.x, self.y, 10, 10))


snake = Snake(100, 100)
food = Food()
running = True

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -5:
                snake.dx, snake.dy = 5, 0
            if event.key == pygame.K_LEFT and snake.dx != 5:
                snake.dx, snake.dy = -5, 0
            if event.key == pygame.K_UP and snake.dy != 5:
                snake.dx, snake.dy = 0, -5
            if event.key == pygame.K_DOWN and snake.dy != -5:
                snake.dx, snake.dy = 0, 5

    if snake.eat(food.x, food.y):
        snake.grow = True
        food.gen()

    snake.move()

    screen.fill((0, 0, 0))
    snake.draw()
    food.draw()
    pygame.display.flip()

pygame.quit()
