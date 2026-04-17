# Lecture 12 — Pygame: Mouse Events, Sprites, Collisions

Each example is built **piece by piece**. Copy the snippet, read the explanation, then copy the next snippet on top. By the end of each section you will have the full working file.

Order of files:

1. `paint/01.py` — mouse events (console only)
2. `paint/02.py` — freehand drawing with lines
3. `paint/03.py` — rectangle tool (reveals a trail bug)
4. `paint/04.py` — rubber-band preview with `base_layer`
5. `01.py` — a single sprite
6. `02.py` — sprite groups (falling stars)
7. `03.py` — player + enemy
8. `04.py` — collisions and score
9. `05.py` — `USEREVENT` timer and `sprite.kill()`
10. `racer.py` — final game

---

## `paint/01.py` — Mouse Events

**Goal:** understand mouse events. We do NOT draw anything yet — we just print events to the console.

### Step 1 — window boilerplate

```python
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - Mouse Events")
clock = pygame.time.Clock()
```

We initialize Pygame, open an 800×600 window, and create a `Clock` that will cap the frame rate.

### Step 2 — main loop with QUIT

```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

The `for event in pygame.event.get()` loop is how Pygame hands us input. `pygame.QUIT` fires when the user closes the window. `clock.tick(60)` keeps the game at 60 FPS.

Run the file now — you should get an empty window that closes cleanly.

### Step 3 — detect left mouse button down

Add two state variables **before** the loop:

```python
LMBpressed = False
THICKNESS = 5
```

And inside the event loop, right after the `QUIT` check:

```python
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("LMB pressed!")
            LMBpressed = True
```

`event.button == 1` means the left mouse button. `LMBpressed` will later tell us "keep drawing while the button is held".

### Step 4 — mouse motion

```python
        if event.type == pygame.MOUSEMOTION:
            print(f"pos: {event.pos}  LMB: {LMBpressed}")
```

`MOUSEMOTION` fires whenever the mouse moves over the window. `event.pos` is a `(x, y)` tuple with the current position.

### Step 5 — left mouse button up

```python
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            print("LMB released!")
            LMBpressed = False
```

Release resets our flag. Together `DOWN` + `UP` give us the "is the user dragging right now?" pattern.

### Step 6 — change thickness with `+` / `-`

```python
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
                print(f"thickness: {THICKNESS}")
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
                print(f"thickness: {THICKNESS}")
```

`K_EQUALS` is the `=`/`+` key. `max(1, …)` prevents the thickness from going below 1.

**Test:** click, move, release — watch the console output.

---

## `paint/02.py` — Freehand Drawing

**Goal:** actually draw on the screen while LMB is held. If we drew "dots" at the current mouse position, fast movement would leave gaps, because `MOUSEMOTION` does not fire on every pixel. Fix: draw a **line** from the previous position to the current one every frame.

### Step 1 — setup + state

```python
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - Freehand Lines")
clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5

currX = currY = 0
prevX = prevY = 0
```

Two pairs of coordinates: `prev*` (where we were last frame) and `curr*` (where we are now).

### Step 2 — main loop skeleton

```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

### Step 3 — on press, sync `prev` and `curr`

Inside the event loop:

```python
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX, prevY = event.pos
            currX, currY = event.pos
```

If we skipped this, the first line of a stroke would be drawn from `(0, 0)` to the current position.

### Step 4 — track motion

```python
        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
```

We don't draw inside the event — we only update `curr*`.

### Step 5 — draw the line every frame

**Outside** the event loop, before `pygame.display.flip()`:

```python
    if LMBpressed:
        pygame.draw.line(screen, "red", (prevX, prevY), (currX, currY), THICKNESS)

    prevX, prevY = currX, currY
```

Every frame we draw a short line segment and then shift `prev ← curr` for the next frame. Because `screen` is never cleared, segments accumulate into a continuous stroke.

### Step 6 — thickness and clear key

Add to `KEYDOWN`:

```python
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
            if event.key == pygame.K_c:
                screen.fill("black")
```

Press `C` to wipe the canvas.

**Test:** draw fast scribbles. No gaps.

---

## `paint/03.py` — Rectangle Tool

