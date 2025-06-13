# tilemap.py

import pygame

TILE_SIZE = 16  # pixels per tile

class TileMap:
    """
    A very simple tilemap where:
      - '#' = solid ground (drawn as a filled gray rectangle)
      - '.' = empty (nothing drawn)
      - 'E' = exit (drawn as a filled blue rectangle)
    """

    def __init__(self, map_file):
        # Load from a text file (e.g., 'level1_map.txt')
        self.map_data = self._load_map_data(map_file)
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0]) if self.rows > 0 else 0
        self.width = self.cols * TILE_SIZE
        self.height = self.rows * TILE_SIZE
        # tilemap.py, at the end of __init__:
        print(f"[TileMap] Loaded map: {self.rows} rows × {self.cols} cols  (pixels: {self.width}×{self.height})")


    def _load_map_data(self, map_file):
        with open(map_file, "r") as f:
            lines = [line.rstrip("\n") for line in f]
        return [list(line) for line in lines]

    def is_solid_at_pixel(self, x, y):
        """
        Return True if the tile at world-pixel (x, y) is '#'.
        """
        col = int(x // TILE_SIZE)
        row = int(y // TILE_SIZE)
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        return self.map_data[row][col] == "#"

    def is_exit_at_pixel(self, x, y):
        """
        Return True if the tile at world-pixel (x, y) is 'E'.
        """
        col = int(x // TILE_SIZE)
        row = int(y // TILE_SIZE)
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        return self.map_data[row][col] == "E"

    def remove_tile(self, col, row):
        """
        Replace the tile at (col, row) with '.' (digging).
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.map_data[row][col] = "."

    def add_tile(self, col, row, tile_char="#"):
        """
        Place a tile (by default '#') at (col, row).
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.map_data[row][col] = tile_char

    def draw(self, surface, camera_offset=(0, 0)):
        """
        Draw each tile as a filled rect:
         - '#' = dark gray
         - 'E' = blue
         - '.' = skip
        """
        cam_x, cam_y = camera_offset
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile_char in enumerate(row):
                if tile_char == "#":
                    rect = pygame.Rect(
                        col_idx * TILE_SIZE - cam_x,
                        row_idx * TILE_SIZE - cam_y,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    pygame.draw.rect(surface, (100, 100, 100), rect)
                elif tile_char == "E":
                    rect = pygame.Rect(
                        col_idx * TILE_SIZE - cam_x,
                        row_idx * TILE_SIZE - cam_y,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    pygame.draw.rect(surface, (50, 50, 200), rect)
                # if '.', do nothing
