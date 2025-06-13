# ui.py

import pygame

SKILLS = ["dig", "build", "block"]

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
        self.selected_skill = None

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

    def draw(self, surface):
        # Draw background bar
        bar_rect = pygame.Rect(0, 0, surface.get_width(), self.icon_size + 2*self.icon_padding)
        pygame.draw.rect(surface, (30, 30, 30), bar_rect)

        # Draw each skill as a filled square
        for idx, rect in enumerate(self.icon_rects):
            color = (200, 50, 50) if SKILLS[idx] == "dig" else \
                    (50, 50, 200) if SKILLS[idx] == "build" else \
                    (200, 200, 50)
            pygame.draw.rect(surface, color, rect)

            # If selected, draw a yellow border
            if SKILLS[idx] == self.selected_skill:
                pygame.draw.rect(surface, (255, 255, 0), rect.inflate(4, 4), 2)
