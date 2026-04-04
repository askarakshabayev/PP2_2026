# Lecture 11: Pygame I

## Plan
- Virtual Environments
- Getting Started (intro/)
- Drawing Shapes
- Paint App (paint/)
- Fonts (fonts/)
- Images (images/)
- Sounds (sounds/)

---

## 0. Virtual Environments

When you run `pip install` without a virtual environment, packages are installed **globally** — shared across every Python project on your machine. This causes problems:

- **Version conflicts** — Project A needs `pygame==2.1`, Project B needs `pygame==2.6`. They can't coexist globally.
- **Polluted system Python** — Uninstalling or upgrading one package can break unrelated projects.
- **Not reproducible** — A teammate cloning your repo won't know which packages to install or at what version.

A **virtual environment** is an isolated directory with its own Python interpreter and packages.

```bash
# 1. Create
python3 -m venv name_of_venv

# 2. Activate
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install
pip install pygame

# 4. Save dependencies
pip freeze > requirements.txt

# 5. Deactivate
deactivate
```

Teammate setup:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`.gitignore`:
```
venv/
__pycache__/
*.pyc
```

---

## 1. Getting Started (`intro/`)

### 01.py — Minimal skeleton

```python
import pygame

pygame.init()  # initializes all the pygame sub-modules

screen = pygame.display.set_mode((800, 480))  # creating a game window

while True:  # game loop
    pass    # use ctrl+c in the terminal to stop it
```

- `pygame.init()` — starts all pygame sub-modules
- `pygame.display.set_mode((w, h))` — creates the window, returns a **Surface**
- The game loop runs forever; Ctrl+C to stop

---

### 02.py — Event loop + proper exit

```python
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 480))

running = True
while running:
    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
```

- `pygame.event.get()` — drains the event queue; **must be called every frame** or the window freezes
- `pygame.QUIT` — fired when the user clicks the ✕ button
- `pygame.quit()` — shuts down all pygame modules; good practice to call at the end

> **events.py** — you can `print(event)` to see every event object pygame generates (mouse moves, key presses, etc.)

---

### 03.py — Colors, `screen.fill()`, `display.flip()`, toggling on Space

```python
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 480))

COLOR_RED  = (255, 0, 0)   # RGB: each component 0–255 (8 bits)
COLOR_BLUE = (0, 0, 255)

running = True
is_red = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_red = not is_red   # toggle True ↔ False

    if is_red:
        screen.fill(COLOR_RED)
    else:
        screen.fill(COLOR_BLUE)

    pygame.display.flip()  # push the frame to the screen

pygame.quit()
```

- Colors are `(R, G, B)` tuples; each value is 0–255
- `screen.fill(color)` — paints the entire surface; call every frame to erase the previous frame
- `pygame.display.flip()` — swaps the back buffer to the screen (double buffering)
- `pygame.KEYDOWN` — fired once per key press; `event.key` identifies which key

---

### 04.py — Drawing a circle

```python
# inside the game loop, after screen.fill():
pygame.draw.circle(screen, COLOR_RED, (100, 100), 40)
# draw.circle(surface, color, center, radius)
```

Order matters: draw **after** `screen.fill()`, **before** `pygame.display.flip()`.

---

### 05.py — Circle contrasts with background

```python
if is_red:
    screen.fill(COLOR_RED)
    pygame.draw.circle(screen, COLOR_BLUE, (circle_x, circle_y), 40)
else:
    screen.fill(COLOR_BLUE)
    pygame.draw.circle(screen, COLOR_RED, (circle_x, circle_y), 40)
```

---

### 06.py & 07.py — Moving with `KEYDOWN` (the problem)

```python
# 06.py — moves 1 px per press: barely visible
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_UP:    circle_y -= 1
    if event.key == pygame.K_DOWN:  circle_y += 1

# 07.py — bigger step, but still choppy: holding the key doesn't keep moving
movement_speed = 10
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_UP:    circle_y -= movement_speed
```

**Problem:** `KEYDOWN` fires only **once** per press. Holding a key does not repeat movement.

---

### 08.py — Smooth movement: boolean flags + `KEYUP`

```python
up_pressed = down_pressed = right_pressed = left_pressed = False

for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:    up_pressed    = True
        if event.key == pygame.K_DOWN:  down_pressed  = True
        if event.key == pygame.K_RIGHT: right_pressed = True
        if event.key == pygame.K_LEFT:  left_pressed  = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:    up_pressed    = False
        if event.key == pygame.K_DOWN:  down_pressed  = False
        if event.key == pygame.K_RIGHT: right_pressed = False
        if event.key == pygame.K_LEFT:  left_pressed  = False

# Outside the event loop — runs every frame:
if up_pressed:    circle_y -= movement_speed
if down_pressed:  circle_y += movement_speed
if right_pressed: circle_x += movement_speed
if left_pressed:  circle_x -= movement_speed
```

