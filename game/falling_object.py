"""A ball that can bounce on the basket before cracking."""


class FallingObject:
    def __init__(self, x, y, radius=14, speed=3, color=(230, 140, 60)):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.velocity_x = 0.0
        self.velocity_y = speed
        self.gravity = 0.02
        self.bounce_count = 0
        self.cracked = False

    @property
    def is_contactable(self):
        return not self.cracked

    def bounce(self, break_direction=1):
        self.bounce_count += 1
        if self.bounce_count >= 3:
            self.crack(break_direction)
            return

        self.velocity_y = -max(3.5, self.speed * 1.2)

    def crack(self, direction=1):
        self.cracked = True
        break_speed = max(2.0, self.speed)
        self.velocity_x = abs(break_speed) * direction
        self.velocity_y = break_speed

    def update(self):
        if self.cracked:
            self.x += self.velocity_x
            self.y += self.velocity_y
            return

        self.velocity_y += self.gravity
        self.y += self.velocity_y

    def is_past_bottom(self, height):
        return self.y - self.radius > height
