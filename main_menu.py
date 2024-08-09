import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, size:tuple, pos, text):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)

        # Text
        font = pg.font.SysFont('Arial', 40)
        self.text = text
        self.text_image = font.render(text, True, 'Black')
        self.text_rect = self.text_image.get_rect(center=self.rect.center)

    def is_pressed(self):
        mpos = pg.mouse.get_pos()
        m_pressed = pg.mouse.get_pressed()
        if m_pressed[0] and self.rect.collidepoint(mpos):
            return True
        return False

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_image, self.text_rect)
        pg.draw.rect(screen, 'black', self.rect, 2)