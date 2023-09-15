import pygame

# from scripts.entities import Player
from scripts.utils import load_img, load_tiles
from scripts.tilemap import Tilemap
# from scripts.cloud import Clouds
# from os import listdir
# from os.path import join

pygame.init()

RENDER_SCALE = 2.0


class Editor:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 640, 480
        self.FPS = 60
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display = pygame.Surface((self.WIDTH // 2, self.HEIGHT // 2))
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption('Editor')
        pygame.display.set_icon(load_img('logo.png'))

        self.assets = load_tiles()
        self.movement = [False, False, False, False]
        # self.assets = load_to_assets(self.assets)
        # print(self.assets)
        # self.player = Player(self.assets, (50, 50), (8, 15))
        # self.clouds = Clouds(self.assets['clouds'], count=16)
        self.tile_map = Tilemap(tile_size=16)
        try:
            self.tile_map.load('map.json')
        except FileNotFoundError:
            print('File not found')
        self.scroll = [0, 0]

        self.tile_list = list(self.assets.keys())
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.r_clicking = False
        self.shift = False

        self.ongrid = True

    def _camera_move(self):
        # self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
        # self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
        self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
        self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
        self.scroll_offset = (int(self.scroll[0]), int(self.scroll[1]))

    def _draw_tile_img(self):
        self.current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
        self.current_tile_img.set_alpha(100)
        self.display.blit(self.current_tile_img, (5, 5))

    def _place_tile(self):
        self.mpos = pygame.mouse.get_pos()
        self.mpos = (self.mpos[0] / RENDER_SCALE, self.mpos[1] / RENDER_SCALE)
        tile_pos = (int((self.mpos[0] + self.scroll[0]) // self.tile_map.tile_size),
                    int((self.mpos[1] + self.scroll[1]) // self.tile_map.tile_size))

        if self.ongrid:
            self.display.blit(self.current_tile_img, (tile_pos[0] * self.tile_map.tile_size - self.scroll[0],
                                                      tile_pos[1] * self.tile_map.tile_size - self.scroll[1]))
        else:
            self.display.blit(self.current_tile_img, self.mpos)

        if self.clicking and self.ongrid:
            self.tile_map.tile_map[str(tile_pos[0]) + ';' + str(tile_pos[1])] = \
                {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
        if self.r_clicking:
            tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
            if tile_loc in self.tile_map.tile_map:
                del self.tile_map.tile_map[tile_loc]
            for tile in self.tile_map.offgrid_tiles.copy():
                tile_img = self.assets[tile['type']][tile['variant']]
                tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                     tile_img.get_width(), tile_img.get_height())
                if tile_r.collidepoint(self.mpos):
                    self.tile_map.offgrid_tiles.remove(tile)

    def _draw(self):
        self.display.fill((0, 0, 0))
        self._draw_tile_img()
        self._camera_move()
        self._place_tile()
        # self.clouds.update()
        # self.clouds.draw(self.display, offset=self.scroll_offset)
        self.tile_map.draw(self.display, self.assets, offset=self.scroll_offset)
        # self.player.update(self.tile_map, (self.player.movement[1]-self.player.movement[0], 0))
        # self.player.draw(self.display, offset=self.scroll_offset)
        self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0, 0))
        pygame.display.update()

    def run(self):
        runnng = True
        while runnng:
            self.CLOCK.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runnng = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tile_map.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 
                                                                'variant': self.tile_variant,
                                                                'pos': (self.mpos[0] + self.scroll[0],
                                                                        self.mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.r_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = ((self.tile_variant-1) %
                                                 len(self.assets[self.tile_list[self.tile_group]]))
                        if event.button == 5:
                            self.tile_variant = ((self.tile_variant+1) %
                                                 len(self.assets[self.tile_list[self.tile_group]]))
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.r_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if event.mod & pygame.KMOD_CTRL:
                            self.tile_map.autotile()
                        else:
                            self.movement[0] = True
                        # self.player.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                        # self.player.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                        # self.player.velocity[1] = -3
                    if event.key == pygame.K_s:
                        if event.mod & pygame.KMOD_CTRL:
                            self.tile_map.save('map.json')
                        else:
                            self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                        # self.player.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                        # self.player.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                        # self.player.velocity[1] = -3
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            self._draw()
        pygame.quit()
        quit()


if __name__ == '__main__':
    Editor().run()
