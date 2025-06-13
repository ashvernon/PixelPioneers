import pygame
import sys
import os
from tilemap import TILE_SIZE

# Default map dimensions if creating new maps
DEFAULT_COLS = 40
DEFAULT_ROWS = 30

# Colors for tiles
COLORS = {
    '#': (100, 100, 100),
    'E': (50, 50, 200),
    '.': (0, 0, 0)
}

# Order in which tiles are cycled/selected
TILE_TYPES = ['#', 'E', '.']

FONT_COLOR = (255, 255, 255)
BACKGROUND = (0, 0, 0)

class LevelCreator:
    """Simple GUI tool to create/edit tilemap text files."""

    def __init__(self, map_file=None, cols=DEFAULT_COLS, rows=DEFAULT_ROWS):
        self.map_file = map_file
        if map_file and os.path.exists(map_file):
            self.map_data = self._load_map(map_file)
            self.rows = len(self.map_data)
            self.cols = len(self.map_data[0]) if self.rows > 0 else 0
        else:
            self.cols = cols
            self.rows = rows
            self.map_data = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        self.selected_index = 0
        self.selected = TILE_TYPES[self.selected_index]
        w = self.cols * TILE_SIZE
        h = self.rows * TILE_SIZE + 40  # space for instructions
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Level Creator")
        self.font = pygame.font.SysFont(None, 24)

    def _load_map(self, filename):
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n') for line in f]
        return [list(line) for line in lines]

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        self.selected_index = 0
                    elif event.key == pygame.K_2:
                        self.selected_index = 1
                    elif event.key == pygame.K_3:
                        self.selected_index = 2
                    elif event.key == pygame.K_s:
                        if self.map_file:
                            self._save_map(self.map_file)
                            print(f"Saved to {self.map_file}")
                    self.selected = TILE_TYPES[self.selected_index]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self._place_tile(event.pos, TILE_TYPES[self.selected_index])
                    elif event.button == 3:
                        self._place_tile(event.pos, '.')
                    elif event.button == 4:  # scroll up
                        self.selected_index = (self.selected_index - 1) % len(TILE_TYPES)
                        self.selected = TILE_TYPES[self.selected_index]
                    elif event.button == 5:  # scroll down
                        self.selected_index = (self.selected_index + 1) % len(TILE_TYPES)
                        self.selected = TILE_TYPES[self.selected_index]
            self._draw()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def _place_tile(self, pos, tile_char):
        x, y = pos
        col = x // TILE_SIZE
        row = y // TILE_SIZE
        if row < self.rows and col < self.cols:
            self.map_data[row][col] = tile_char

    def _draw(self):
        self.screen.fill(BACKGROUND)
        for r, row in enumerate(self.map_data):
            for c, tile in enumerate(row):
                color = COLORS.get(tile, BACKGROUND)
                rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

        # Highlight the tile under the mouse with the selected color
        mx, my = pygame.mouse.get_pos()
        col = mx // TILE_SIZE
        row = my // TILE_SIZE
        if row < self.rows and col < self.cols:
            preview_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            highlight_color = COLORS.get(self.selected, (255, 255, 255))
            pygame.draw.rect(self.screen, highlight_color, preview_rect, 2)

        self._draw_instructions()

    def _draw_instructions(self):
        text = (
            f"Selected: {self.selected}  [1] Ground  [2] Exit  [3] Empty  "
            "Left Click: place  Right Click: erase  Wheel: cycle  [S] Save  [Esc] Quit"
        )
        img = self.font.render(text, True, FONT_COLOR)
        rect = img.get_rect()
        rect.topleft = (5, self.rows * TILE_SIZE + 5)
        self.screen.blit(img, rect)

    def _save_map(self, filename):
        with open(filename, 'w') as f:
            for row in self.map_data:
                f.write(''.join(row) + '\n')

if __name__ == '__main__':
    pygame.init()
    file_arg = sys.argv[1] if len(sys.argv) > 1 else 'new_map.txt'
    creator = LevelCreator(file_arg)
    creator.run()
