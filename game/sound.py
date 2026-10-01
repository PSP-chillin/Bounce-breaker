"""Optional generated sound effects with no external audio files."""

import array
import math
import pygame


class SoundEffects:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.sounds = {
                "bounce": self._tone(520, 0.06),
                "powerup": self._tone(760, 0.12),
                "miss": self._tone(180, 0.14),
            }
            self.enabled = True
        except pygame.error:
            pass

    @staticmethod
    def _tone(frequency, duration):
        sample_rate = 44100
        samples = int(sample_rate * duration)
        data = array.array(
            "h",
            (
                int(12000 * math.sin(2 * math.pi * frequency * i / sample_rate))
                for i in range(samples)
            ),
        )
        return pygame.mixer.Sound(buffer=data.tobytes())

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()