Movement code is **outside** the event loop → runs every frame while the key is held.

---

### 09.py — FPS clock

```python
clock = pygame.time.Clock()
FPS = 60

while running:
    # ... event handling, movement, drawing ...
    pygame.display.flip()
    clock.tick(FPS)  # wait until this frame took at least 1000/60 ms
```

Without `clock.tick()` the loop runs as fast as the CPU allows — movement speed would differ between computers.

---

### 10.py — Simpler: `pygame.key.get_pressed()`

```python
# Approach 2: one call returns a snapshot of ALL keys right now
pressed_keys = pygame.key.get_pressed()
if pressed_keys[pygame.K_UP]:    circle_y -= movement_speed
if pressed_keys[pygame.K_DOWN]:  circle_y += movement_speed
if pressed_keys[pygame.K_RIGHT]: circle_x += movement_speed
if pressed_keys[pygame.K_LEFT]:  circle_x -= movement_speed
```

No need for manual booleans or `KEYUP` — pygame tracks the state for us.

| | `KEYDOWN` event | `key.get_pressed()` |
|---|---|---|
| Fires | Once per press | Every frame (while held) |
| Use for | Toggle, shoot, jump | Smooth continuous movement |

---

### 11.py — Boundary clamping

```python
RADIUS = 40

# After movement:
if circle_x - RADIUS < 0:        circle_x = RADIUS
if circle_x + RADIUS > WIDTH:    circle_x = WIDTH - RADIUS
if circle_y - RADIUS < 0:        circle_y = RADIUS
if circle_y + RADIUS > HEIGHT:   circle_y = HEIGHT - RADIUS
```

Prevents the circle from going off-screen by clamping its center so the edge never leaves the window.

---

### 12.py — All drawing primitives

```python
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

red    = (255, 0, 0)
green  = (0, 255, 0)
blue   = (0, 0, 255)
yellow = (255, 255, 0)
white  = (255, 255, 255)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # Rectangle: (surface, color, (x, y, width, height))
    pygame.draw.rect(screen, red, (50, 50, 200, 100))

    # Rectangle with border only (last arg = border thickness)
    pygame.draw.rect(screen, green, (300, 50, 200, 100), 3)

    # Circle: (surface, color, center, radius)
    pygame.draw.circle(screen, blue, (150, 300), 60)

    # Ellipse: (surface, color, bounding_rect)
    pygame.draw.ellipse(screen, yellow, (300, 250, 200, 100))

    # Line: (surface, color, start_pos, end_pos, width)
    pygame.draw.line(screen, white, (550, 50), (750, 150), 3)

    # Polygon: (surface, color, list_of_points)
    pygame.draw.polygon(screen, green, [(600, 300), (700, 200), (750, 350)])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

Summary:

| Function | Signature |
|---|---|
| `draw.rect` | `(surface, color, (x, y, w, h))` · last arg = border thickness, 0 = filled |
| `draw.circle` | `(surface, color, (cx, cy), radius)` |
| `draw.ellipse` | `(surface, color, (x, y, w, h))` |
| `draw.line` | `(surface, color, start, end, width)` |
| `draw.polygon` | `(surface, color, [(x,y), ...])` |

---

## 2. Paint App (`paint/paint.py`)

Bare-bones paint app — draw on screen by holding the mouse button:

```python
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

screen.fill("white")

color   = (0, 0, 0)
radius  = 5
drawing = False

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  color = (255, 0, 0)
            if event.key == pygame.K_g:  color = (0, 255, 0)
            if event.key == pygame.K_b:  color = (0, 0, 255)
            if event.key == pygame.K_k:  color = (0, 0, 0)
            if event.key == pygame.K_e:  color = (255, 255, 255)  # eraser
            if event.key == pygame.K_c:  screen.fill("white")     # clear
            if event.key == pygame.K_UP:   radius = min(radius + 2, 50)
            if event.key == pygame.K_DOWN: radius = max(radius - 2, 1)

    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, color, mouse_pos, radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

Controls: **R/G/B/K** — color · **E** — eraser · **C** — clear · **↑/↓** — brush size

Key ideas:
- `screen.fill()` is called **once before the loop** to set the white canvas — not inside the loop (that would erase everything)
- `pygame.mouse.get_pos()` — returns `(x, y)` of the cursor right now

---

## 3. Fonts (`fonts/01.py`)

```python
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock  = pygame.time.Clock()

# Create a font object: SysFont(name, size)
font = pygame.font.SysFont("comicsansms", 72)

# Render returns a Surface — do this ONCE, not inside the loop
text = font.render("Hello KBTU", True, (0, 0, 255))

# Center it
x = 400 - text.get_width()  // 2
y = 300 - text.get_height() // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]: x += 1
    if keys[pygame.K_LEFT]:  x -= 1
    if keys[pygame.K_DOWN]:  y += 1
    if keys[pygame.K_UP]:    y -= 1

    screen.fill((0, 0, 0))
    screen.blit(text, (x, y))
    pygame.display.flip()
    clock.tick(60)
```

