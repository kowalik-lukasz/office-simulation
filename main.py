import pygame as pg
from office_rooms import MainRoom
from office_rooms import DiningRoom


def main():

    # Window setup - 1280:800 resolution is recommended
    RESX = 1280
    RESY = 800
    win = pg.display.set_mode((RESX, RESY))
    pg.display.set_caption("Office Sim")

    # View setup
    view = 1
    VIEWS = 2   # current amount of views

    # Loading the surroundings textures
    floor_tile_sprite = pg.image.load("textures/office-floor.png")
    desk_sprite = pg.image.load("textures/desk.png")
    coffee_machine_sprite = pg.image.load("textures/coffee-machine.png")
    vending_machine_sprite = pg.image.load("textures/vending-machine.png")

    # Loading the workers textures
    blond_back_sprite = pg.image.load("textures/blond-back.png")
    ginger_back_sprite = pg.image.load("textures/ginger-back.png")
    markus_back_sprite = pg.image.load("textures/markus-back.png")
    nerd_back_sprite = pg.image.load("textures/nerd-back.png")
    suit_back_sprite = pg.image.load("textures/suit-back.png")

    blond_profile_left_sprite = pg.image.load("textures/blond-profile-left.png")
    ginger_profile_left_sprite = pg.image.load("textures/ginger-profile-left.png")
    markus_profile_left_sprite = pg.image.load("textures/markus-profile-left.png")
    nerd_profile_left_sprite = pg.image.load("textures/nerd-profile-left.png")
    suit_profile_left_sprite = pg.image.load("textures/suit-profile-left.png")


    # Creating the office room objects
    main_room = MainRoom(RESX, RESY, int(RESX * 3 / 4), int(RESY * 3 / 4), desk_sprite)
    dining_room = DiningRoom(RESX, RESY, int(RESX * 3 / 4), int(RESY * 1 / 2), coffee_machine_sprite, vending_machine_sprite)

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

        # Displaying office views
        if view == 1:
            main_room.blit_floor(floor_tile_sprite)
            main_room.blit_desks()
            main_room.show_room(win)

        elif view == 2:
            dining_room.blit_floor(floor_tile_sprite)
            dining_room.blit_machines()
            dining_room.show_room(win)

        pg.display.update()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
