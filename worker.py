import threading
from pygame import transform
import time


class Worker(threading.Thread):

    def __init__(self, RESX, RESY, desk_x, desk_y, desk, name, surname, sprite_set, locks):
        threading.Thread.__init__(self)
        self.sprite_set = sprite_set
        # self._scale_sprites(RESX, RESY)
        self.desk_x = desk_x
        self.desk_y = desk_y
        self.desk = desk
        self.name = name
        self.surname = surname
        self.sprite_set = sprite_set
        self.locks = locks
        self.pos_x = desk_x
        self.pos_y = desk_y
        self.state = "working"
        self.current_sprite = self.sprite_set["back"]
        self.number = 999  # NEW

    def _scale_sprites(self, RESX, RESY):
        for key, sprite in self.sprite_set.items():
            sprite_width, sprite_height = sprite.get_size()
            sprite = transform.scale(sprite, (int(sprite_width * RESX / 1280), int(sprite_height * RESY / 800)))
            # self.sprite_set[key] = sprite
            sprite_width, sprite_height = sprite.get_size()

    def run(self):
        print(self.name, self.surname, " is ready to work!")
        self.daily_routine()
        print(self.name, self.surname, " ended his work day!")

    def daily_routine(self):
        self._work()
        self._copy_documents()
        self._place_documents()
        self._get_coffee()
        self._get_snack()
        self._work()
        self._copy_documents()
        self._place_documents()
        self._work()
        self.state = "done"
        self.desk.lock.release()
        self.desk.is_used = False

    def _work(self):
        self.state = "working"
        self.current_sprite = self.sprite_set["back"]
        self.pos_x = self.desk_x
        self.pos_y = self.desk_y
        time.sleep(5)

    def _get_coffee(self):
        self.state = "coffee_queue"
        self.current_sprite = self.sprite_set["profile-left"]
        self.locks["coffee_machine"].acquire()
        self.state = "coffee"
        self.current_sprite = self.sprite_set["back"]
        time.sleep(5)
        self.locks["coffee_machine"].release()

    def _get_snack(self):
        self.state = "snack_queue"
        self.current_sprite = self.sprite_set["profile-left"]
        self.locks["vending_machine"].acquire()
        self.state = "snack"
        self.current_sprite = self.sprite_set["back"]
        time.sleep(5)
        self.locks["vending_machine"].release()

    def _copy_documents(self):
        self.state = "copy_queue"
        self.current_sprite = self.sprite_set["profile-left"]
        run = True
        index = 999
        while run:
            from office_rooms import CopyRoom
            for copy in CopyRoom.copy_machines:
                if not copy.lock.locked():
                    index = CopyRoom.copy_machines.index(copy)
                    self.number = index
                    self.locks["copy_machine"+str(index)].acquire()
                    run = False
                    break
        self.state = "copy"
        self.current_sprite = self.sprite_set["back"]
        time.sleep(5)
        self.locks["copy_machine"+str(index)].release()  # - uwolnic loka z konkretnej kserokopiarki

    def _place_documents(self):
        self.state = "safe_queue"
        self.current_sprite = self.sprite_set["profile-left"]
        run = True
        index = 999
        while run:
            from office_rooms import Archives
            for safe in Archives.safes:
                if not safe.lock.locked():
                    index = Archives.safes.index(safe)
                    self.number = index
                    self.locks["safe" + str(index)].acquire()
                    run = False
                    break
        self.state = "placing_documents"
        self.current_sprite = self.sprite_set["back"]
        time.sleep(5)
        self.locks["safe" + str(index)].release()  # - uwolnic loka z konkretnej kserokopiarki
