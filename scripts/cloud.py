import random
import pygame


class Cloud:
    def __init__(self, pos, img: pygame.Surface, spd, depth):
        self.pos = list(pos)
        self.img = img
        self.spd = spd
        self.depth = depth

    def update(self):
        self.pos[0] += self.spd

    def draw(self, display: pygame.Surface, offset=(0, 0)):
        pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        display.blit(self.img, (pos[0] % (display.get_width() + self.img.get_width()) - self.img.get_width(),
                                pos[1] % (display.get_height() + self.img.get_height()) - self.img.get_height()))


class Clouds:
    def __init__(self, imgs: list[pygame.Surface], count=16):
        self.clouds = []

        for i in range(count):
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(imgs),
                                     random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def draw(self, display: pygame.Surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.draw(display, offset=offset)
