# Code Update

This file contains copies of the current game source code. The original source files remain unchanged.

## `catch-falling/main.py`

```python
"""
Catch the Falling Objects (Lab Starter)

Run with:  python3 main.py

Controls: Left/Right arrows to move the basket.
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Catch the Falling Objects")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    engine = GameEngine()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                engine.handle_keydown(event.key)

        keys = pygame.key.get_pressed()
        engine.handle_input(keys)
        engine.update()
        engine.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
```

## `catch-falling/game/basket.py`

```python
"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.boosted_frames = 0
        self.normal_speed = self.speed
        self.boost_speed = self.speed * 1.8

    @property
    def current_speed(self):
        return self.boost_speed if self.boosted_frames > 0 else self.normal_speed

    def activate_boost(self, duration_frames=180):
        self.boosted_frames = max(self.boosted_frames, duration_frames)

    def update_boost(self):
        if self.boosted_frames > 0:
            self.boosted_frames -= 1

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
```

## `catch-falling/game/collision.py`

```python
"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    return (
        basket_rect.left <= obj.x <= basket_rect.right
        and basket_rect.top <= obj.y <= basket_rect.bottom
    )
```

## `catch-falling/game/falling_object.py`

```python
"""
FallingObject: a simple object that falls straight down.
"""


class FallingObject:
    def __init__(self, x, y, radius=14, speed=3, color=(230, 140, 60)):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height
```

## `catch-falling/game/game_engine.py`

```python
"""
GameEngine: owns the basket and all falling objects.

Starter version: basket movement and spawning both work at a basic
level (Tasks 2 and 3 ask you to improve them), there's no speed boost
yet (Task 4 builds it from scratch), and catch detection has two
known bugs (see game/collision.py and the catch-checking loop below)
that Task 1 asks you to fix.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 50
MAX_MISSES = 5
MAX_OBJECTS_ON_SCREEN = 8


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _choose_spawn_x(self):
        margin = 30
        min_x = margin
        max_x = WIDTH - margin

        if not self.objects:
            return random.randint(min_x, max_x)

        for _ in range(200):
            candidate = random.randint(min_x, max_x)
            if all(abs(candidate - obj.x) > 60 for obj in self.objects):
                return candidate

        return random.randint(min_x, max_x)

    def _spawn_object(self):
        if len(self.objects) >= MAX_OBJECTS_ON_SCREEN:
            return

        x = self._choose_spawn_x()
        speed = random.randint(3, 5)
        self.objects.append(FallingObject(x=x, y=-14, speed=speed))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        move_speed = self.basket.current_speed

        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= move_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += move_speed

        half_width = self.basket.width / 2
        self.basket.x = max(half_width, min(WIDTH - half_width, self.basket.x))

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            self.basket.activate_boost()
        if self.game_over and key == pygame.K_r:
            self.__init__()

    def update(self):
        if self.game_over:
            return

        self.basket.update_boost()
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_object()
            if len(self.objects) < MAX_OBJECTS_ON_SCREEN:
                self.frames_until_spawn = random.randint(20, 60)
            else:
                self.frames_until_spawn = 10

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()
        caught_objects = [
            obj for obj in self.objects if is_caught(basket_rect, obj)
        ]
        self.objects = [
            obj for obj in self.objects if not is_caught(basket_rect, obj)
        ]
        self.score += len(caught_objects)

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [
                o for o in self.objects if not o.is_past_bottom(HEIGHT)
            ]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(
            surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))

        if self.basket.boosted_frames > 0:
            renderer.draw_text(surface, font, "BOOST!",
                               (10, 62), (80, 255, 180))
        else:
            renderer.draw_text(surface, font, "Normal speed",
                               (10, 62), (220, 220, 220))

        if self.game_over:
            renderer.draw_banner(
                surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")
```

## `catch-falling/game/renderer.py`

```python
"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(surface, obj.color,
                           (int(obj.x), int(obj.y)), obj.radius)

    pygame.draw.rect(surface, COLOR_BASKET, basket.get_rect(), border_radius=6)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() //
                         2, surface.get_height() // 2))
    surface.blit(surf, rect)
```
