"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (0, 0, 0)
COLOR_BASKET = (150, 110, 70)
COLOR_TEXT = (255, 255, 255)


def draw_background(surface, background):
    if not background:
        surface.fill(COLOR_BG)
        return

    surface.fill(background["color"])
    accent = background.get("accent", (80, 80, 80))
    kind = background.get("kind")
    if kind == "court":
        pygame.draw.line(surface, accent, (WIDTH // 2, 0),
                         (WIDTH // 2, HEIGHT), 2)
        pygame.draw.circle(surface, accent, (WIDTH // 2, HEIGHT // 2), 70, 2)
        pygame.draw.rect(surface, accent, (40, 90, 150, 320), 2)
        pygame.draw.rect(surface, accent, (WIDTH - 190, 90, 150, 320), 2)
    elif kind == "grid":
        for x in range(0, WIDTH, 35):
            pygame.draw.line(surface, accent, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 35):
            pygame.draw.line(surface, accent, (0, y), (WIDTH, y), 1)
    elif kind == "stripes":
        for y in range(0, HEIGHT, 32):
            pygame.draw.line(surface, accent, (0, y), (WIDTH, y), 2)
    elif kind == "gradient":
        for y in range(HEIGHT):
            blend = y / HEIGHT
            color = tuple(int(background["color"][i] * (1 - blend)
                              + accent[i] * blend) for i in range(3))
            pygame.draw.line(surface, color, (0, y), (WIDTH, y))
    elif kind == "stars":
        for x, y in ((80, 70), (210, 145), (350, 55), (510, 120),
                     (620, 75), (450, 260), (120, 330)):
            pygame.draw.circle(surface, accent, (x, y), 2)


def draw_scene(surface, basket, objects, cracked_objects=None,
               power_ups=None, particles=None, background=None):
    draw_background(surface, background)
    for obj in (*objects, *(cracked_objects or [])):
        center = (int(obj.x), int(obj.y))
        pygame.draw.circle(surface, obj.color, center, obj.radius)
        if obj.cracked:
            pygame.draw.line(
                surface, (20, 20, 20),
                (center[0] - obj.radius // 2, center[1] - obj.radius // 2),
                (center[0], center[1] - obj.radius // 5), 2,
            )
            pygame.draw.line(
                surface, (20, 20, 20),
                (center[0], center[1] - obj.radius // 5),
                (center[0] - obj.radius // 4, center[1] + obj.radius // 2), 2,
            )
            pygame.draw.line(
                surface, (20, 20, 20),
                (center[0], center[1] - obj.radius // 5),
                (center[0] + obj.radius // 2, center[1] + obj.radius // 3), 2,
            )

    for power_up in power_ups or []:
        rect = power_up.get_rect()
        pygame.draw.rect(surface, power_up.color, rect, border_radius=5)
        pygame.draw.rect(surface, COLOR_TEXT, rect, 2, border_radius=5)
        label = pygame.font.Font(None, 22).render(
            power_up.label, True, COLOR_TEXT)
        surface.blit(label, label.get_rect(center=rect.center))

    for particle in particles or []:
        pygame.draw.circle(
            surface, particle.color,
            (int(particle.x), int(particle.y)), particle.radius)

    pygame.draw.rect(surface, basket.color, basket.get_rect(), border_radius=6)
    pygame.draw.rect(
        surface, COLOR_TEXT, (0, 0, WIDTH - 1, HEIGHT - 1), 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() //
                         2, surface.get_height() // 2))
    surface.blit(surf, rect)
