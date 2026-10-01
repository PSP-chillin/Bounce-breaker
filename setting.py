"""Settings and menu UI for Bounce Breaker."""

import pygame


PANEL_RECT = pygame.Rect(110, 60, 480, 380)
SETTINGS_BUTTON_RECT = pygame.Rect(650, 18, 32, 32)
PLAY_BUTTON_RECT = pygame.Rect(260, 330, 180, 54)
CLOSE_BUTTON_RECT = pygame.Rect(545, 76, 28, 28)

TAB_NAMES = ("Video", "Audio", "Keybinds", "Quit")
TAB_RECTS = {
    name: pygame.Rect(125, 115 + index * 62, 120, 48)
    for index, name in enumerate(TAB_NAMES)
}
KEYBIND_ACTIONS = ("up", "down", "left", "right")
KEYBIND_LABELS = {
    "up": "Move up / select previous",
    "down": "Move down / select next",
    "left": "Move bar left",
    "right": "Move bar right",
}

COLOR_PANEL = (35, 35, 35)
COLOR_SIDEBAR = (24, 24, 24)
COLOR_BUTTON = (65, 95, 125)
COLOR_BUTTON_HOVER = (85, 120, 155)
COLOR_TEXT = (240, 240, 240)
COLOR_MUTED = (170, 170, 170)
COLOR_CRACK = (20, 20, 20)


