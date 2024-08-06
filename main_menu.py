import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, size:tuple, pos, text):
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect(center=pos)

        #Text
        font = pg.font.SysFont('Arial', 20)
        self.text = text
        self.text_image = font.render(text, True, 'white')
        self.image.blit(self.text_image, (0, 0))

    def is_pressed(self):
        mpos = pg.mouse.get_pos()
        m_pressed = pg.mouse.get_pressed()
        if m_pressed[0] and self.rect.collidepoint(mpos):
            return True
        return False

    def update(self, screen):
        screen.blit(self.image, self.rect)