import pygame as pg


class Resource:

    def __init__(self, sprite):
        self.is_used = False
        self.sprite = sprite


class CoffeeMachine(Resource):

    def __init__(self, sprite, scale_x, scale_y):
        # Scaling the base img to the size that is potentially going to be changed according to resolution.
        self.sprite = pg.transform.rotozoom(sprite, 0, 0.45)
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.sprite = pg.transform.scale(self.sprite, (int(self.sprite_width * scale_x), int(self.sprite_height * scale_y)))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        super().__init__(self.sprite)


class VendingMachine(Resource):

    def __init__(self, sprite, scale_x, scale_y):
        # Scaling the base img to the size that is potentially going to be changed according to resolution.
        self.sprite = pg.transform.rotozoom(sprite, 0, 0.45)
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.sprite = pg.transform.scale(sprite, (int(self.sprite_width * scale_x), int(self.sprite_height * scale_y)))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        super().__init__(self.sprite)


class ComputerDesk(Resource):

    def __init__(self, sprite, scale_x, scale_y):
        # Scaling the base img to the size that is potentially going to be changed according to resolution.
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.sprite = pg.transform.scale(sprite, (int(self.sprite_width * scale_x), int(self.sprite_height * scale_y)))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        super().__init__(self.sprite)
