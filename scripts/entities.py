import pygame

from scripts.tilemap import Tilemap
from scripts.utils import Animation


class PhysicsEntity:

    def __init__(self, assets: dict, e_type: str, pos: tuple[int, int], size: tuple[int, int]):
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0.0, 0.0]
        self.movement = [False, False]
        self.collisions: dict | None = None
        self.action: str | None = None
        self.animation_offset = (-3, -3)
        self.flip = False
        self.animation: Animation | None = None
        self.assets = assets

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.e_type + '_' + self.action]

    def rect(self) -> pygame.Rect:
        return pygame.Rect(*self.pos, *self.size)

    def update(self, tile_map: Tilemap, movement=(0, 0)):
        self.collisions = {'top': False, 'bottom': False, 'left': False, 'right': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tile_map.phy_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tile_map.phy_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['bottom'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['top'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5.0, self.velocity[1] + 0.1)

        if self.collisions['bottom'] or self.collisions['top']:
            self.velocity[1] = 0
        if self.animation:
            self.animation.update()

    def draw(self, display: pygame.Surface, offset=(0, 0)):
        # print(self.animation)
        display.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                     (self.pos[0] - offset[0] + self.animation_offset[0],
                      self.pos[1] - offset[1] + self.animation_offset[1]))


class Player(PhysicsEntity):
    def __init__(self, assets: dict, pos: tuple, size: tuple):
        super().__init__(assets, 'p', pos, size)
        self.air_time = 0

    def update(self, tile_map: Tilemap, movement=(0, 0)):
        super().update(tile_map, movement=movement)

        self.air_time += 1
        if self.collisions['bottom']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
