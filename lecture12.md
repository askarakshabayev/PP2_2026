# Lecture 12: Pygame II

## Plan
- Paint App II (`paint/`)
  - Mouse events
  - Freehand lines (prev/curr coords)
  - Rectangle tool & `calculate_rect()`
  - Rubber-band preview with `base_layer`
- Sprites (`pygame.sprite.Sprite`)
- Sprite Groups (`pygame.sprite.Group`)
- `Rect` and `move_ip`
- Collision detection
- `USEREVENT` — timed events & `kill()`
- Racer game demo

---

## 1. Paint App II (`paint/`)

In Lecture 11 we built a basic Paint app (freehand circles, colors, eraser). Now we'll improve it: smooth lines and a rectangle tool with live preview.

---

### Mouse events (`paint/01.py`)

Three main mouse events:

```python
if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    LMBpressed = True           # left button pressed

if event.type == pygame.MOUSEMOTION:
    print(event.pos)            # (x, y) cursor position right now

if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
    LMBpressed = False          # left button released
```

`event.button`: `1` = LMB, `2` = scroll wheel, `3` = RMB.

---

### Freehand — smooth lines (`paint/02.py`)

Problem with drawing dots (`draw.rect`): when moving the mouse quickly, the gap between `MOUSEMOTION` events is large → dashed line instead of a continuous one.

**Solution:** connect the previous and current position with a line:

```python
prevX = prevY = currX = currY = 0

if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    LMBpressed = True
    prevX, prevY = event.pos   # initialize prev = curr so we don't drag a line from (0,0)
    currX, currY = event.pos

if event.type == pygame.MOUSEMOTION:
    if LMBpressed:
        currX, currY = event.pos

# outside event loop — each frame:
if LMBpressed:
    pygame.draw.line(screen, "red", (prevX, prevY), (currX, currY), THICKNESS)

prevX, prevY = currX, currY    # save for the next frame
```

---

### Rectangle Tool (`paint/03.py`)

`pygame.Rect(x, y, w, h)` requires **positive** width and height. If you drag the mouse left or up, `w` and `h` become negative — the rectangle won't draw.

**Solution — `calculate_rect()`:**

```python
def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x1 - x2),
        abs(y1 - y2)
    )
```

Now it doesn't matter which direction we drag — we always get a valid Rect.

```python
if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    LMBpressed = True
    startX, startY = event.pos

if event.type == pygame.MOUSEMOTION:
    if LMBpressed:
        currX, currY = event.pos
        pygame.draw.rect(screen, "red",
                         calculate_rect(startX, startY, currX, currY), THICKNESS)

if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
    LMBpressed = False
    pygame.draw.rect(screen, "red",
                     calculate_rect(startX, startY, *event.pos), THICKNESS)
```

**Problem with 03.py:** every `MOUSEMOTION` draws a rectangle on top of the previous one → during dragging, a trail of rectangles accumulates on screen.

---

### Rubber-band preview с `base_layer` (`paint/04.py`)

Need to show a **live preview** of the rectangle while dragging, without affecting what's already drawn.

**Bad solution:** `screen.fill("black")` before each preview — erases everything drawn.

**Correct solution — two layers:**

```
base_layer  — the "fixed" canvas (only completed shapes)
screen      — what the user sees (base_layer + current preview)
```

```python
screen     = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))   # starts black
```

Logic:

```python
if event.type == pygame.MOUSEMOTION:
    if LMBpressed:
        currX, currY = event.pos
        screen.blit(base_layer, (0, 0))       # 1. restore the fixed canvas
        pygame.draw.rect(screen, "red",       # 2. draw preview on top
                         calculate_rect(startX, startY, currX, currY), THICKNESS)

if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
    LMBpressed = False
    pygame.draw.rect(screen, "red",
                     calculate_rect(startX, startY, *event.pos), THICKNESS)
    base_layer.blit(screen, (0, 0))           # 3. commit: save screen → base_layer
```

