import pygame as pg
import exceptions
import random
import queue
from worker import Worker
from office_resources import CoffeeMachine
from office_resources import VendingMachine
from office_resources import ComputerDesk


class Room:

    all_workers = []

    def __init__(self, RESX, RESY, res_x, res_y):
        self.res_x = res_x
        self.res_y = res_y
        self.surface = pg.Surface((self.res_x, self.res_y))
        self.x = int(RESX / 2) - self.surface.get_width() // 2
        self.y = int(RESY / 2) - self.surface.get_height() // 2

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

    def blit_workers(self, workers):
        for worker in workers:
            self.blit_object(worker.pos_x, worker.pos_y, worker.current_sprite)


class MainRoom(Room):

    def __init__(self, RESX, RESY, res_x, res_y, desk_sprite):
        super().__init__(RESX, RESY, res_x, res_y)
        self.desk_sprite_width, self.desk_sprite_height = desk_sprite.get_size()
        self.desk_sprite = pg.transform.scale(desk_sprite, (int(self.desk_sprite_width * RESX / 1280), int(
            self.desk_sprite_height * RESY / 800)))
        self.desk_sprite_width, self.desk_sprite_height = self.desk_sprite.get_size()
        self.desks = []
        self._init_desks()
        self.workers = []

    # Private method initializing all the computer desks in the main room. It is designed in a way so that there's
    # always 20 desks (max nr of available workers - threads at one time), no matter the resolution.
    def _init_desks(self):
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
                    self.desks.append(ComputerDesk(desk_x, desk_y, self.desk_sprite))
                j += 1
            i += 1

    def blit_desks(self):
        for desk in self.desks:
            self.blit_object(desk.x, desk.y, desk.sprite)

    def deploy_new_worker(self, RESX, RESY, name, surname, texture_dict, locks):
        # Generating random sprite seta
        sprite_set_key = random.randint(0, 4)
        sprite_set = texture_dict[sprite_set_key]

        # Might want to add random name generator in this method
        for desk in self.desks:
            if not desk.is_used:
                desk.lock.acquire()
                desk.is_used = True
                worker = Worker(RESX, RESY, desk.x, desk.y, desk, name, surname, sprite_set, locks)
                worker.start()
                self.workers.append(worker)
                super().all_workers.append(worker)
                return worker

    def update_workers(self):
        try:
            for worker in super().all_workers:
                if not worker.state == "working":
                    if worker in self.workers:
                        self.workers.remove(worker)
                else:
                    worker.pos_x = worker.desk_x
                    worker.pos_y = worker.desk_y
                    if worker not in self.workers:
                        self.workers.append(worker)
            super().blit_workers(self.workers)
        except AttributeError:
            return


class DiningRoom(Room):
    def __init__(self, RESX, RESY, res_x, res_y, coffee_machine_sprite, vending_machine_sprite):
        super().__init__(RESX, RESY, res_x, res_y)

        self.coffee_machine = CoffeeMachine(coffee_machine_sprite, RESX / 1280, RESY / 800, res_x)
        self.vending_machine = VendingMachine(vending_machine_sprite, RESX / 1280, RESY / 800, res_x)
        self.workers = []
        self.coffee_machine_queue = queue.Queue()
        self.vending_machine_queue = queue.Queue()

        # States that allow Worker objects to be stored in DiningRoom object. Those ending with "_response" indicate
        # that the object is waiting for info on where to be placed - directly next to the resource or in queue.
        self.acceptable_states = ["snack", "coffee", "snack_queue", "coffee_queue"]

    def blit_machines(self):
        self.blit_object(self.coffee_machine.x, self.coffee_machine.y, self.coffee_machine.sprite)
        self.blit_object(self.vending_machine.x, self.vending_machine.y, self.vending_machine.sprite)

    def get_locks(self):
        return {"coffee_machine": self.coffee_machine.lock, "vending_machine": self.vending_machine.lock}

    # Method updating workers' positions within dining room + removing those wo left the room from the workers list
    def update_workers(self):
        try:
            for worker in super().all_workers:
                if worker.state not in self.acceptable_states:
                    if worker in self.workers:
                        self.workers.remove(worker)
                # Setting up the blitting position of the worker
                else:
                    if worker.state == self.acceptable_states[0]:
                        worker.pos_x, worker.pos_y = self.vending_machine.x, self.vending_machine.y
                    elif worker.state == self.acceptable_states[1]:
                        worker.pos_x, worker.pos_y = self.coffee_machine.x, self.coffee_machine.y
                    elif worker.state == self.acceptable_states[2]:
                        worker.pos_x, worker.pos_y = self.vending_machine.x + self.vending_machine.sprite_width, \
                                                     self.vending_machine.y + self.vending_machine.sprite_height
                    elif worker.state == self.acceptable_states[3]:
                        worker.pos_x, worker.pos_y = self.coffee_machine.x - self.coffee_machine.sprite_width, \
                                                     self.coffee_machine.y + self.coffee_machine.sprite_height
                    if worker not in self.workers:
                        self.workers.append(worker)

            super().blit_workers(self.workers)
        except AttributeError:
            return
