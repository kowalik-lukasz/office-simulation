import pygame as pg
import exceptions
import random
import queue
from worker import Worker
from office_resources import CoffeeMachine, Safe
from office_resources import VendingMachine
from office_resources import ComputerDesk
from office_resources import CopyMachine


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


class CopyRoom(Room):
    copy_machines = []

    def __init__(self, RESX, RESY, res_x, res_y, copy_machine_sprite):
        super().__init__(RESX, RESY, res_x, res_y)
        # self.copy_machine = CopyMachine(copy_machine_sprite, RESX / 2180, RESY / 1700, res_x)

        self.sprite_width, self.sprite_height = copy_machine_sprite.get_size()
        self.sprite = pg.transform.scale(copy_machine_sprite, (int(self.sprite_width * RESX / 6180),
                                                               int(self.sprite_height * RESY / 5500)))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        # self.busy = False
        # self.copy_machines = []
        self._init_copy_machines()
        self.workers = []
        self.copy_machine_queue = queue.Queue

        # States that allow Worker objects to be stored in CopyRoom object. Those ending with "_response" indicate
        # that the object is waiting for info on where to be placed - directly next to the resource or in queue.
        self.acceptable_states = ["copy", "copy_queue"]

    def _init_copy_machines(self):
        blitting = True
        i = 0
        while blitting:
            row_blitting = True
            j = 0
            while row_blitting:
                copy_x = int(self.sprite_width / 2) + j * self.sprite_width * 1.5 + j * int(
                    self.sprite_width / 2)
                copy_y = int(self.sprite_height / 2) + i * self.sprite_height * 1.3 + i * int(
                    self.sprite_height / 2)
                try:
                    self.blit_object(copy_x, copy_y, self.sprite)
                except exceptions.ObjectOutOfAcceptedXBoundsError:
                    row_blitting = False
                except exceptions.ObjectOutOfAcceptedYBoundsError:
                    row_blitting = False
                    blitting = False
                else:
                    self.copy_machines.append(CopyMachine(copy_x, copy_y, self.sprite))
                j += 1
                if j == 3:
                    row_blitting = False
            i += 1
            if i == 2:
                blitting = False

    def blit_machines(self):
        # self.blit_object(self.copy_machine.x, self.copy_machine.y, self.copy_machine.sprite)
        for copy_machine in self.copy_machines:
            self.blit_object(copy_machine.x, copy_machine.y, copy_machine.sprite)

    def get_locks(self, index):
        index = index
        copy_machine = self.copy_machines[index]
        return {"copy_machine" + str(index): copy_machine.lock}

    def update_workers(self):
        try:
            for worker in super().all_workers:
                if worker.state not in self.acceptable_states:
                    if worker in self.workers:
                        self.workers.remove(worker)
                # Setting up the blitting position of the worker
                else:
                    if worker.state == self.acceptable_states[0]:
                        worker.pos_x, worker.pos_y = self.copy_machines[worker.number].x, \
                                                     self.copy_machines[worker.number].y
                    elif worker.state == self.acceptable_states[1]:
                        worker.pos_x, worker.pos_y = self.copy_machines[5].x + \
                                                     self.copy_machines[5].sprite_width * 1.5, \
                                                     self.copy_machines[5].y + \
                                                     self.copy_machines[5].sprite_height * 1.5 * 5
                    if worker not in self.workers:
                        self.workers.append(worker)

            super().blit_workers(self.workers)
        except AttributeError:
            return


class Archives(Room):
    safes = []

    def __init__(self, RESX, RESY, res_x, res_y, safe_sprite):
        super().__init__(RESX, RESY, res_x, res_y)

        self.sprite_width, self.sprite_height = safe_sprite.get_size()
        self.sprite = pg.transform.scale(safe_sprite, (int(self.sprite_width * RESX / 6180),
                                                       int(self.sprite_height * RESY / 4500)))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self._init_safes()
        self.workers = []
        self.safe_queue = queue.Queue

        self.acceptable_states = ["placing_documents", "safe_queue"]

    def _init_safes(self):
        blitting = True
        i = 0
        while blitting:
            row_blitting = True
            j = 0
            while row_blitting:
                safe_x = int(self.sprite_width / 2) + j * self.sprite_width * 1.5 + j * int(
                    self.sprite_width / 2)
                safe_y = int(self.sprite_height / 2) + i * self.sprite_height * 2 + i * int(
                    self.sprite_height / 2)
                try:
                    self.blit_object(safe_x, safe_y, self.sprite)
                except exceptions.ObjectOutOfAcceptedXBoundsError:
                    row_blitting = False
                except exceptions.ObjectOutOfAcceptedYBoundsError:
                    row_blitting = False
                    blitting = False
                else:
                    self.safes.append(Safe(safe_x, safe_y, self.sprite))
                j += 1
                if j == 3:
                    row_blitting = False
            i += 1
            if i == 3:
                blitting = False

    def blit_machines(self):
        # self.blit_object(self.copy_machine.x, self.copy_machine.y, self.copy_machine.sprite)
        for safe in self.safes:
            self.blit_object(safe.x, safe.y, safe.sprite)

    def get_locks(self, index):
        index = index
        safe = self.safes[index]
        return {"safe" + str(index): safe.lock}

    def update_workers(self):
        try:
            for worker in super().all_workers:
                if worker.state not in self.acceptable_states:
                    if worker in self.workers:
                        self.workers.remove(worker)
                # Setting up the blitting position of the worker
                else:
                    if worker.state == self.acceptable_states[0]:
                        worker.pos_x, worker.pos_y = self.safes[worker.number].x, self.safes[worker.number].y
                    elif worker.state == self.acceptable_states[1]:
                        worker.pos_x, worker.pos_y = self.safes[2].x + \
                                                     self.safes[2].sprite_width * 2, \
                                                     self.safes[2].y + \
                                                     self.safes[2].sprite_height * 2
                    if worker not in self.workers:
                        self.workers.append(worker)

            super().blit_workers(self.workers)
        except AttributeError:
            return
