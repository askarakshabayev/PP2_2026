import pygame

from game_object import GameObject, Point


class Snake(GameObject):
    def __init__(self, tile):
        super().__init__([Point(5, 15)], (0, 200, 0), tile)
        self.dx = 1
        self.dy = 0
        self.grow = False

    def head(self):
        return self.points[0]

    def move(self):
        if self.grow:
            self.points.append(self.points[-1].copy())
            self.grow = False
        for i in range(len(self.points) - 1, 0, -1):
            self.points[i].c = self.points[i - 1].c
            self.points[i].r = self.points[i - 1].r
        self.points[0].c += self.dx
        self.points[0].r += self.dy

    def hits_self(self):
        return self.points[0] in self.points[1:]

    def process_input(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_RIGHT and self.dx != -1:
                self.dx, self.dy = 1, 0
            elif event.key == pygame.K_LEFT and self.dx != 1:
                self.dx, self.dy = -1, 0
            elif event.key == pygame.K_UP and self.dy != 1:
                self.dx, self.dy = 0, -1
            elif event.key == pygame.K_DOWN and self.dy != -1:
                self.dx, self.dy = 0, 1
