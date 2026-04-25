# Lecture 13 — Snake: Architecture, Grid, States, Score

We build the classic Snake game **piece by piece**, starting from a naive pixel version and ending with a fully architected game that has menus, pause, game-over, walls with levels, and a persistent high score.

Each step is a separate file. Copy a snippet, read the explanation, then add the next snippet on top. By the end of each section you will have the full working file.

Order of files:

1. `01_pixel.py` — naive pixel-based snake (one file)
2. `02_grid.py` — refactor to a tile grid
3. `03_oop/` — split into `game_object.py` + `snake.py` + `food.py` + `wall.py` + `main.py` with levels loaded from `.txt` files
4. `04_states.py` — `MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`
5. `05_snake.py` — `ScoreManager` with persistent high score

---

## Snake Game Architecture

Every frame of the game loop does the same four things:

```
┌────────────┐   ┌────────────┐   ┌────────────────┐   ┌──────────┐
│  1. INPUT  │ → │ 2. UPDATE  │ → │ 3. COLLISIONS  │ → │ 4. DRAW  │
└────────────┘   └────────────┘   └────────────────┘   └──────────┘
 keyboard          snake.move()    snake vs wall         background
 events            food timer      snake vs self         food
                                   snake vs food         snake
```

We will grow this skeleton in every section:

| Concept            | Introduced in   | Responsibility                           |
| ------------------ | --------------- | ---------------------------------------- |
| `Snake`            | `01_pixel.py`   | Body, direction, movement, growth        |
| `Food`             | `01_pixel.py`   | Where to eat, how to respawn             |
| **Grid (tiles)**   | `02_grid.py`    | Everything snaps to cells                |
| `GameObject` base  | `03_oop/`       | Shared `draw()` — DRY                    |
| `Wall` + levels    | `03_oop/`       | Static obstacles loaded from disk        |
| `State`            | `04_states.py`  | `MENU` / `PLAYING` / `PAUSED` / `OVER`   |
| `ScoreManager`     | `05_snake.py`   | Current score, high score, persistence   |

The key idea: every time we add a new responsibility, we try to **give it its own class**. The main loop stays short — it just orchestrates objects.

---

## `01_pixel.py` — A Naive Pixel Snake

**Goal:** get *something* on the screen that moves and grows. We will not worry about cells yet — the snake moves by 5 pixels per frame and the food is a small rectangle we test with a range check. This is intentionally the "wrong" way so the next section has something to fix.

### Step 1 — setup

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - Pixel Snake")
clock = pygame.time.Clock()
```

Nothing new — the same boilerplate as lecture 11.

### Step 2 — `Snake` stores a list of `[x, y]` positions

```python
class Snake:
    def __init__(self, x, y):
        self.elements = [[x, y]]
        self.radius = 10
        self.dx = 5
        self.dy = 0
        self.grow = False
```

`self.elements` is the body: a list of `[x, y]` points where `elements[0]` is the head and each next entry follows the previous one. `dx`/`dy` is the direction in pixels per frame. `self.grow` is a flag we flip when the snake eats food.

### Step 3 — draw circles

```python
    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (0, 200, 0), element, self.radius)
```

A circle per body segment. `pygame.draw.circle` takes `(surface, color, center, radius)`.

### Step 4 — the movement trick

```python
    def move(self):
        if self.grow:
            self.elements.append([0, 0])
            self.grow = False
        for i in range(len(self.elements) - 1, 0, -1):
            self.elements[i][0] = self.elements[i - 1][0]
            self.elements[i][1] = self.elements[i - 1][1]
        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy
```

Read the loop carefully — this is the heart of the snake:

- If `grow` is set, append one dummy segment to the tail. Its position will be overwritten in the next frame, so the initial `[0, 0]` doesn't matter.
- Walk the body **from tail to head**, copying each segment's previous segment into it. This shifts the whole body one step along itself.
- Finally, move the **head** by `(dx, dy)`.

Going head-to-tail would overwrite data you still need. Going tail-to-head is safe.

### Step 5 — eat with a sloppy range check

```python
    def eat(self, fx, fy):
        x, y = self.elements[0]
        return fx - 10 <= x <= fx + 10 and fy - 10 <= y <= fy + 10