**Goal:** click and drag to draw a rectangle. We'll hit a problem: `pygame.Rect(x, y, w, h)` doesn't render correctly when `w` or `h` is negative. If you drag up or left, nothing appears. We fix that with a helper.

### Step 1 — the `calculate_rect` helper

```python
def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x1 - x2),
        abs(y1 - y2)
    )
```

Always returns a valid rect regardless of drag direction.

### Step 2 — setup and state

```python
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - Rectangle Tool")
clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 3
startX = startY = 0
currX  = currY  = 0
```

### Step 3 — remember where the drag started

```python
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            startX, startY = event.pos
```

### Step 4 — live preview on motion

```python
        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos
                pygame.draw.rect(
                    screen, "red",
                    calculate_rect(startX, startY, currX, currY),
                    THICKNESS
                )
```

A `THICKNESS` > 0 as the last argument draws the rect outline only.

### Step 5 — commit on release

```python
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            pygame.draw.rect(
                screen, "red",
                calculate_rect(startX, startY, currX, currY),
                THICKNESS
            )
```

### Step 6 — thickness / clear

```python
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
            if event.key == pygame.K_c:
                screen.fill("black")
```

**Test it. You will see a bug:** while dragging, every intermediate preview stays on screen, so you get a "rainbow of rectangles". Step 4 will fix that.

---

## `paint/04.py` — Rubber-band Preview (`base_layer`)

**Goal:** kill the trail bug. We can't just `screen.fill("black")` before each preview — that would wipe finished shapes too. Instead we keep **two** surfaces.

### Step 1 — a second surface

```python
screen     = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))   # starts black
```

`base_layer` holds only the **committed** drawings. `screen` is what the user sees, including the live preview.

### Step 2 — restore + preview on motion

```python
        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos
                screen.blit(base_layer, (0, 0))
                pygame.draw.rect(
                    screen, "red",
                    calculate_rect(startX, startY, currX, currY),
                    THICKNESS
                )
```

Order matters: **first** restore the canvas from `base_layer`, **then** draw the preview on top. That way the old previews vanish but finished shapes stay.

### Step 3 — commit on release

```python
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            pygame.draw.rect(
                screen, "red",
                calculate_rect(startX, startY, currX, currY),
                THICKNESS
            )
            base_layer.blit(screen, (0, 0))
```

After the final rect is drawn on `screen`, we copy the whole `screen` back into `base_layer` — that's the "commit".

### Step 4 — clear BOTH layers

```python
            if event.key == pygame.K_c:
                screen.fill("black")
                base_layer.fill("black")
```

If you only clear `screen`, the next `MOUSEMOTION` would restore everything back from `base_layer`.

**Test:** draw many rectangles. No trail. Existing shapes survive.

> Optional: open `paint/01_.py` for a combined `LINE`/`RECT` version, useful as a second look at the same mechanics.

---

## `01.py` — A Basic Sprite

**Goal:** introduce `pygame.sprite.Sprite`. A sprite is just an object with two attributes Pygame needs:
- `self.image` — the `Surface` to draw
- `self.rect` — where to draw it

### Step 1 — setup

```python
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - Basic Sprite")
clock = pygame.time.Clock()
```

### Step 2 — the `Ball` class

```python
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()                                   # required
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
```

`super().__init__()` registers the sprite internally. `get_rect(center=…)` gives us a rect positioned at the center of the screen.

### Step 3 — add movement

```python
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]: self.rect.move_ip(5, 0)
        if keys[pygame.K_UP]:    self.rect.move_ip(0, -5)
        if keys[pygame.K_DOWN]:  self.rect.move_ip(0, 5)
```

`move_ip` = "move in place" — mutates the existing rect. `pygame.key.get_pressed()` returns the current keyboard state (unlike `KEYDOWN`, which only fires once per press).

### Step 4 — group and main loop

```python
ball = Ball()
all_sprites = pygame.sprite.Group()
all_sprites.add(ball)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill("black")
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

`group.update()` calls `update()` on every sprite. `group.draw(screen)` blits every sprite's `.image` at its `.rect`.

> `01_.py` adds two extra balls — same class, different `center`. All of them move together because they share the same `update` logic.

---

## `02.py` — Sprite Groups (Starfield)

**Goal:** use a group to manage many sprites at once.

### Step 1 — the `Star` class, init

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - Sprite Groups")
clock = pygame.time.Clock()


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(4, 12)
        self.image = pygame.Surface((size, size))
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = random.randint(1, 4)
```

