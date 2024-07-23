import pygame as pg
from map import Tile
from unit import Unit, Fortress
from random import choice
pg.init()

class Game:

    bg_theme = pg.mixer.Sound('sources/sounds/Background_theme.mp3')
    bg_theme.set_volume(0.1)

    choose_unit_sound = pg.mixer.Sound('sources/sounds/Choose_unit_sound_effect.wav')
    choose_unit_sound.set_volume(0.35)

    killing_sound_effect = pg.mixer.Sound('sources/sounds/killing_sound_effect.mp3')
    killing_sound_effect.set_volume(0.35)

    move_sound_effect = pg.mixer.Sound('sources/sounds/move_sound_effect.wav')
    move_sound_effect.set_volume(0.35)
    def __init__(self):
        # Screen
        self.screen = pg.display.set_mode((1000, 700))

        # Tiles
        self.tiles = self.__get_tiles()

        # Fortresses
        self.fortresses_group = pg.sprite.Group(
            Fortress((350, 50), 'red'),
            Fortress((350, 550), 'blue')
        )

        # Units
        self.red_units = self.__get_red_units()
        self.blue_units = self.__get_blue_units()

        self.units_group = pg.sprite.Group(
            self.red_units.sprites(),
            self.blue_units.sprites()
        )

        self.all_playable_sprites = pg.sprite.Group(
            self.fortresses_group.sprites(),
            self.units_group.sprites()
        )

        self.__fill_tiles()
        # self.__count_neighbours()

        self.FPS = pg.time.Clock()

        # Timer
        self.choose_timer = 120

        # Turns
        self.turn_flag = choice([True, False])
        self.current_unit = None

        self.__set_neighbours()
        self.__set_chains_power()

    def run(self):
        self.bg_theme.play(-1)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            self.screen.fill('white')

            # Sprites update
            self.tiles.update(self.screen)
            self.fortresses_group.update(self.screen)
            self.blue_units.update(self.fortresses_group, self.screen)
            self.red_units.update(self.fortresses_group, self.screen)

            self.__choose_unit()
            self.__draw_points()
            self.__reload_timer()
            self.__unit_move()

            self.__show_turn()
            self.FPS.tick(240)
            pg.display.update()

    def print_all_tiles(self):
        for tile in self.tiles:
            if tile.sprite:
                print(tile.rect.center, tile.sprite)

    def __reload_timer(self):
        if self.choose_timer < 120:
            self.choose_timer += 1

    def __switch_turn(self):
        self.turn_flag = not self.turn_flag
        self.current_unit = None

    def __choose_unit(self):
        sprites = self.blue_units.sprites() if self.turn_flag else self.red_units.sprites()
        for unit in sprites:
            if unit.is_pressed() and self.choose_timer == 120:
                self.choose_unit_sound.play()
                self.current_unit = None if self.current_unit else unit
                self.choose_timer = 0
                break

    def __unit_move(self):
        if self.current_unit is not None and pg.mouse.get_pressed()[0]:
            m_pos = pg.mouse.get_pos()
            for tile in self.tiles:
                if tile.rect.collidepoint(m_pos) and self.current_unit.can_move() and tile.sprite is not self.current_unit:
                    if not tile.sprite:
                        self.move_sound_effect.play()
                        self.current_unit.rect.center = tile.rect.center
                        self.__switch_turn()
                    if tile.sprite and tile.sprite.color != self.current_unit.color and self.current_unit.power > tile.sprite.power:
                        self.killing_sound_effect.play()
                        tile.sprite.kill()
                        tile.sprite = None
                    self.__fill_tiles()
                    self.__set_neighbours()
                    self.__set_chains_power()

    def __draw_points(self):
        if self.current_unit is not None:
            for tile in self.tiles:
                if not tile.sprite and tile.rect.center in self.current_unit.get_neighbours_cords():
                    pg.draw.circle(self.screen, 'green', tile.rect.center, 20)

    def __show_turn(self):
        pg.draw.circle(self.screen, 'black', (850, 110), 105)
        if self.turn_flag:
            pg.draw.circle(self.screen, 'blue', (850, 110), 100)
        else:
            pg.draw.circle(self.screen, 'red', (850, 110), 100)

    def __fill_tiles(self):
        for tile in self.tiles:
            for sprite in self.all_playable_sprites:
                if tile.rect.colliderect(sprite.rect):
                    tile.sprite = sprite
                    break
                else:
                    tile.sprite = None

    def __set_neighbours(self):
        for unit in self.units_group:
            unit.neighbours = pg.sprite.Group()
            for neighbour in self.units_group:
                for cord in unit.get_neighbours_x_y_cords():
                    if neighbour.rect.collidepoint(cord) and neighbour.color == unit.color:
                        unit.neighbours.add(neighbour)

    def __count_unit_chain(self, head, chain: pg.sprite.Group):
        count = 0
        if len(head.neighbours) == 0:
            if head not in chain:
                count += 1
                chain.add(head)
        else:
            for neighbour in head.neighbours:
                if neighbour not in chain:
                    count += 1
                    chain.add(neighbour)
                    count += self.__count_unit_chain(neighbour, chain)
        return count

    def __set_chains_power(self):
        for unit in self.units_group:
            unit.power = self.__count_unit_chain(unit, pg.sprite.Group())
            unit.update_power_image()

    @staticmethod
    def __get_tiles():
        tiles = pg.sprite.Group()
        for i in range(6):
            for j in range(7):
                tile = Tile((100 * j, 100 * i))
                tiles.add(tile)
        return tiles

    @staticmethod
    def __get_red_units():
        red_units = pg.sprite.Group()
        for h in range(7):
            if h != 3:
                sprite = Unit((100 * h + 50, 50), 'red')
                red_units.add(sprite)
        return red_units

    @staticmethod
    def __get_blue_units():
        blue_units = pg.sprite.Group()
        for h in range(7):
            if h != 3:
                sprite = Unit((100 * h + 50, 550), 'blue')
                blue_units.add(sprite)
        return blue_units


game = Game()
game.run()