```

Since the snake moves 5 px per frame and the food is 10×10, we can't just compare `==` — the head would usually skip over the food. We check whether the head is *close enough*. It works, but feels wrong — you will see why in the next file.

### Step 6 — `Food`

```python
class Food:
    def __init__(self):
        self.gen()

    def gen(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(20, HEIGHT - 20)

    def draw(self):
        pygame.draw.rect(screen, (220, 60, 60), (self.x, self.y, 10, 10))
```

A tiny red rect at a random position. `gen()` is factored out so we can respawn on the same instance instead of creating a new one.

### Step 7 — the main loop

```python
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
```

Two subtle but important details:

- **`dx != -5` guards.** Without them, pressing LEFT while going RIGHT would instantly send the snake into its own neck.
- **Eat *before* moving.** If we moved first and then checked, the head could jump past the food in one tick.

**Run it.** You should see a green circle-snake that grows.

### Why this file is a dead end

- Food collisions are sloppy (range check instead of equality).
- Self-collision would be painful to write at the pixel level — the head would never land on an old tail position *exactly*.
- Walls would have the same problem.
- There is no real "board" — it's a 600×600 pixel soup.

The fix is **to stop thinking in pixels**. Enter the grid.

---

## `02_grid.py` — Grid Logic

**Goal:** re-express the whole game in terms of *cells* (columns and rows). The snake moves exactly one cell per tick. Collisions become `==`. A checkerboard background makes the cells visible.

### Step 1 — tile constants + setup

```python
import pygame
import random

pygame.init()
TILE = 20
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - Grid Snake")
clock = pygame.time.Clock()
```

`TILE` is the size of one cell in pixels. The window is `COLS × ROWS` cells. Now `[5, 15]` is a cell address, not a pixel.

### Step 2 — checkerboard background

```python
def draw_background():
    colors = [(30, 30, 30), (40, 40, 40)]
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(
                screen, colors[(r + c) % 2],
                pygame.Rect(c * TILE, r * TILE, TILE, TILE),
            )
```

`(r + c) % 2` flips every other tile — classic chess pattern. Converting `cell (c, r)` to a pixel rect is always `(c * TILE, r * TILE, TILE, TILE)`. Remember this conversion.

### Step 3 — `Snake` in cell space

```python
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
```

Three changes vs. `01_pixel.py`:

- `body` stores `[col, row]`, not `[x, y]`.
- `dx`/`dy` are `±1` (cells), not `±5` (pixels).
- The new tail copies the **last** tail cell (`list(self.body[-1])`), not `[0, 0]` — this means new segments don't briefly flicker at the top-left.

### Step 4 — real collision helpers

```python
    def head(self):
        return self.body[0]

    def hits_self(self):
        return self.body[0] in self.body[1:]

    def hits_wall(self):
        c, r = self.body[0]
        return c < 0 or c >= COLS or r < 0 or r >= ROWS
```

`self.body[0] in self.body[1:]` does exact equality on lists — exactly what we couldn't do in the pixel version. "Head on a tail cell" = `True`. This is the win of moving to a grid.

### Step 5 — draw snake

```python
    def draw(self):
        for c, r in self.body:
            pygame.draw.rect(
                screen, (0, 200, 0),
                pygame.Rect(c * TILE, r * TILE, TILE, TILE),
            )
```

Same `(c * TILE, r * TILE, TILE, TILE)` translation as the background.

### Step 6 — `Food` picks a random free cell

```python
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
```

`respawn(blocked)` accepts a list of forbidden cells (the snake body) and keeps rolling until it picks one that's free. Without this, food could spawn **inside** the snake and become impossible to eat as the snake grows.

### Step 7 — the main loop, now clean

```python
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
```

Note `clock.tick(10)` — 10 moves per second, which is the right pace for a grid game. The pixel version at 30 FPS was moving 5 px per frame = 150 px/sec; this is 10 cells × 20 px = 200 px/sec but much more *controllable* because each input maps to one discrete move.

**Run it.** Exact collisions. Clean cells. Game over when you hit a wall or yourself.

---

## `03_oop/` — Splitting Into Files, Adding Walls and Levels

**Goal:** extract a shared base class, split each concept into its own file, and add **walls loaded from text files**. This is where the project starts to feel like a real codebase.

Directory layout:

```
03_oop/
├── game_object.py
├── snake.py
├── food.py
├── wall.py
├── main.py
└── levels/
    ├── level0.txt
    ├── level1.txt
    └── level2.txt
```

### Step 1 — `game_object.py`: `Point` + `GameObject`

```python
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
```

Two things earn their own names here:

- **`Point`** replaces `[c, r]`. We get `__eq__` so `head == food.points[0]` does what we expect, and `__hash__` so we could put points in a `set` later if we wanted fast `in` lookups.
- **`GameObject`** owns `points`, `color`, `tile`, and a single `draw()` that fills a cell and strokes its border. Snake, Food, and Wall will all `draw()` through this one method — **no duplication**.

### Step 2 — `snake.py`

```python
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
```

Differences from `02_grid.py`:

- `Snake` *is a* `GameObject`: we reuse `draw()` for free — we no longer write it here.
- `body` → `points` (inherited), `[c, r]` → `Point(c, r)`.
- `process_input(events)` lives on the snake, not in `main`. The main loop only passes the event list — it doesn't know which keys mean what. This is the whole point of OOP: each class owns its concerns.

### Step 3 — `food.py`

```python
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
```

`can_eat(head)` reads nicely in the caller: `if food.can_eat(snake.head()): ...`. The food "knows" whether it has been eaten — `main` doesn't read the coordinates.

### Step 4 — `wall.py`

```python
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
```

`load()` walks a text file line by line (row) and char by char (col), pushing a `Point` for every `#`. `next_level()` cycles through `level0.txt → level1.txt → level2.txt → level0.txt`. No graphics work — a level designer could edit the `.txt` files and we'd never touch code.

### Step 5 — a `levels/` folder

Create three text files in `levels/`. Each is 30 lines × 30 columns. Characters:

- `#` — a wall cell
- anything else (we use `.`) — empty

`levels/level0.txt` — empty, just open space:

```
..............................
..............................
  (... 30 lines total, all dots)
..............................
```

`levels/level1.txt` — a box in the middle:

```
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..........##########..........
..........#........#..........
..........#........#..........
..........#........#..........
..........#........#..........
..........#........#..........
..........#........#..........
..........##########..........
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..............................
..............................
```

`levels/level2.txt` — scattered obstacles (see the repo for the exact file). The point is that you can **design a level in a text editor**, no code changes needed.

### Step 6 — `main.py` ties it together

```python
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
```

Compare to the big main loop in `02_grid.py`. The logic is the same, but now:

- Input dispatch is the snake's responsibility (`snake.process_input`).
- Drawing is the object's responsibility (`wall.draw`, `snake.draw`, `food.draw`).
- Food respawns avoid both the snake **and** the wall (`snake.points + wall.points`).
- Every 3 segments, the level cycles.

**Run it:**

```bash
cd week12/snake/03_oop
python main.py
```

### Why this matters

The pixel version in `01_pixel.py` was ~60 lines. `03_oop` is ~130 lines across 5 files — longer but each file is short, each class has one job, and adding a new kind of object (poison? moving walls? portals?) is "write one more subclass of `GameObject`". We traded a few extra lines for the ability to grow.

---

## `04_states.py` — Game States

**Goal:** the game needs a title screen ("press ENTER to start"), the ability to pause, and a game-over screen. A Snake object always "exists", but it should only **move** during `PLAYING`. The clean way to express this is a state machine.

### Step 1 — setup + fonts

```python
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
```

### Step 2 — a `State` "enum"

```python
class State:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
```

### Step 3 — `Snake` with a `reset()`

```python
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [[15, 15]]
        self.dx, self.dy = 1, 0
        self.grow = False
    # ... move(), head(), hits_self(), hits_wall(), draw() as before
```

We extract init into `reset()` so that after GAME_OVER we can start a fresh game without re-creating the object.

### Step 4 — `Food` (unchanged) and `draw_background()` (unchanged).

### Step 5 — a tiny centered-text helper

```python
def draw_center(text, font, y, color=(255, 255, 255)):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)
```

`font.render` returns a surface; `get_rect(center=...)` positions it. This saves a lot of repeated `blit` boilerplate on menus.

### Step 6 — the state-aware event loop

```python
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
```

Read the transitions out loud: "in MENU, ENTER goes to PLAYING". "In PLAYING, SPACE pauses, arrows turn". "In PAUSED, SPACE resumes". "In GAME_OVER, ENTER restarts". The whole state machine fits in one block of code.

### Step 7 — updates happen only in `PLAYING`

```python
    if state == State.PLAYING:
        snake.move()
        if snake.hits_wall() or snake.hits_self():
            state = State.GAME_OVER
        elif snake.head() == [food.c, food.r]:
            snake.grow = True
            food.respawn(snake.body)
```

Input was always processed (arrow keys, menus), but the snake only *moves* in `PLAYING`. In `PAUSED` the world freezes.

### Step 8 — draw the right overlay

```python
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
```

We always draw the world first, then overlay the menu/pause/game-over text **only if** we're in that state. `PLAYING` draws nothing extra.

**Test:** launch → title screen → ENTER → play → SPACE → frozen with "PAUSED" over the board → SPACE → unfrozen → crash → GAME OVER → ENTER → fresh game.

---

## `05_snake.py` — Score Manager with Persistent High Score

**Goal:** add a score that goes up when you eat, a high score that **survives closing the program**, a HUD strip at the top of the screen, and a bit of difficulty (snake speeds up every 5 segments, occasional gold food worth 5 points).

Everything from `04_states.py` stays. We add one new class.

### Step 1 — HUD strip + file constant

```python
TILE = 20
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + 40   # +40 HUD strip on top
GRID_TOP = 40

HIGHSCORE_FILE = "highscore.txt"
```

We add 40 pixels to the window height and offset the grid by `GRID_TOP`. Every `y = r * TILE` becomes `y = GRID_TOP + r * TILE` — the grid moves down, the strip at the top is for text.

### Step 2 — `ScoreManager`

```python
import os

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
```

Breakdown:

- `current` — score for this run.
- `high` — best score ever seen (loaded from disk on construction).
- `_load()` — returns `0` if the file is missing or garbage. Graceful handling of a first run, or of a user who edited the file to something invalid.
- `_save()` — called only when we beat the record. Writes the high as a plain integer.
- `reset()` — called on restart. Notice we **don't** touch `self.high` here — the record survives across games.

The underscore prefix on `_load` / `_save` is the Python convention for "internal to the class". Callers should only use `add`, `reset`, and read `current`/`high`.

### Step 3 — bonus food

```python
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
        self.points = 5 if random.random() < 0.2 else 1

    def draw(self):
        color = (255, 215, 0) if self.points == 5 else (220, 60, 60)
        pygame.draw.rect(
            screen, color,
            pygame.Rect(self.c * TILE, GRID_TOP + self.r * TILE, TILE, TILE),
        )
```

20% of spawns are **gold food** worth 5 points. `Food` carries its own `points` value — the `ScoreManager` only needs to be told `add(food.points)`. No `if/else` in `main`.

### Step 4 — speed ramp

```python
class Snake:
    def reset(self):
        self.body = [[15, 15]]
        self.dx, self.dy = 1, 0
        self.grow = False
        self.speed = 8
```

And in the main loop after eating:

```python
    if len(snake.body) % 5 == 0:
        snake.speed += 1
```

Used as `clock.tick(snake.speed)` at the bottom of the loop. Every 5th segment the game ticks one frame faster.

### Step 5 — HUD render

```python
def draw_hud(score):
    s = font_small.render(f"Score: {score.current}", True, (255, 255, 255))
    h = font_small.render(f"High:  {score.high}", True, (255, 215, 0))
    screen.blit(s, (10, 8))
    screen.blit(h, (WIDTH - h.get_width() - 10, 8))
```

Score top-left, high score top-right. `h.get_width()` lets us right-align without hard-coding pixel positions.

### Step 6 — wiring

After eating:

```python
    snake.grow = True
    score.add(food.points)
    if len(snake.body) % 5 == 0:
        snake.speed += 1
    food.respawn(snake.body, len(snake.body))
```

On restart:

```python
    elif state == State.GAME_OVER and event.key == pygame.K_RETURN:
        snake.reset()
        score.reset()
        food.respawn(snake.body, len(snake.body))
        state = State.PLAYING
```

And on GAME_OVER overlay:

```python
    draw_center("GAME OVER", font_big, HEIGHT // 2 - 60)
    draw_center(f"Score: {score.current}", font_small, HEIGHT // 2)
    draw_center(f"High Score: {score.high}", font_small, HEIGHT // 2 + 30)
    draw_center("Press ENTER to restart", font_small, HEIGHT // 2 + 70)
```

**Test:** close the game after scoring. Reopen. The high score is still there — that's the disk persistence working.

