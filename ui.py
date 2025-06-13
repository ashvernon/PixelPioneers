# ui.py

import pygame

SKILLS = ["dig", "build", "block", "umbrella"]


def _draw_gradient_rect(surface, rect, color1, color2):
    """Draw a simple vertical gradient"""
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r = color1[0] + (color2[0] - color1[0]) * ratio
        g = color1[1] + (color2[1] - color1[1]) * ratio
        b = color1[2] + (color2[2] - color1[2]) * ratio
        pygame.draw.line(surface, (int(r), int(g), int(b)), (x, y + i), (x + w, y + i))

class SkillToolbar:
    """
    A simple toolbar at the top of the screen with three colored squares:
      - dig  = red
      - build = blue
      - block = yellow
    Click to select/deselect a skill.
    """

    def __init__(self):
        self.icon_size = 32
        self.icon_padding = 10
        self.bar_height = self.icon_size + 2 * self.icon_padding
        self.selected_skill = None

        # Font for HUD information
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 20)

        # Precompute rectangles for each skill
        self.icon_rects = []
        x = self.icon_padding
        y = self.icon_padding
        for _ in SKILLS:
            rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
            self.icon_rects.append(rect)
            x += self.icon_size + self.icon_padding

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for idx, rect in enumerate(self.icon_rects):
                if rect.collidepoint(mx, my):
                    skill = SKILLS[idx]
                    if self.selected_skill == skill:
                        self.selected_skill = None
                    else:
                        self.selected_skill = skill
                    return  # only one can be toggled per click

    def draw(self, surface, level=None):
        # Draw background bar with a subtle gradient
        bar_rect = pygame.Rect(0, 0, surface.get_width(), self.bar_height)
        _draw_gradient_rect(surface, bar_rect, (40, 40, 40), (25, 25, 25))

        # Draw each skill as a colored circle
        color_map = {
            "dig": (220, 70, 70),
            "build": (70, 70, 220),
            "block": (220, 220, 70),
            "umbrella": (150, 150, 220),
        }
        for idx, rect in enumerate(self.icon_rects):
            color = color_map.get(SKILLS[idx], (200, 200, 200))
            center = rect.center
            radius = rect.width // 2 - 2
            pygame.draw.circle(surface, color, center, radius)

            # If selected, draw a white border around the circle
            if SKILLS[idx] == self.selected_skill:
                pygame.draw.circle(surface, (255, 255, 255), center, radius + 2, 2)

        # Draw HUD info on the right
        if level is not None:
            info = (
                f"Exits: {level.exit_count}/{level.target_exits} | "
                f"Score: {int(level.get_score())} | "
                f"Time: {int(level.get_elapsed_time())}s"
            )
            text_surf = self.font.render(info, True, (240, 240, 240))
            text_rect = text_surf.get_rect()
            text_rect.top = self.icon_padding
            text_rect.right = surface.get_width() - self.icon_padding
            surface.blit(text_surf, text_rect)