When clearing the canvas (`K_c`) both layers must be cleared:

```python
if event.key == pygame.K_c:
    screen.fill("black")
    base_layer.fill("black")
```

**Summary:**

| Event | Action |
|---|---|
| `MOUSEBUTTONDOWN` | save `startX, startY` |
| `MOUSEMOTION` (drag) | `screen ← base_layer` → draw preview |
| `MOUSEBUTTONUP` | draw final rectangle → `base_layer ← screen` |

---

## 3. Sprites (`01.py`)

In Pygame, a **Sprite** is any game object that has:
- `.image` — a `Surface` that gets drawn
- `.rect` — a `Rect` that defines its position and size

To create a sprite, subclass `pygame.sprite.Sprite` and call `super().__init__()`:

```python
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()                   # required
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect(center=(400, 300))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]: self.rect.move_ip(5, 0)
        if keys[pygame.K_UP]:    self.rect.move_ip(0, -5)
        if keys[pygame.K_DOWN]:  self.rect.move_ip(0, 5)
```

The `update()` method is called by the group every frame — put your movement logic there.

### `Rect.move_ip(dx, dy)`

`move_ip` moves the rect **in place** (modifies the existing rect, returns nothing).

```python
self.rect.move_ip(-5, 0)   # move 5px to the left
self.rect.move_ip(0, 3)    # move 3px down
```

Contrast with `move(dx, dy)` which returns a **new** Rect without modifying the original.

### Useful `Rect` attributes for positioning

```python
rect.left, rect.right, rect.top, rect.bottom   # edges
rect.centerx, rect.centery                      # center coordinates
rect.center                                     # (cx, cy) tuple
rect.width, rect.height                         # size
```

You can set any of these directly to reposition the rect:
```python
self.rect.left = 0          # snap to left wall
self.rect.bottom = HEIGHT   # snap to bottom
self.rect.center = (400, 300)
```

---

## 4. Sprite Groups (`02.py`)

A `Group` holds a collection of sprites and lets you update and draw them all at once.

```python
all_sprites = pygame.sprite.Group()
all_sprites.add(ball)
all_sprites.add(star1, star2, star3)
# or at construction time:
all_sprites = pygame.sprite.Group(ball, star1, star2)
```

Inside the game loop:
```python
all_sprites.update()       # calls update() on every sprite
screen.fill("black")
all_sprites.draw(screen)   # blits each sprite's .image at its .rect
```

`group.draw(surface)` is equivalent to:
```python
for sprite in group:
    surface.blit(sprite.image, sprite.rect)
```

### Multiple groups

A sprite can belong to **more than one group**. This is the key technique for collision detection:

```python
all_sprites   = pygame.sprite.Group(player, enemy)
enemy_sprites = pygame.sprite.Group(enemy)
```

You update/draw via `all_sprites`, but check collisions using the focused `enemy_sprites` group.

---

## 5. Player + Enemy Movement (`03.py`)

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
        # clamp to screen
        if self.rect.left < 0:    self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH


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
        self.rect.bottom = 0   # place just above the screen

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self._reset()
```

**Pattern:** player moves left/right with clamping; enemy falls from the top and resets when it goes off the bottom.

---

## 6. Collision Detection (`04.py`)

Pygame detects overlapping rects using two main functions:

### `spritecollideany(sprite, group)`

Returns the **first** sprite in `group` that overlaps `sprite`, or `None` if none.
Use it for a simple yes/no check (e.g., did the player hit anything?).

```python
if pygame.sprite.spritecollideany(player, enemy_sprites):
    print("Hit!")
```

### `spritecollide(sprite, group, dokill)`

Returns a **list** of all sprites in `group` that overlap `sprite`.
`dokill=True` automatically removes the colliding sprites from their groups.

```python
hit_list = pygame.sprite.spritecollide(player, block_group, False)
for block in hit_list:
    block.reset_position()
    score += 1
