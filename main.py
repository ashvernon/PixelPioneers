# main.py

import pygame
from pygame.locals import QUIT
from ui import SkillToolbar
from level import Level

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PixelPioneers (Lemmings-Style)")
    clock = pygame.time.Clock()

    # Create toolbar and level
    toolbar = SkillToolbar()
    # Assume you have a map text file called 'level1_map.txt' in the same folder
    level = Level("level1_map.txt", SCREEN_WIDTH, SCREEN_HEIGHT, target_exits=5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            # Let toolbar handle clicks on skill icons
            toolbar.handle_event(event)
            # Pass clicks (and the current skill) to level
            level.handle_event(event, toolbar.selected_skill)

        # Update game logic
        level.update()
        pygame.display.set_caption(
            f"PixelPioneers - Exits: {level.exit_count}/{level.target_exits} "
            f"Score: {int(level.get_score())}")

        # Draw everything
        screen.fill((0, 0, 0))
        level.draw(screen)
        toolbar.draw(screen, level)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
