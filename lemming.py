# lemming.py

import pygame
from tilemap import TILE_SIZE

# Movement constants
WALK_SPEED = 1.0
GRAVITY = 0.2
MAX_FALL_SPEED = 4.0

class Lemming(pygame.sprite.Sprite):
    """
    A single lemming, drawn as a green rectangle ~ (TILE_SIZE/2 × TILE_SIZE/2).
    States:
      - "walking": moves horizontally, checks for ground and blockers ahead
      - "falling": obeys gravity until it lands
      - "digging": removes one tile below, then falls
      - "building": adds one tile in front/above, then walks
      - "blocking": stands in place
    """

    def __init__(self, spawn_pos):
        super().__init__()
        # Create a simple green rectangle as the “sprite”
        size = TILE_SIZE // 2
        self.image = pygame.Surface((size, size))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(midbottom=spawn_pos)

        # Velocity
        self.vx = WALK_SPEED
        self.vy = 0

        # Direction: +1 = right, -1 = left
        self.direction = 1

        # Initial state
        self.state = "walking"
        self.skill_assigned = None

        # Placeholder for sounds
        # self.dig_sound = None  # TODO: load dig.wav here
        # self.build_sound = None  # TODO: load build.wav here

    def assign_skill(self, skill_name):
        """
        Called by Level when the player clicks on this lemming
        while having a skill selected (e.g. "dig", "build", "block").
        """
        if self.state in ("walking", "falling"):
            self.skill_assigned = skill_name

    def update(self, tilemap, all_lemmings):
        """
        Perform one step of behavior depending on self.state,
        possibly consuming self.skill_assigned.
        """
        # Check if a skill was clicked
        if self.skill_assigned == "dig" and self.state == "walking":
            self.state = "digging"
            self.skill_assigned = None
        elif self.skill_assigned == "build" and self.state == "walking":
            self.state = "building"
            self.skill_assigned = None
        elif self.skill_assigned == "block" and self.state in ("walking", "falling"):
            self.state = "blocking"
            self.vx = 0
            self.vy = 0
            self.skill_assigned = None

        # State behavior
        if self.state == "walking":
            self._walk(tilemap, all_lemmings)
        elif self.state == "falling":
            self._fall(tilemap)
        elif self.state == "digging":
            self._dig(tilemap)
        elif self.state == "building":
            self._build(tilemap)
        elif self.state == "blocking":
            # Just stand; other lemmings will now treat me as an obstacle
            pass

    def _walk(self, tilemap, all_lemmings):
        """
        Attempt to move horizontally by WALK_SPEED * direction,
        but first check:
        1) Wall/tile collision
        2) Blocking lemming collision
        3) Ground ahead (else switch to falling)
        """
        next_x = self.rect.x + self.vx * self.direction

        # 1) Check for a solid tile in front (at foot height)
        foot_y = self.rect.bottom - 1
        check_x = next_x + (self.rect.width if self.direction == 1 else 0)
        if tilemap.is_solid_at_pixel(check_x, foot_y):
            # Hit a wall → turn around
            self.direction *= -1
            return

        # 2) Check for a blocking lemming in front
        next_rect = self.rect.copy()
        next_rect.x = next_x
        for other in all_lemmings:
            if other is not self and other.state == "blocking":
                if next_rect.colliderect(other.rect):
                    # We would run into a blocking lemming → turn around
                    self.direction *= -1
                    return

        # 3) Check if ground ahead is missing → start falling
        ahead_px = self.rect.midbottom[0] + (self.rect.width // 2) * self.direction
        below_py = self.rect.bottom + 1
        if not tilemap.is_solid_at_pixel(ahead_px, below_py):
            self.state = "falling"
            self.vy = 0
            return

        # 4) All clear → move horizontally
        self.rect.x = next_x

    def _fall(self, tilemap):
        # Apply gravity
        self.vy = min(self.vy + GRAVITY, MAX_FALL_SPEED)
        self.rect.y += self.vy

        # Check if landed
        foot_x = self.rect.midbottom[0]
        foot_y = self.rect.bottom
        if tilemap.is_solid_at_pixel(foot_x, foot_y + 1):
            # Snap to top of that tile
            row = foot_y // TILE_SIZE
            self.rect.bottom = row * TILE_SIZE
            self.state = "walking"
            self.vy = 0

    def _dig(self, tilemap):
        """
        Remove the tile directly below, then switch to falling.
        """
        # TODO: if self.dig_sound: self.dig_sound.play()
        col = int(self.rect.centerx // TILE_SIZE)
        row = int(self.rect.bottom // TILE_SIZE)
        tilemap.remove_tile(col, row)
        self.state = "falling"
        self.vy = 0

    def _build(self, tilemap):
        """
        Place one tile in front/above to let the lemming step up, then resume walking.
        """
        # TODO: if self.build_sound: self.build_sound.play()
        col = int(self.rect.centerx // TILE_SIZE)
        row = int(self.rect.bottom // TILE_SIZE)
        target_col = col + self.direction
        target_row = row - 1
        tilemap.add_tile(target_col, target_row, "#")
        self.state = "walking"

    def draw(self, surface, camera):
        """
        Draw the lemming’s green rectangle at (world-coords minus camera).
        """
        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        surface.blit(self.image, (screen_x, screen_y))
