"""A ball that can bounce on the basket before cracking."""


class FallingObject:
    def __init__(self, x, y, radius=14, speed=3, color=(230, 140, 60)):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.velocity_y = speed
        self.gravity = 0.02
        self.bounce_count = 0
        self.cracked = False

    @property
    def is_contactable(self):
        return not self.cracked

    def bounce(self):
        self.bounce_count += 1
        if self.bounce_count >= 3:
            self.crack()
            return

        self.velocity_y = -max(3.5, self.speed * 1.2)

    def crack(self):
        self.cracked = True
        self.velocity_y = max(2.0, self.speed)
        self.color = (130, 130, 130)

    def update(self):
        if self.cracked:
            self.y += self.velocity_y
            self.velocity_y += self.gravity
            return

        self.velocity_y += self.gravity
        self.y += self.velocity_y

    def is_past_bottom(self, height):
        return self.y - self.radius > height
