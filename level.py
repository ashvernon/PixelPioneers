# level.py

import pygame
from tilemap import TileMap, TILE_SIZE
from lemming import Lemming

class Level:
    def __init__(self, map_file, screen_width, screen_height):
        # Load the tilemap
        self.tilemap = TileMap(map_file)

        # Camera starts at (0,0), but will follow the first lemming once it spawns
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)

        # Group for all lemmings
        self.lemmings = pygame.sprite.Group()

        # Spawn point (tile coordinates)
        self.spawn_point = (2, 2)

        # Timer to control spawning
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_interval = 2000  # spawn every 2000 ms

        self.completed = False
        self.failed = False

    def handle_event(self, event, selected_skill):
        """
        If the player clicks on a lemming while a skill is selected,
        assign that skill to the clicked lemming.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            world_x = mx + self.camera.x
            world_y = my + self.camera.y
            for lemming in self.lemmings:
                if lemming.rect.collidepoint(world_x, world_y):
                    lemming.assign_skill(selected_skill)
                    break

    def update(self):
        """
        Spawn new lemmings, update them, remove those that exit/fall off.
        Re‐enable camera follow so the viewport scrolls with the first lemming.
        """
        if self.completed or self.failed:
            return

        now = pygame.time.get_ticks()
        if now - self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = now
            self._spawn_lemming()

        # Update each lemming (pass the entire group so they can detect blockers)
        for lemming in list(self.lemmings):
            lemming.update(self.tilemap, self.lemmings)

            # If they've reached an exit tile, remove (“kill”) them
            cx, cy = lemming.rect.center
            if self.tilemap.is_exit_at_pixel(cx, cy):
                lemming.kill()
                continue

            # If they fall off the bottom of the map, remove them
            if lemming.rect.top > self.tilemap.height:
                lemming.kill()
                continue

        # Re‐enable camera‐follow: center on the first spawned lemming
        if self.lemmings:
            first = next(iter(self.lemmings))
            self.camera.centerx = first.rect.centerx
            self.camera.centery = first.rect.centery

            # Clamp camera coordinates so we never scroll outside the map bounds
            max_x = self.tilemap.width - self.camera.width
            max_y = self.tilemap.height - self.camera.height

            self.camera.x = max(0, min(self.camera.x, max_x))
            self.camera.y = max(0, min(self.camera.y, max_y))

    def _spawn_lemming(self):
        """
        Create a new Lemming at the spawn point (tile -> pixel) and add it.
        """
        px = self.spawn_point[0] * TILE_SIZE + (TILE_SIZE // 2)
        py = self.spawn_point[1] * TILE_SIZE
        lemming = Lemming((px, py))
        self.lemmings.add(lemming)

    def draw(self, surface):
        """
        Draw the tilemap first, then draw each lemming, applying the camera offset.
        """
        # Draw tiles (ground and exit) offset by the camera
        self.tilemap.draw(surface, (self.camera.x, self.camera.y))

        # Draw each lemming at its world‐position minus camera‐offset
        for lemming in self.lemmings:
            lemming.draw(surface, self.camera)
