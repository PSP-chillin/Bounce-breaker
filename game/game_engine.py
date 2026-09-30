"""
GameEngine: owns the basket and all falling objects.

The engine handles basket movement, object spawning, speed changes, and
collision detection for Bounce Breaker.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 50
MAX_MISSES = 5
MAX_OBJECTS_ON_SCREEN = 3


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.cracked_objects = []
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
        for obj in self.cracked_objects:
            obj.update()

        basket_rect = self.basket.get_rect()
        cracked_this_frame = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                obj.bounce()
                self.score += 1
                if obj.cracked:
                    cracked_this_frame.append(obj)

        if cracked_this_frame:
            self.objects = [
                obj for obj in self.objects if obj not in cracked_this_frame
            ]
            self.cracked_objects.extend(cracked_this_frame)
            for _ in cracked_this_frame:
                self._spawn_object()

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [
                o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            missed_contactable = [o for o in missed if o.is_contactable]
            self.misses += len(missed_contactable)
            if self.misses >= MAX_MISSES:
                self.game_over = True

            for _ in missed:
                self._spawn_object()

        self.cracked_objects = [
            obj for obj in self.cracked_objects
            if not obj.is_past_bottom(HEIGHT)
        ]

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(
            surface, self.basket, self.objects, self.cracked_objects)
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
