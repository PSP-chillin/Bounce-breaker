"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (0, 0, 0)
COLOR_BASKET = (150, 110, 70)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, basket, objects, cracked_objects=None):
    surface.fill(COLOR_BG)
    for obj in (*objects, *(cracked_objects or [])):
        center = (int(obj.x), int(obj.y))
        pygame.draw.circle(surface, obj.color, center, obj.radius)
        if obj.cracked:
            pygame.draw.line(
                surface, (245, 245, 245),
                (center[0] - obj.radius // 2, center[1] - obj.radius // 2),
                (center[0] + obj.radius // 3, center[1]), 2,
            )
            pygame.draw.line(
                surface, (245, 245, 245),
                (center[0] + obj.radius // 3, center[1]),
                (center[0] - obj.radius // 3, center[1] + obj.radius // 2), 2,
            )

    pygame.draw.rect(surface, COLOR_BASKET, basket.get_rect(), border_radius=6)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() //
                         2, surface.get_height() // 2))
    surface.blit(surf, rect)
