"""
Bounce Breaker

Run with:  python3 main.py

Controls: Left/Right arrows to move the basket, P to pause.
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE
from setting import SettingsPanel


def create_display(fullscreen):
    flags = pygame.SCALED
    if fullscreen:
        flags |= pygame.FULLSCREEN
    return pygame.display.set_mode(WINDOW_SIZE, flags)


def main():
    pygame.init()
    fullscreen = True
    screen = create_display(fullscreen)
    pygame.display.set_caption("Bounce Breaker")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    title_font = pygame.font.SysFont("consolas", 38, bold=True)

    engine = GameEngine()
    settings = SettingsPanel()
    game_started = False
    settings_open = False
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if settings_open:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    settings_open = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    screen = create_display(fullscreen)
                else:
                    action = settings.handle_event(event)
                    if action == "quit":
                        running = False
                    elif action == "close":
                        settings_open = False
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    screen = create_display(fullscreen)
                elif event.key == pygame.K_p:
                    settings_open = True
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and (
                        not game_started or engine.game_over):
                    engine = GameEngine()
                    game_started = True
                elif game_started and not engine.game_over:
                    engine.handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if settings.settings_button_hit(event.pos):
                    settings_open = True
                elif settings.play_button_hit(event.pos) and (
                        not game_started or engine.game_over):
                    engine = GameEngine()
                    game_started = True

        if game_started and not settings_open and not engine.game_over:
            keys = pygame.key.get_pressed()
            engine.handle_input(keys)
            engine.update()

        if not game_started or engine.game_over:
            settings.draw_play_screen(
                screen, title_font, font, mouse_pos, engine.game_over,
                engine.score)
        else:
            engine.draw(screen, font)
            settings.draw_settings_button(screen, mouse_pos)

        if settings_open:
            settings.draw(screen, font, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
