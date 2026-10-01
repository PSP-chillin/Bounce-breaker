"""
Basket: the player-controlled bar at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=120, height=24, speed=7.5,
                 color=(150, 110, 70)):
        self.x = x
        self.y = y
        self.width = float(width)
        self.base_width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.boosted_frames = 0
        self.wide_frames = 0
        self.target_width = self.width
        self.normal_speed = self.speed
        self.boost_speed = self.speed * 1.8

    @property
    def current_speed(self):
        return self.boost_speed if self.boosted_frames > 0 else self.normal_speed

    def activate_boost(self, duration_frames=180):
        self.boosted_frames = max(self.boosted_frames, duration_frames)

    def activate_wide(self, duration_frames=360):
        self.wide_frames = max(self.wide_frames, duration_frames)
        self.target_width = self.base_width * 1.5

    def update_boost(self):
        if self.boosted_frames > 0:
            self.boosted_frames -= 1

    def update_effects(self):
        self.update_boost()
        if self.wide_frames > 0:
            self.wide_frames -= 1
        self.target_width = (
            self.base_width * 1.5
            if self.wide_frames > 0 else self.base_width
        )
        width_delta = self.target_width - self.width
        if width_delta:
            self.width += max(-2.0, min(2.0, width_delta))

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
