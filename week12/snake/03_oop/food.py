import random

from game_object import GameObject, Point


class Food(GameObject):
    def __init__(self, tile, cols, rows):
        super().__init__([Point(15, 15)], (220, 60, 60), tile)
        self.cols = cols
        self.rows = rows

    def can_eat(self, head):
        return head == self.points[0]

    def respawn(self, blocked):
        while True:
            p = Point(
                random.randint(0, self.cols - 1),
                random.randint(0, self.rows - 1),
            )
            if p not in blocked:
                self.points = [p]
                return
