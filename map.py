import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, pos: tuple):
        super().__init__()
        self.image = pg.Surface((100, 100))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=pos)
        self.sprite = None

    def update(self, screen):
        screen.blit(self.image, self.rect)
        pg.draw.rect(screen, 'black', self.rect, 2)
