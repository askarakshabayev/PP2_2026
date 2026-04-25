from game_object import GameObject, Point


class Wall(GameObject):
    def __init__(self, tile):
        super().__init__([], (60, 60, 200), tile)
        self.level = 0
        self.load()

    def load(self):
        self.points = []
        with open(f"levels/level{self.level}.txt") as f:
            for r, line in enumerate(f):
                for c, ch in enumerate(line.rstrip("\n")):
                    if ch == "#":
                        self.points.append(Point(c, r))

    def next_level(self):
        self.level = (self.level + 1) % 3
        self.load()

    def hits(self, point):
        return point in self.points
