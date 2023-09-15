import pygame

from os import listdir
from os.path import join

BASE_IMG_PATH = ('assets', 'images')
BLACK = (0, 0, 0)


def load_all_imgs() -> dict:
    assets = {}
    for i in listdir(join(*BASE_IMG_PATH)):
        if i.endswith('.png'):
            assets[i[:-4]] = load_img(i)
        else:
            for j in listdir(join(*BASE_IMG_PATH, i)):
                if j.endswith('.png'):
                    assets[i] = load_imgs(i)
                else:
                    for k in listdir(join(*BASE_IMG_PATH, i, j)):
                        if k.endswith('.png'):
                            assets[j] = load_imgs(i, j)
                        else:
                            for _ in listdir(join(*BASE_IMG_PATH, i, j, k)):
                                assets[k] = Animation(load_imgs(i, j, k))
    assets['p_idle'].img_dur = 6
    assets['p_run'].img_dur = 4
    return assets


def load_img(*path) -> pygame.Surface:
    img = pygame.image.load(join(*BASE_IMG_PATH, *path)).convert()
    img.set_colorkey(BLACK)
    return img


def load_imgs(*path) -> list[pygame.Surface]:
    imgs = []
    for img_name in sorted(listdir(join(*BASE_IMG_PATH, *path))):
        imgs.append(load_img(join(*path, img_name)))
    return imgs


def load_tiles() -> dict:
    lst = [i for i in listdir(join(*BASE_IMG_PATH, 'tiles'))]
    assets = {i: load_imgs(join('tiles', i)) for i in lst}
    assets.pop('spawners')
    return assets


class Animation:
    def __init__(self, imgs: list[pygame.Surface], img_dur=5, loop=True):
        self.imgs = imgs
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    # def copy(self):
    #     return Animation(self.imgs, self.img_dur, self.loop)

    def img(self) -> pygame.Surface:
        return self.imgs[int(self.frame / self.img_dur)]

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.imgs))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.imgs) - 1)
            if self.frame >= self.img_dur * len(self.imgs) - 1:
                self.done = True