- `pygame.font.SysFont(name, size)` — uses a system font
- `font.render(text, antialias, color)` — returns a **Surface**; render once and reuse
- `surface.blit(other_surface, (x, y))` — draws one surface onto another
- `text.get_width()` / `text.get_height()` — size of the rendered text surface

Other font sources:
```python
font = pygame.font.Font(None, 48)               # built-in pygame default
font = pygame.font.Font("fonts/Roboto.ttf", 32) # custom .ttf file
```

---

## 4. Images (`images/`)

### 01.py — Load and move an image

```python
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock  = pygame.time.Clock()

# Load image ONCE, before the loop
image = pygame.image.load("ball.png")

x, y = 30, 30

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]: x += 1
    if keys[pygame.K_LEFT]:  x -= 1
    if keys[pygame.K_DOWN]:  y += 1
    if keys[pygame.K_UP]:    y -= 1

    screen.fill((255, 255, 255))
    screen.blit(image, (x, y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

- `pygame.image.load(path)` — loads an image from disk; call **once before the loop**
- `screen.blit(image, (x, y))` — draws the image at position `(x, y)`

### 02.py — Rotating an image

```python
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()

image = pygame.image.load("car.png")
angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  angle += 3
    if keys[pygame.K_RIGHT]: angle -= 3

    # rotate() returns a NEW surface — always rotate the ORIGINAL,
    # not an already-rotated surface, to avoid quality loss
    rotated = pygame.transform.rotate(image, angle)

    # After rotation the surface size changes — recalculate center position
    rect = rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill("white")
    screen.blit(rotated, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

- `pygame.transform.rotate(surface, angle)` — returns a **new** rotated surface
- Always rotate the **original** image, not the already-rotated one → no quality loss
- `surface.get_rect(center=(...))` — gets a `Rect` positioned so the center is at the given point

---

## 5. Sounds (`sounds/`)

### 01.py — Play a sound effect once

```python
import pygame

pygame.init()

sound = pygame.mixer.Sound("bonk.mp3")
sound.play()

input()  # keep the script alive until Enter
```

`pygame.mixer.Sound` — for short one-shot effects (loads the whole file into memory).

---

### 02.py — Sound library + play on key press

```python
import pygame
import os

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock  = pygame.time.Clock()

# Cache: maps file path → Sound object (load each file only once)
_sound_library = {}

def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        # os.sep = '/' on mac/linux, '\\' on windows
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:   # fires ONCE per press → sound plays once
            if event.key == pygame.K_b:
                play_sound("bonk.mp3")

    screen.fill("white")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

Use `KEYDOWN` (not `get_pressed`) so the sound triggers once per press, not every frame.

---

### 03.py — Background music with `mixer.music`

```python
import pygame

pygame.init()

screen = pygame.display.set_mode((400, 200))

# mixer.music streams from disk — suitable for long background tracks
# Only one music track can play at a time
pygame.mixer.music.load("bonk.mp3")
pygame.mixer.music.play(-1)   # -1 = loop forever, 0 = play once

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_s:
                pygame.mixer.music.stop()
            if event.key == pygame.K_r:
                pygame.mixer.music.play(-1)

    screen.fill("black")
    font = pygame.font.SysFont("Verdana", 20)
    screen.blit(font.render("P = pause/unpause, S = stop, R = restart", True, "white"), (10, 80))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

| | `mixer.Sound` | `mixer.music` |
|---|---|---|
| Use for | Short effects (beep, bonk) | Long background music |
| Loading | Whole file into memory | Streamed from disk |
| Simultaneous | Multiple at once | Only one track at a time |
| Key functions | `.play()`, `.stop()` | `.load()`, `.play()`, `.pause()`, `.unpause()`, `.stop()` |

---

## Conclusion

| Topic | Key APIs |
|---|---|
| **Window & loop** | `pygame.init()`, `display.set_mode()`, `event.get()`, `display.flip()`, `clock.tick(fps)` |
| **Drawing** | `draw.rect`, `draw.circle`, `draw.ellipse`, `draw.line`, `draw.polygon` |
| **Input (one-shot)** | `KEYDOWN` / `KEYUP` events |
| **Input (continuous)** | `key.get_pressed()` |
| **Mouse** | `MOUSEBUTTONDOWN/UP`, `mouse.get_pos()` |
| **Text** | `font.SysFont()`, `font.render()` → Surface → `blit()` |
| **Images** | `image.load()`, `transform.rotate()`, `blit()` |
| **Sound effects** | `mixer.Sound(path).play()` |
| **Music** | `mixer.music.load/play/pause/stop` |
