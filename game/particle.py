"""Small visual particles used for ball and power-up feedback."""


class Particle:
    def __init__(self, x, y, velocity_x, velocity_y, color, lifetime=24):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.08
        self.lifetime -= 1

    @property
    def alive(self):
        return self.lifetime > 0

    @property
    def radius(self):
        return max(1, int(3 * self.lifetime / self.max_lifetime))