```

| Function | Returns | dokill |
|---|---|---|
| `spritecollideany` | First hit or `None` | N/A |
| `spritecollide` | List of all hits | `True` = remove from group |

### Full example (04.py)

```python
# 50 falling blocks; mouse-controlled player; score on each hit
hit_list = pygame.sprite.spritecollide(player, block_group, False)
for block in hit_list:
    block.reset_position()   # send block back to top
    score += 1
```

Under the hood, collision uses **rect intersection** (`Rect.colliderect`). No pixel-perfect by default — good enough for most games.

---

## 7. USEREVENT — Timed events & `kill()` (`05.py`)

### Custom events with `USEREVENT`

`pygame.USEREVENT` is the first available slot for your own event types.

```python
SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, 1500)   # fires every 1500 ms
```

Handle it in the event loop like any other event:

```python
for event in pygame.event.get():
    if event.type == SPAWN_CAR:
        cars.add(Car())
```

Useful for: spawning enemies, speeding up the game, countdown timers.

### `sprite.kill()`

Removes the sprite from **all** groups it belongs to. Python will garbage-collect it when nothing else references it.

```python
def update(self):
    self.rect.y += self.speed
    if self.rect.top > HEIGHT:
        self.kill()    # gone: no manual group.remove() needed
```

```python
# Similarly, kill all sprites at once:
for sprite in all_sprites:
    sprite.kill()
```

---

## 8. Racer Game Demo (`racer.py`)

A complete game bringing together all the concepts:

```
Player  — moves left/right, clamped to screen
Enemy   — falls from top, resets with score increment on passing
Speed   — increases every second via USEREVENT
Crash   — spritecollideany detects collision → game over screen
```

### Key design choices

**Speed as a global variable** — enemies read it from the module scope so a single timer event can raise everyone's speed:

```python
SPEED = 5

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# in event loop:
if event.type == INC_SPEED:
    SPEED += 0.5

# in Enemy.update():
self.rect.move_ip(0, SPEED)
```

**Two enemy groups** — `all_sprites` for updating/drawing, `enemy_sprites` for collision:

```python
all_sprites   = pygame.sprite.Group(player, enemy1, enemy2)
enemy_sprites = pygame.sprite.Group(enemy1, enemy2)

all_sprites.update()
all_sprites.draw(screen)

if pygame.sprite.spritecollideany(player, enemy_sprites):
    # game over
```

**Staggering enemy start positions** — prevents enemies from starting at the same y:

```python
enemy2.rect.bottom = -HEIGHT // 2
```

### Full game loop structure

```python
while running:
    # 1. Events
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5

    # 2. Update
    all_sprites.update()

    # 3. Draw
    screen.fill(...)
    all_sprites.draw(screen)
    screen.blit(score_surf, ...)

    # 4. Collision check (after drawing so game over shows on top)
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        # show game over, quit
        ...

    pygame.display.flip()
    clock.tick(FPS)
```

---

## Summary

| Concept | API |
|---|---|
| **Sprite base class** | `class Foo(pygame.sprite.Sprite): super().__init__()` |
| **Required attributes** | `.image` (Surface), `.rect` (Rect) |
| **Move in place** | `rect.move_ip(dx, dy)` |
| **Clamp to screen** | `rect.left = 0`, `rect.right = WIDTH`, etc. |
| **Group — create** | `pygame.sprite.Group(s1, s2, ...)` |
| **Group — update all** | `group.update()` → calls each sprite's `update()` |
| **Group — draw all** | `group.draw(surface)` → blits each `.image` at `.rect` |
| **Collision (yes/no)** | `spritecollideany(sprite, group)` |
| **Collision (list)** | `spritecollide(sprite, group, dokill)` |
| **Remove sprite** | `sprite.kill()` — removes from all groups |
| **Custom timer** | `pygame.time.set_timer(USEREVENT+1, ms)` |
