"""A ball that can bounce on the basket before cracking."""


class FallingObject:
    def __init__(self, x, y, radius=14, speed=3, color=(230, 140, 60),
                 velocity_x=0.0, gravity=0.02, bounce_multiplier=1.2,
                 break_speed=2.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = speed
        self.speed_factor = 1.0
        self.gravity = gravity
        self.bounce_multiplier = bounce_multiplier
        self.break_speed = break_speed
        self.bounce_count = 0
        self.cracked = False

    @property
    def is_contactable(self):
        return not self.cracked

    def bounce(self, break_direction=1, horizontal_velocity=None):
        self.bounce_count += 1
        if self.bounce_count >= 3:
            self.crack(break_direction)
            return

        self.velocity_y = -max(3.5, self.speed * self.bounce_multiplier)
        if horizontal_velocity is not None:
            self.velocity_x = horizontal_velocity

    def crack(self, direction=1):
        self.cracked = True
        break_speed = max(self.break_speed, self.speed * 0.6)
        self.velocity_x = abs(break_speed) * direction
        self.velocity_y = break_speed

    def update(self):
        if self.cracked:
            self.x += self.velocity_x * self.speed_factor
            self.y += self.velocity_y * self.speed_factor
            return

        self.velocity_y += self.gravity * self.speed_factor
        self.x += self.velocity_x * self.speed_factor
        self.y += self.velocity_y * self.speed_factor

    def handle_walls(self, width, height):
        if self.cracked:
            return

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.velocity_x = abs(self.velocity_x)
        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.velocity_x = -abs(self.velocity_x)

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.velocity_y = abs(self.velocity_y)

    def is_past_bottom(self, height):
        return self.y - self.radius > height
