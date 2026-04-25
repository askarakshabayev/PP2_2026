import pygame


class Point:
    def __init__(self, c, r):
        self.c = c
        self.r = r

    def __eq__(self, other):
        return isinstance(other, Point) and self.c == other.c and self.r == other.r

    def __hash__(self):
        return hash((self.c, self.r))

    def copy(self):
        return Point(self.c, self.r)


class GameObject:
    def __init__(self, points, color, tile):
        self.points = points
        self.color = color
        self.tile = tile

    def draw(self, screen):
        for p in self.points:
            rect = pygame.Rect(p.c * self.tile, p.r * self.tile, self.tile, self.tile)
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
