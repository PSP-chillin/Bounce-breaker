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
from game.particle import Particle
from game.power_up import POWER_UP_TYPES, PowerUp
from game.renderer import WIDTH, HEIGHT
from game.sound import SoundEffects
from assets.catalog import BALL_ASSETS, BACKGROUND_ASSETS, BASKET_ASSETS

SPAWN_INTERVAL_FRAMES = 50
MAX_LIVES = 5
MAX_OBJECTS_ON_SCREEN = 2
POWER_UP_DROP_CHANCE = 0.15


class GameEngine:
    def __init__(self, background_index=0):
        basket_asset = BASKET_ASSETS[0]
        self.basket = Basket(
            x=WIDTH / 2, y=HEIGHT - 30,
            width=basket_asset["width"], height=basket_asset["height"],
            speed=basket_asset["speed"], color=basket_asset["color"],
        )
        self.background = BACKGROUND_ASSETS[background_index % len(
            BACKGROUND_ASSETS)]
        self.objects = []
        self.cracked_objects = []
        self.power_ups = []
        self.particles = []
        self.sounds = SoundEffects()
        self.frames_until_spawn = 0
        self.score = 0
        self.combo = 0
        self.misses = 0
        self.lives = MAX_LIVES
        self.slow_frames = 0
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
        asset = random.choice(BALL_ASSETS)
        self.objects.append(FallingObject(
            x=x, y=-asset["radius"], radius=asset["radius"],
            speed=asset["speed"], color=asset["color"],
            gravity=asset["gravity"],
            bounce_multiplier=asset["bounce_multiplier"],
            break_speed=asset["break_speed"],
        ))
        if self.slow_frames > 0:
            self.objects[-1].speed_factor = 0.65
        if len(self.power_ups) < 2 and random.random() < POWER_UP_DROP_CHANCE:
            power_type = random.choice(POWER_UP_TYPES)
            self.power_ups.append(PowerUp(x=x, y=-14, power_type=power_type))

    def _add_particles(self, x, y, color, count=8):
        for _ in range(count):
            self.particles.append(Particle(
                x, y, random.uniform(-2.5, 2.5),
                random.uniform(-2.5, 0.5), color,
            ))

    def _activate_power_up(self, power_up):
        if power_up.power_type == "wide":
            self.basket.activate_wide()
        elif power_up.power_type == "slow":
            self.slow_frames = max(self.slow_frames, 360)
            for obj in self.objects:
                obj.speed_factor = 0.65
        elif power_up.power_type == "life":
            self.lives = min(MAX_LIVES, self.lives + 1)
        self.sounds.play("powerup")
        self._add_particles(power_up.x, power_up.y, power_up.color, 12)

    def handle_input(self, keys_pressed, keybinds=None):
        if self.game_over:
            return

        keybinds = keybinds or {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
        }
        move_speed = self.basket.current_speed

        if keys_pressed[keybinds.get("left", pygame.K_LEFT)]:
            self.basket.x -= move_speed
        if keys_pressed[keybinds.get("right", pygame.K_RIGHT)]:
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

        self.basket.update_effects()
        if self.slow_frames > 0:
            self.slow_frames -= 1
            if self.slow_frames == 0:
                for obj in self.objects:
                    obj.speed_factor = 1.0
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_object()
            if len(self.objects) < MAX_OBJECTS_ON_SCREEN:
                self.frames_until_spawn = random.randint(20, 60)
            else:
                self.frames_until_spawn = 10

        for obj in self.objects:
            obj.update()
            obj.handle_walls(WIDTH, HEIGHT)
        for obj in self.cracked_objects:
            obj.update()
        for power_up in self.power_ups:
            power_up.update()
        for particle in self.particles:
            particle.update()
        self.particles = [
            particle for particle in self.particles if particle.alive]

        basket_rect = self.basket.get_rect()
        caught_power_ups = [
            power_up for power_up in self.power_ups
            if basket_rect.colliderect(power_up.get_rect())
        ]
        for power_up in caught_power_ups:
            self._activate_power_up(power_up)
        self.power_ups = [
            power_up for power_up in self.power_ups
            if power_up not in caught_power_ups
            and not power_up.is_past_bottom(HEIGHT)
        ]

        cracked_this_frame = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                hit_offset = (
                    (obj.x - basket_rect.centerx)
                    / (basket_rect.width / 2)
                )
                hit_offset = max(-1.0, min(1.0, hit_offset))
                horizontal_velocity = hit_offset * max(3.0, obj.speed * 1.5)
                break_direction = -1 if horizontal_velocity < 0 else 1
                obj.bounce(
                    break_direction=break_direction,
                    horizontal_velocity=horizontal_velocity,
                )
                self.combo += 1
                self.score += self.combo
                self.sounds.play("bounce")
                self._add_particles(obj.x, obj.y, obj.color)
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
            if missed_contactable:
                # Several balls can cross the boundary in one frame; treat
                # that as one miss event so one frame cannot drain several lives.
                self.misses += 1
                self.lives = max(0, MAX_LIVES - self.misses)
                self.combo = 0
                self.sounds.play("miss")
                if self.lives <= 0:
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
            surface, self.basket, self.objects, self.cracked_objects,
            self.power_ups, self.particles, self.background)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(
            surface, font, f"Lives: {self.lives}/{MAX_LIVES}", (10, 36))
        renderer.draw_text(
            surface, font, f"Combo: x{self.combo}", (10, 62))

        if self.basket.boosted_frames > 0:
            renderer.draw_text(surface, font, "BOOST!",
                               (10, 88), (80, 255, 180))
        else:
            renderer.draw_text(surface, font, "Normal speed",
                               (10, 88), (220, 220, 220))

        if self.basket.wide_frames > 0:
            renderer.draw_text(surface, font, "WIDE BAR",
                               (10, 114), (80, 190, 255))
        if self.slow_frames > 0:
            renderer.draw_text(surface, font, "SLOW BALL",
                               (10, 140), (190, 140, 255))

        if self.game_over:
            renderer.draw_banner(
                surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")
