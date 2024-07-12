import pygame as pg
from map import Tile
from unit import Unit, Fortress
from random import choice

class Game:
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
        self.__count_neighbours()

        self.FPS = pg.time.Clock()

        # Timer
        self.choose_timer = 120

        # Turns
        self.turn_flag = choice([True, False])
        self.current_unit = None

    def run(self):
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
                self.current_unit = None if self.current_unit else unit
                self.choose_timer = 0
                break

    def __unit_move(self):
        if self.current_unit is not None and pg.mouse.get_pressed()[0]:
            m_pos = pg.mouse.get_pos()
            for tile in self.tiles:
                if tile.rect.collidepoint(m_pos) and self.current_unit.can_move() and tile.sprite is not self.current_unit:
                    if not tile.sprite:
                        self.current_unit.rect.center = tile.rect.center
                        self.__switch_turn()
                    if tile.sprite and tile.sprite.color != self.current_unit.color:
                        tile.sprite.kill()
                        tile.sprite = None
                    self.__fill_tiles()
                    self.__count_neighbours()

    def __draw_points(self):
        if self.current_unit is not None:
            for tile in self.tiles:
                if not tile.sprite and tile.rect.center in self.current_unit.get_neighbours():
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

    def __count_neighbours(self):
        for first_unit in self.units_group:
            neighbours_count = 0
            for coord in first_unit.get_x_y_neighbours():
                for second_unit in self.units_group:
                    if second_unit.rect.collidepoint(coord) and first_unit.color == second_unit.color:
                        neighbours_count += 1
            first_unit.power = neighbours_count
            first_unit.update_power_image()

    def __count_power(self, unit):
        general_power = 0
        for unit in self.units_group:
            if unit.rect.center in self.current_unit.get_x_y_neighbours():
                general_power += self.__count_power(unit) - 1


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