Each star gets a random size, random position and random speed.

### Step 2 — falling `update`

```python
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, WIDTH)
```

When a star drops off the bottom edge, we teleport it above the top edge at a random column → infinite starfield.

### Step 3 — spawn a bunch and run

```python
stars = pygame.sprite.Group()
for _ in range(60):
    stars.add(Star())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    stars.update()
    screen.fill("black")
    stars.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

One `stars.update()` moves all 60 stars. Groups scale the same code to hundreds of sprites.

---

## `03.py` — Player and Enemy

**Goal:** a keyboard-controlled player, plus a falling enemy that respawns.

### Step 1 — setup

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - Player and Enemy")
clock = pygame.time.Clock()
FPS = 60
```

### Step 2 — `Player` with arrow keys

```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((50, 200, 50))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
```

### Step 3 — clamp the player

Still inside `update`:

```python
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
```

Without this the player can slide off the screen.

### Step 4 — `Enemy` with a reset helper

```python
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect()
        self.speed = 5
        self._reset()

    def _reset(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self._reset()
```

`_reset()` puts the enemy just above the top at a random column. The underscore prefix is just convention for "internal helper".

### Step 5 — main loop

```python
player = Player()
enemy = Enemy()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
```

---

## `04.py` — Collisions

**Goal:** detect when the player touches a block and increase the score.

### Step 1 — setup + font

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("04 - Collision Detection")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24)
```

### Step 2 — `Block`, falling with reset

```python
class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 15))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(WIDTH - 20)

    def update(self):
        self.rect.y += 3
        if self.rect.top > HEIGHT:
            self.reset_position()
```

### Step 3 — `Player` follows the mouse

```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 15))
        self.image.fill("red")
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
```

`pygame.mouse.get_pos()` gives the current cursor position, even without events.

### Step 4 — groups

```python
block_group = pygame.sprite.Group()
for _ in range(50):
    b = Block()
    b.rect.x = random.randrange(WIDTH)
    b.rect.y = random.randrange(HEIGHT)
    block_group.add(b)

player = Player()
all_sprites = pygame.sprite.Group(block_group, player)

score = 0
```

Notice a sprite can be in **several groups at once** — `player` is in `all_sprites`, blocks are in both `block_group` and `all_sprites`.

### Step 5 — the collision check

Inside the main loop, after `all_sprites.update()`:

```python
    hit_list = pygame.sprite.spritecollide(player, block_group, True)
    for block in hit_list:
        block.reset_position()
        score += 1
```

- `spritecollide(sprite, group, dokill)` — returns the list of colliding sprites. `dokill=True` auto-removes them from the group.
- `spritecollideany(sprite, group)` — returns just the first hit (or `None`), useful for "did we crash?" checks.

### Step 6 — score text

```python
    screen.fill("white")
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, "black")
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
```

`font.render(text, antialias, color)` returns a Surface you can `blit` anywhere.

---

## `05.py` — `USEREVENT` and `sprite.kill()`

**Goal:** spawn objects on a timer instead of creating them all up front, and let them self-remove when off-screen.

### Step 1 — custom event + timer

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("05 - USEREVENT + kill()")
clock = pygame.time.Clock()

SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, 1500)   # fire every 1.5 s
```

`pygame.USEREVENT` is a base id for your own events; `+1`, `+2`, … let you define multiple.

### Step 2 — `Car` class with `kill()`

```python
COLORS = ["red", "blue", "orange", "purple", "cyan"]

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(random.choice(COLORS))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(15, WIDTH - 15)
        self.rect.bottom = 0
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
```

`self.kill()` removes the sprite from every group it belongs to; with no references left, Python's GC cleans it up.

### Step 3 — spawn inside the event loop

