"""Procedural catalogs for baskets, balls, and backgrounds.

The game keeps these as data instead of requiring hundreds of binary image
files. Each entry has a stable id and can be selected by index later.
"""

from colorsys import hsv_to_rgb


def _color(hue, saturation=0.72, value=0.92):
    red, green, blue = hsv_to_rgb(hue % 1.0, saturation, value)
    return tuple(int(channel * 255) for channel in (red, green, blue))


BASKET_STYLES = (
    "classic", "sport", "carbon", "candy", "sunset",
    "mint", "royal", "electric", "sand", "mono",
)

BASKET_ASSETS = [
    {
        "id": f"basket_{index + 1:03d}",
        "style": BASKET_STYLES[index // 10],
        "color": _color(index / 100),
        "width": 120 + (index % 5) * 4,
        "height": 22 + (index % 3) * 2,
        "speed": 7.5 + (index % 6) * 0.4,
    }
    for index in range(100)
]


BALL_STYLES = (
    "ember", "aqua", "violet", "lime", "gold",
    "coral", "ice", "ruby", "plasma", "pearl",
)

BALL_ASSETS = [
    {
        "id": f"ball_{index + 1:03d}",
        "style": BALL_STYLES[index // 10],
        "color": _color((index * 0.071) + 0.02),
        "radius": 10 + (index % 6),
        "speed": 2.5 + (index % 8) * 0.35,
        "gravity": 0.014 + (index % 5) * 0.003,
        "bounce_multiplier": 1.08 + (index % 7) * 0.035,
        "break_speed": 1.8 + (index % 5) * 0.2,
    }
    for index in range(100)
]


BACKGROUND_ASSETS = [
    {"id": "black", "name": "Black", "kind": "solid", "color": (0, 0, 0)},
    {"id": "basketball_court", "name": "Basketball Court",
        "kind": "court", "color": (40, 25, 18), "accent": (205, 125, 55)},
    {"id": "neon_grid", "name": "Neon Grid", "kind": "grid",
        "color": (8, 12, 28), "accent": (30, 180, 220)},
    {"id": "sunset", "name": "Sunset", "kind": "gradient",
        "color": (65, 20, 45), "accent": (240, 115, 70)},
    {"id": "forest", "name": "Forest", "kind": "stripes",
        "color": (10, 35, 24), "accent": (55, 150, 85)},
    {"id": "ocean", "name": "Ocean", "kind": "gradient",
        "color": (5, 25, 55), "accent": (30, 140, 200)},
    {"id": "desert", "name": "Desert", "kind": "stripes",
        "color": (70, 40, 20), "accent": (210, 155, 75)},
    {"id": "arctic", "name": "Arctic", "kind": "grid",
        "color": (25, 50, 65), "accent": (160, 220, 235)},
    {"id": "volcano", "name": "Volcano", "kind": "gradient",
        "color": (55, 8, 5), "accent": (235, 75, 25)},
    {"id": "lavender", "name": "Lavender", "kind": "stripes",
        "color": (35, 20, 55), "accent": (165, 105, 220)},
    {"id": "industrial", "name": "Industrial", "kind": "grid",
        "color": (32, 35, 38), "accent": (150, 155, 160)},
    {"id": "paper", "name": "Paper", "kind": "stripes",
        "color": (48, 45, 38), "accent": (185, 175, 135)},
    {"id": "deep_space", "name": "Deep Space", "kind": "stars",
        "color": (4, 5, 18), "accent": (100, 120, 220)},
    {"id": "clouds", "name": "Clouds", "kind": "gradient",
        "color": (45, 55, 75), "accent": (170, 190, 215)},
    {"id": "cherry", "name": "Cherry", "kind": "stripes",
        "color": (55, 8, 25), "accent": (210, 55, 100)},
    {"id": "teal", "name": "Teal", "kind": "grid",
        "color": (5, 40, 42), "accent": (40, 190, 175)},
    {"id": "royal", "name": "Royal", "kind": "gradient",
        "color": (18, 15, 65), "accent": (90, 95, 220)},
    {"id": "copper", "name": "Copper", "kind": "stripes",
        "color": (55, 28, 18), "accent": (195, 105, 60)},
    {"id": "meadow", "name": "Meadow", "kind": "stripes",
        "color": (20, 50, 28), "accent": (125, 200, 80)},
    {"id": "monochrome", "name": "Monochrome", "kind": "grid",
        "color": (18, 18, 18), "accent": (125, 125, 125)},
]


assert len(BASKET_ASSETS) == 100
assert len(BALL_ASSETS) == 100
assert len(BACKGROUND_ASSETS) == 20
