import pygame as pg
import exceptions
from desk_info import DeskInfo


class Room:

    def __init__(self, res_x, res_y):
        self.res_x = res_x
        self.res_y = res_y
        self.surface = pg.Surface(self.res_x, self.res_y)
        self.x = int(self.res_x / 2) - self.surface.get_width() // 2
        self.y = int(self.res_y / 2) - self.surface.get_height() // 2

    def blit_floor(self, surface, floor_tile):
        x = 0
        y = 0
        while y < self.res_y:
            while x < self.res_x:
                surface.blit(floor_tile, (x, y))
                x += 148
            x = 0
            y += 150

    def blit_object(self, sprite_x, sprite_y, sprite):
        sprite_width, sprite_height = sprite.get_size()
        # Ensuring that the object will not be printed outside of given surface AND that there will be some space
        # between marginal objects and the end of the surface.
        if sprite_x < int(sprite_width / 4) or sprite_x > self.surface.get_width() - 3 * int(sprite_width / 4):
            raise exceptions.ObjectOutOfAcceptedXBoundsError
        elif sprite_y < int(sprite_height / 4) or sprite_y > self.surface.get_height() - 3 * int(sprite_height / 4):
            raise exceptions.ObjectOutOfAcceptedYBoundsError
        else:
            self.surface.blit(sprite, (sprite_x, sprite_y))


class MainRoom(Room):

    def __init__(self, res_x, res_y, desk):
        super().__init__(res_x, res_y)
        self.desk = desk
        self.desk_width, self.desk_height = self.desk.get_size()
        self.desks = []

    # Method blitting all the computer desks in the main room. It is designed in a way so that there's always 20 desks
    # (max nr of available workers - threads), no matter the resolution.
    def blit_desks(self):
        blitting = True
        i = 0
        while blitting:
            row_blitting = True
            j = 0
            while row_blitting:
                desk_x = int(self.desk_width / 2) + j * self.desk_width + j * int(self.desk_width / 2)
                desk_y = int(self.desk_height / 2) + i * self.desk_height + i * int(self.desk_height / 2)
                try:
                    self.blit_object(desk_x, desk_y, self.desk)
                except exceptions.ObjectOutOfAcceptedXBoundsError:
                    row_blitting = False
                except exceptions.ObjectOutOfAcceptedYBoundsError:
                    row_blitting = False
                    blitting = False
                else:
                    self.desks.append(DeskInfo(desk_x, desk_y))
                j += 1
            i += 1


class DiningRoom(Room):
    pass
