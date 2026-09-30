"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width * 1.33
        self.height = height
        self.speed = speed * 1.5
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
