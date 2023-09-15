import pygame
import json

AUTOTILE_MAP = {
    tuple(sorted([(1,0), (0, 1)])): 0,
    tuple(sorted([(1,0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1,0), (0, 1)])): 2,
    tuple(sorted([(-1,0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1,0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSET = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
PHYSICS_TILES = {'grass', 'stone'}
AUTOTILE_TYPES = {'grass', 'stone'}


class Tilemap:
    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.tile_map = {}
        self.offgrid_tiles = []

        # for i in range(10):
        #     self.tile_map[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
        #     self.tile_map['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def tiles_around(self, pos: list) -> list[dict]:
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tile_map:
                tiles.append(self.tile_map[check_loc])
        return tiles

    def phy_rects_around(self, pos: list) -> list[pygame.Rect]:
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size,
                                         self.tile_size, self.tile_size))
        return rects

    def autotile(self):
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tile_map:
                    if self.tile_map[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def draw(self, display: pygame.Surface, assets: dict, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            display.blit(assets[tile['type']][tile['variant']], (tile['pos'][0]-offset[0], tile['pos'][1]-offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + display.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + display.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tile_map:
                    tile = self.tile_map[loc]
                    display.blit(assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0],
                                                                         tile['pos'][1] * self.tile_size - offset[1]))

    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tile_map,
                       'tile_size': self.tile_size,
                       'offgrid': self.offgrid_tiles}, f)

    def load(self, path):
        with open(path, 'r') as f:
            map_data = json.load(f)
        self.tile_map = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
