"""Collision helpers for balls and the paddle."""


def is_caught(paddle_rect, obj):
    return (
        obj.is_contactable
        and obj.velocity_y > 0
        and paddle_rect.left <= obj.x <= paddle_rect.right
        and paddle_rect.top <= obj.y <= paddle_rect.bottom
    )
