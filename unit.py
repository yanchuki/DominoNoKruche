import pygame as pg
pg.init()

class Unit(pg.sprite.Sprite):
    def __init__(self, pos: tuple, color):
        super().__init__()
        self.image = pg.Surface((90, 90))
        self.image.fill('white')
        self.chosen = False
        self.color = color
        pg.draw.circle(self.image, color, (45, 45), 45)
        pg.draw.circle(self.image, 'black', (45, 45), 45, 3)
        self.power = 0
        font = pg.font.SysFont('arial', 20)
        self.power_image = font.render(str(self.power), True, (154, 219, 171))
        self.image.blit(self.power_image, (70, 20))
        self.rect = self.image.get_rect(center=pos)
        self.neighbours = pg.sprite.Group()

    def is_pressed(self):
        m_pos = pg.mouse.get_pos()
        m_pressed = pg.mouse.get_pressed()
        if m_pressed[0] and self.rect.collidepoint(m_pos):
            return True

    def can_move(self):
        m_pos = pg.mouse.get_pos()
        return abs(self.rect.centerx - m_pos[0]) < 150 and abs(self.rect.centery - m_pos[1]) < 150

    def update_power_image(self):
        font = pg.font.SysFont('arial', 20)
        pg.draw.circle(self.image, self.color, (45, 45), 45)
        pg.draw.circle(self.image, 'black', (45, 45), 45, 3)
        self.power_image = font.render(str(self.power), True, (154, 219, 171))
        self.image.blit(self.power_image, (70, 20))

    def get_neighbours_cords(self):
        return [(self.rect.centerx - 100, self.rect.centery - 100),
                (self.rect.centerx - 100, self.rect.centery + 100),
                (self.rect.centerx + 100, self.rect.centery - 100),
                (self.rect.centerx + 100, self.rect.centery + 100),
                (self.rect.centerx - 100, self.rect.centery),
                (self.rect.centerx + 100, self.rect.centery),
                (self.rect.centerx, self.rect.centery + 100),
                (self.rect.centerx, self.rect.centery - 100)]

    def get_neighbours_x_y_cords(self):
        return [(self.rect.centerx - 100, self.rect.centery),
                (self.rect.centerx + 100, self.rect.centery),
                (self.rect.centerx, self.rect.centery + 100),
                (self.rect.centerx, self.rect.centery - 100)]

    def update(self, fortresses_group, screen):
        screen.blit(self.image, self.rect)


class Fortress(pg.sprite.Sprite):
    def __init__(self, pos: tuple, color):
        super().__init__()
        self.image = pg.Surface((90, 90))
        self.image.fill('white')
        pg.draw.circle(self.image, color, (45, 45), 45)
        pg.draw.circle(self.image, 'black', (45, 45), 45, 3)
        crown = pg.transform.scale(pg.image.load('sources/images/crown.png'), (40, 40))
        self.image.blit(crown, (25, 25))
        self.rect = self.image.get_rect(center=pos)
        self.color = color

    def update(self, screen):
        screen.blit(self.image, self.rect)
