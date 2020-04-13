import threading
import time


class Worker(threading.Thread):
    def __init__(self, x, y, name, surname, sprite_type):
        threading.Thread.__init__(self)
        self.name = name
        self.surname = surname
        self.sprite_type = sprite_type
        # self.current_sprite

    def daily_routine(self):
        pass

    def run(self):
        print(self.name, self.surname, " is ready to work!")
        self.daily_routine()
