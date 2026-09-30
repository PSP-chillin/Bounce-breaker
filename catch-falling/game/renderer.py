"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(surface, obj.color,
                           (int(obj.x), int(obj.y)), obj.radius)

    rect = basket.get_rect()
    pygame.draw.rect(surface, COLOR_BASKET, rect, border_radius=6)

    side_thickness = basket.width * 0.5
    left_start = int(rect.left)
    right_start = int(rect.right)
    vertical_height = int(basket.width * 2)
    bottom_y = int(rect.bottom)
    top_y = int(bottom_y - vertical_height)

    pygame.draw.line(surface, COLOR_BASKET, (left_start, bottom_y),
                     (left_start, top_y), int(side_thickness))
    pygame.draw.line(surface, COLOR_BASKET, (right_start, bottom_y),
                     (right_start, top_y), int(side_thickness))


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() //
                         2, surface.get_height() // 2))
    surface.blit(surf, rect)