```python
cars = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_CAR:
            cars.add(Car())

    cars.update()

    screen.fill((50, 50, 50))
    cars.draw(screen)

    count = pygame.font.SysFont("Verdana", 20).render(
        f"Cars: {len(cars)}", True, "white"
    )
    screen.blit(count, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

`len(cars)` should stabilize, not grow forever — that's proof `kill()` works.

---

## `racer.py` — Final Game

**Goal:** combine sprites, groups, collisions, `USEREVENT`, assets, sound and text into a small game.

### Step 1 — imports, window, fonts

```python
import pygame
import random
import sys
import time

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
FPS = 60

font_big   = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
```

### Step 2 — load images and sound once

```python
image_background = pygame.image.load("resources/AnimatedStreet.png")
image_player     = pygame.image.load("resources/Player.png")
image_enemy      = pygame.image.load("resources/Enemy.png")

pygame.mixer.music.load("resources/background.wav")
pygame.mixer.music.play(-1)   # -1 = loop forever

sound_crash = pygame.mixer.Sound("resources/crash.wav")
```

Asset loading is expensive — never do it inside the main loop. Paths are relative to the working directory, so run from `week11/`.

### Step 3 — globals + timer

```python
SPEED = 5
SCORE = 0

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)   # every second
```

### Step 4 — `Player`

```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if self.rect.left < 0:      self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
```

### Step 5 — `Enemy` (uses the global `SPEED` + increments score)

```python
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self._reset()

    def _reset(self):
        global SCORE
        SCORE += 1
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

    def update(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self._reset()
```

Every time an enemy loops back to the top, the player earns a point.

### Step 6 — create sprites and groups

```python
player = Player()
enemy1 = Enemy()
enemy2 = Enemy()
enemy2.rect.bottom = -HEIGHT // 2   # stagger — different starting y

all_sprites   = pygame.sprite.Group(player, enemy1, enemy2)
enemy_sprites = pygame.sprite.Group(enemy1, enemy2)
```

Two groups: `all_sprites` for drawing/updating, `enemy_sprites` for collision checks.

### Step 7 — main loop, speed up over time

```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == INC_SPEED:
            SPEED += 0.5

    all_sprites.update()

    screen.blit(image_background, (0, 0))
    all_sprites.draw(screen)

    score_surf = font_small.render(
        f"Score: {int(SCORE)}   Speed: {SPEED:.1f}", True, "black"
    )
    screen.blit(score_surf, (10, 10))
```

### Step 8 — collision → Game Over screen

Still inside the loop, before `pygame.display.flip()`:

```python
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        screen.fill("red")
        go_surf = font_big.render("Game Over", True, "black")
        go_rect = go_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        sc_surf = font_small.render(f"Final score: {int(SCORE)}", True, "black")
        sc_rect = sc_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(go_surf, go_rect)
        screen.blit(sc_surf, sc_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(FPS)
```

`spritecollideany` returns a truthy value if the player overlaps any enemy. On hit we play the crash sound, freeze for a second (dramatic pause), show the Game Over screen, wait 3 s, then quit.

### Step 9 — run it

```bash
cd week11
python racer.py
```

You now have a small but complete game:
- player controlled with ← / →
- enemies that respawn
- score per dodged enemy
- speed increasing every second
- background music + crash sound
- Game Over screen on collision

---

## Skills You Should Now Have

- Mouse events: `MOUSEBUTTONDOWN`, `MOUSEMOTION`, `MOUSEBUTTONUP`, `event.pos`, `event.button`.
- Freehand line drawing with a `prev` / `curr` pair.
- `calculate_rect` for any drag direction.
- Rubber-band preview using a `base_layer` `Surface`.
- Building sprites by subclassing `pygame.sprite.Sprite` (`image` + `rect` + `update`).
- Moving sprites with `move_ip` and reading `pygame.key.get_pressed()`.
- `pygame.sprite.Group` for bulk `update()` / `draw()`.
- Clamping sprites to screen and resetting them off-edge.
- Collision checks with `spritecollide(..., dokill)` and `spritecollideany`.
- `USEREVENT` + `pygame.time.set_timer` for periodic spawns.
- `sprite.kill()` for auto-cleanup.
- Loading images and sounds, rendering text with `font.render`.
- Assembling everything into a game (`racer.py`).