class SettingsPanel:
    """Draw and handle the settings overlay without changing game state."""

    def __init__(self):
        self.active_tab = "Video"
        self.selected_tab = "Video"
        self.keybinds = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
        }
        self.rebinding_action = None

    @staticmethod
    def draw_button(surface, font, rect, label, mouse_pos=None):
        hovered = mouse_pos is not None and rect.collidepoint(mouse_pos)
        color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, rect, border_radius=6)
        pygame.draw.rect(surface, (170, 190, 210), rect, 2, border_radius=6)
        text = font.render(label, True, COLOR_TEXT)
        surface.blit(text, text.get_rect(center=rect.center))

    @staticmethod
    def draw_settings_button(surface, mouse_pos=None):
        rect = SETTINGS_BUTTON_RECT
        hovered = mouse_pos is not None and rect.collidepoint(mouse_pos)
        color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, rect, border_radius=6)

        center = rect.center
        pygame.draw.circle(surface, COLOR_TEXT, center, 9, 3)
        pygame.draw.circle(surface, color, center, 3)
        for angle in range(0, 360, 45):
            direction = pygame.math.Vector2(1, 0).rotate(angle)
            start = pygame.Vector2(center) + direction * 9
            end = pygame.Vector2(center) + direction * 13
            pygame.draw.line(surface, COLOR_TEXT, start, end, 3)

    @staticmethod
    def play_button_hit(pos):
        return PLAY_BUTTON_RECT.collidepoint(pos)

    @staticmethod
    def settings_button_hit(pos):
        return SETTINGS_BUTTON_RECT.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.rebinding_action is not None:
                if event.key == pygame.K_ESCAPE:
                    self.rebinding_action = None
                else:
                    self.keybinds[self.rebinding_action] = event.key
                    self.rebinding_action = None
                return None
            if event.key == pygame.K_ESCAPE:
                return "close"
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                step = -1 if event.key == pygame.K_UP else 1
                current_index = TAB_NAMES.index(self.selected_tab)
                self.selected_tab = TAB_NAMES[
                    (current_index + step) % len(TAB_NAMES)]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.selected_tab == "Quit":
                    return "quit"
                self.active_tab = self.selected_tab
            return None

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None

        if CLOSE_BUTTON_RECT.collidepoint(event.pos):
            return "close"
        if self.active_tab == "Keybinds":
            for index, action in enumerate(KEYBIND_ACTIONS):
                rect = self._keybind_rect(index)
                if rect.collidepoint(event.pos):
                    self.rebinding_action = action
                    return None
        for name, rect in TAB_RECTS.items():
            if rect.collidepoint(event.pos):
                self.selected_tab = name
                if name == "Quit":
                    return "quit"
                self.active_tab = name
                return None
        return None

    def draw(self, surface, font, mouse_pos=None):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, COLOR_PANEL, PANEL_RECT, border_radius=8)
        pygame.draw.rect(surface, (130, 145, 160),
                         PANEL_RECT, 2, border_radius=8)
        sidebar = pygame.Rect(PANEL_RECT.left, PANEL_RECT.top,
                              150, PANEL_RECT.height)
        pygame.draw.rect(surface, COLOR_SIDEBAR, sidebar,
                         border_top_left_radius=8, border_bottom_left_radius=8)

        title = font.render("SETTINGS", True, COLOR_TEXT)
        surface.blit(title, (PANEL_RECT.left + 18, PANEL_RECT.top + 18))
        close = font.render("X", True, COLOR_TEXT)
        surface.blit(close, close.get_rect(center=CLOSE_BUTTON_RECT.center))
        pygame.draw.rect(surface, (100, 100, 100), CLOSE_BUTTON_RECT, 1,
                         border_radius=4)

        for name, rect in TAB_RECTS.items():
            active = name == self.active_tab
            selected = name == self.selected_tab
            color = COLOR_BUTTON_HOVER if active else COLOR_SIDEBAR
            pygame.draw.rect(surface, color, rect, border_radius=5)
            if selected:
                pygame.draw.rect(surface, (245, 245, 245), rect, 2,
                                 border_radius=5)
            text = font.render(name, True, COLOR_TEXT)
            surface.blit(text, text.get_rect(center=rect.center))

        content_x = PANEL_RECT.left + 180
        content_title = font.render(self.active_tab, True, COLOR_TEXT)
        surface.blit(content_title, (content_x, PANEL_RECT.top + 72))
        self._draw_content(surface, font, content_x, PANEL_RECT.top + 125)

    def _draw_content(self, surface, font, x, y):
        if self.active_tab == "Video":
            lines = ("Video settings will be added later.",)
        elif self.active_tab == "Audio":
            lines = ("Audio settings will be added later.",)
        else:
            self._draw_keybinds(surface, font, x, y)
            return

        max_width = PANEL_RECT.right - x - 18
        for index, line in enumerate(lines):
            line_font = self._fit_font(font, line, max_width)
            text = line_font.render(line, True, COLOR_MUTED)
            surface.blit(text, (x, y + index * 30))

    @staticmethod
    def _keybind_rect(index):
        return pygame.Rect(PANEL_RECT.left + 170, PANEL_RECT.top + 115 + index * 42,
                           PANEL_RECT.width - 190, 34)

    def _draw_keybinds(self, surface, font, x, y):
        for index, action in enumerate(KEYBIND_ACTIONS):
            rect = self._keybind_rect(index)
            selected = action == self.rebinding_action
            pygame.draw.rect(
                surface, COLOR_BUTTON if selected else COLOR_SIDEBAR,
                rect, border_radius=4,
            )
            if selected:
                pygame.draw.rect(surface, (245, 245, 245), rect, 2,
                                 border_radius=4)
            label = f"{KEYBIND_LABELS[action]}: {pygame.key.name(self.keybinds[action]).upper()}"
            line_font = self._fit_font(font, label, rect.width - 12)
            text = line_font.render(label, True, COLOR_TEXT)
            surface.blit(text, text.get_rect(
                midleft=(rect.left + 8, rect.centery)))

        instruction = (
            "Press a key to remap the selected row."
            if self.rebinding_action is not None
            else "Click a row to change its key."
        )
        instruction_font = self._fit_font(
            font, instruction, PANEL_RECT.width - 205)
        surface.blit(instruction_font.render(instruction, True, COLOR_MUTED),
                     (x, y + 180))

    @staticmethod
    def _fit_font(font, text, max_width):
        size = font.get_height()
        while size > 12:
            candidate = pygame.font.SysFont("consolas", size)
            if candidate.size(text)[0] <= max_width:
                return candidate
            size -= 1
        return pygame.font.SysFont("consolas", 12)

    def draw_play_screen(self, surface, title_font, body_font, mouse_pos=None,
                         game_over=False, score=0):
        surface.fill((0, 0, 0))
        title = title_font.render("BOUNCE BREAKER", True, COLOR_TEXT)
        surface.blit(title, title.get_rect(
            center=(surface.get_width() // 2, 135)))
        message = (
            "Press ENTER or click PLAY AGAIN"
            if game_over else "Press ENTER or click PLAY to start"
        )
        subtitle = body_font.render(message, True, COLOR_MUTED)
        surface.blit(subtitle, subtitle.get_rect(
            center=(surface.get_width() // 2, PLAY_BUTTON_RECT.bottom + 28)))
        if game_over:
            score_text = body_font.render(
                f"Final score: {score}", True, COLOR_TEXT)
            surface.blit(score_text, score_text.get_rect(
                center=(surface.get_width() // 2, PLAY_BUTTON_RECT.top - 46)))
        self.draw_button(
            surface, body_font, PLAY_BUTTON_RECT,
            "PLAY AGAIN" if game_over else "PLAY", mouse_pos,
        )
        self.draw_settings_button(surface, mouse_pos)
