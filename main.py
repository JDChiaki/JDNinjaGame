import pygame
from os.path import join

from scripts.entities import Player
from scripts.utils import load_img, load_all_imgs
from scripts.tilemap import Tilemap
from scripts.cloud import Clouds

pygame.init()


class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 640, 480
        self.FPS = 60
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display = pygame.Surface((self.WIDTH // 2, self.HEIGHT // 2))
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption('JDNinja')
        pygame.display.set_icon(load_img('logo.png'))

        self.assets = load_all_imgs()
        # print(self.assets['p_run'].img_dur)
        self.player = Player(self.assets, (50, 50), (8, 15))
        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.tile_map = Tilemap(tile_size=16)
        try:
            self.tile_map.load(join('assets', 'maps', '1.json'))
        except FileNotFoundError:
            pass
        self.scroll = [0, 0]

    def _camera_move(self):
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
        self.scroll_offset = (int(self.scroll[0]), int(self.scroll[1]))

    def _draw(self):
        self.display.blit(self.assets['background'], (0, 0))
        self._camera_move()
        self.clouds.update()
        self.clouds.draw(self.display, offset=self.scroll_offset)
        self.tile_map.draw(self.display, self.assets, offset=self.scroll_offset)
        self.player.update(self.tile_map, (self.player.movement[1]-self.player.movement[0], 0))
        self.player.draw(self.display, offset=self.scroll_offset)
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.player.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.player.movement[1] = False
            self._draw()
        pygame.quit()
        quit()


if __name__ == '__main__':
    Game().run()
