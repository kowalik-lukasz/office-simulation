import pygame as pg
import exceptions
from worker import Worker
from desk_info import DeskInfo
from office_resources import CoffeeMachine
from office_resources import VendingMachine


class Room:

    def __init__(self, RESX, RESY, res_x, res_y):
        self.res_x = res_x
        self.res_y = res_y
        self.surface = pg.Surface((self.res_x, self.res_y))
        self.x = int(RESX / 2) - self.surface.get_width() // 2
        self.y = int(RESY / 2) - self.surface.get_height() // 2
        self.workers = []

    def blit_floor(self, floor_tile):
        pos_x = 0
        pos_y = 0
        while pos_y < self.res_y:
            while pos_x < self.res_x:
                self.surface.blit(floor_tile, (pos_x, pos_y))
                pos_x += 148
            pos_x = 0
            pos_y += 150

    def blit_object(self, sprite_x, sprite_y, sprite):
        sprite_width, sprite_height = sprite.get_size()
        # Ensuring that the object will not be printed outside of given surface AND that there will be some space
        # between marginal objects and the end of the surface (more specifically 1/4 of the object's height or width).
        if sprite_x < int(sprite_width / 4) or sprite_x > self.surface.get_width() - 3 * int(sprite_width / 4):
            raise exceptions.ObjectOutOfAcceptedXBoundsError
        elif sprite_y < int(sprite_height / 4) or sprite_y > self.surface.get_height() - 3 * int(sprite_height / 4):
            raise exceptions.ObjectOutOfAcceptedYBoundsError
        else:
            self.surface.blit(sprite, (sprite_x, sprite_y))

    def show_room(self, win):
        win.blit(self.surface, (self.x, self.y))

    def blit_workers(self):
        for worker in self.workers:
            self.blit_object(worker.x, worker.y, worker.current_sprite)


class MainRoom(Room):

    def __init__(self, RESX, RESY, res_x, res_y, desk_sprite):
        super().__init__(RESX, RESY, res_x, res_y)
        self.desk_sprite_width, self.desk_sprite_height = desk_sprite.get_size()
        self.desk_sprite = pg.transform.scale(desk_sprite, (int(self.desk_sprite_width * RESX / 1280), int(
            self.desk_sprite_height * RESY / 800)))
        self.desk_sprite_width, self.desk_sprite_height = self.desk_sprite.get_size()
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
                desk_x = int(self.desk_sprite_width / 2) + j * self.desk_sprite_width + j * int(
                    self.desk_sprite_width / 2)
                desk_y = int(self.desk_sprite_height / 2) + i * self.desk_sprite_height + i * int(
                    self.desk_sprite_height / 2)
                try:
                    self.blit_object(desk_x, desk_y, self.desk_sprite)
                except exceptions.ObjectOutOfAcceptedXBoundsError:
                    row_blitting = False
                except exceptions.ObjectOutOfAcceptedYBoundsError:
                    row_blitting = False
                    blitting = False
                else:
                    self.desks.append(DeskInfo(desk_x, desk_y))
                j += 1
            i += 1

    def deploy_new_worker(self, name, surname, sprite):
        worker = Worker(name, surname, sprite)
        worker.start()

        self.workers.append(worker)


class DiningRoom(Room):
    def __init__(self, RESX, RESY, res_x, res_y, coffee_machine_sprite, vending_machine_sprite):
        super().__init__(RESX, RESY, res_x, res_y)

        self.coffee_machine = CoffeeMachine(coffee_machine_sprite, int(RESX / 1280), int(RESY / 800))
        self.vending_machine = VendingMachine(vending_machine_sprite, int(RESX / 1280), int(RESY / 800))

    def blit_machines(self):
        pos_y = self.coffee_machine.sprite_height / 4 + 1
        pos_x = int(self.res_x / 2) - self.coffee_machine.sprite_width - int(self.coffee_machine.sprite_width / 20)
        self.blit_object(pos_x, pos_y, self.coffee_machine.sprite)
        pos_x = int(self.res_x / 2) + int(self.coffee_machine.sprite_width / 20)
        self.blit_object(pos_x, pos_y, self.vending_machine.sprite)
