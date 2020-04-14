import pygame as pg
import threading


class Resource:

    def __init__(self, sprite, x, y):
        self.is_used = False
        self.sprite = sprite
        self.lock = threading.Lock()
        self.x = x
        self.y = y


class CoffeeMachine(Resource):

    def __init__(self, sprite, scale_x, scale_y, res_x):
        # Scaling the base img to the size that is potentially going to be changed according to resolution.
        self.sprite = pg.transform.rotozoom(sprite, 0, 0.45)
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.sprite = pg.transform.scale(self.sprite, (int(self.sprite_width * scale_x),
                                                       int(self.sprite_height * scale_y)))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        y = self.sprite_height / 4 + 1
        x = int(res_x / 2) - self.sprite_width - int(self.sprite_width / 20)
        super().__init__(self.sprite, x, y)


class VendingMachine(Resource):

    def __init__(self, sprite, scale_x, scale_y, res_x):
        # Scaling the base img to the size that is potentially going to be changed according to resolution.
        self.sprite = pg.transform.rotozoom(sprite, 0, 0.45)
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.sprite = pg.transform.scale(self.sprite, (int(self.sprite_width * scale_x),
                                                       int(self.sprite_height * scale_y)))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        y = self.sprite_height / 4 + 1
        x = int(res_x / 2) + int(self.sprite_width / 20)
        super().__init__(self.sprite, x, y)


# Desks serve as a default position for new workers and furthermore cannot be shared between workers. The only way to
# obtain staffed desk is for the current worker thread to end.
class ComputerDesk(Resource):

    def __init__(self, x, y, sprite):
        super().__init__(sprite, x, y)
