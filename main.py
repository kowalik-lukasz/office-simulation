import pygame as pg
from office_rooms import MainRoom, Archives
from office_rooms import DiningRoom
from office_rooms import CopyRoom


def main():

    # Window setup - 1280:800 resolution is recommended
    RESX = 800
    RESY = 600
    win = pg.display.set_mode((RESX, RESY))
    pg.display.set_caption("Office Sim")

    # View setup
    view = 1
    VIEWS = 4  # current amount of views    #changed!

    # Loading the surroundings textures
    floor_tile_sprite = pg.image.load("textures/office-floor.png")
    desk_sprite = pg.image.load("textures/desk.png")
    coffee_machine_sprite = pg.image.load("textures/coffee-machine.png")
    vending_machine_sprite = pg.image.load("textures/vending-machine.png")
    copy_machine_sprite = pg.image.load("textures/printer.png")
    safe_sprite = pg.image.load("textures/safe.png")

    # Making a dict in order to store keys to all worker texture packs
    texture_dict = {
        0: "blond",
        1: "ginger",
        2: "markus",
        3: "nerd",
        4: "suit"
    }

    # Loading the worker textures
    worker_textures_dir = "textures/"
    worker_textures_dict = {}
    for k, text in texture_dict.items():
        nested_dict = {"back": pg.image.load(worker_textures_dir + text + "-back.png"),
                       "profile-left": pg.image.load(worker_textures_dir + text + "-profile-left.png")}
        for key, texture in nested_dict.items():
            sprite_width, sprite_height = texture.get_size()
            nested_dict[key] = pg.transform.scale(texture, (int(sprite_width * RESX / 1280),
                                                            int(sprite_height * RESY / 800)))
        worker_textures_dict[k] = nested_dict

    # Creating the office room objects
    main_room = MainRoom(RESX, RESY, int(RESX * 3 / 4), int(RESY * 3 / 4), desk_sprite)
    dining_room = DiningRoom(RESX, RESY, int(RESX * 3 / 4), int(RESY * 1 / 2), coffee_machine_sprite,
                             vending_machine_sprite)
    copy_room = CopyRoom(RESX, RESY, int(RESX * 3 / 4), int(RESY * 3 / 5), copy_machine_sprite)
    archives = Archives(RESX, RESY, int(RESX * 3 / 4), int(RESY * 3 / 5), safe_sprite)

    # Game loop
    run = True
    while run:
        pg.time.delay(100)
        win.fill((0, 0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()
        # Key input handling section
        if keys[pg.K_LEFT]:
            if view > 1:
                view -= 1
        elif keys[pg.K_RIGHT]:
            if view < VIEWS:
                view += 1
        elif keys[pg.K_a]:
            locks = {}
            locks.update(dining_room.get_locks())
            locks.update(copy_room.get_locks())     # NEW
            main_room.deploy_new_worker(RESX, RESY, "Sample", "Worker", worker_textures_dict, locks)

        # Displaying office views
        if view == 1:
            main_room.blit_floor(floor_tile_sprite)
            main_room.blit_desks()
            main_room.update_workers()
            main_room.show_room(win)

        elif view == 2:
            dining_room.blit_floor(floor_tile_sprite)
            dining_room.blit_machines()
            dining_room.update_workers()
            dining_room.show_room(win)

        elif view == 3:
            copy_room.blit_floor(floor_tile_sprite)
            copy_room.blit_machines()
            # copy_room.update_workers()
            copy_room.show_room(win)

        elif view == 4:
            archives.blit_floor(floor_tile_sprite)
            archives.blit_machines()
            # archives.update_workers()
            archives.show_room(win)

        pg.display.update()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
