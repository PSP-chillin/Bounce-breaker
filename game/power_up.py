"""Falling power-ups for Bounce Breaker."""

import pygame


POWER_UP_TYPES = ("wide", "slow", "life")
POWER_UP_COLORS = {
    "wide": (80, 190, 255),
    "slow": (180, 130, 255),
    "life": (255, 100, 130),
}
POWER_UP_LABELS = {"wide": "W", "slow": "S", "life": "+"}


class PowerUp:
    def __init__(self, x, y, power_type, speed=2):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.speed = speed
        self.size = 16

    def update(self):
        self.y += self.speed

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.size), int(self.y - self.size),
            self.size * 2, self.size * 2,
        )

    def is_past_bottom(self, height):
        return self.y - self.size > height

    @property
    def color(self):
        return POWER_UP_COLORS[self.power_type]

    @property
    def label(self):
        return POWER_UP_LABELS[self.power_type]
