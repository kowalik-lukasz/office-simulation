import pygame as pg
import exceptions
from office_rooms import MainRoom
from desk_info import DeskInfo
import worker

# Creating the window resolution - 1280:800 is recommended
RESX = 1280
RESY = 800
win = pg.display.set_mode((RESX, RESY))
pg.display.set_caption("Office Sim")

# Loading the floor texture
floor_tile = pg.image.load("textures/office-floor.png")
floor_tile_width, floor_tile_height = floor_tile.get_size()

# Creating and calculating the working room surface according to the window's size
main_surface = pg.Surface((int(RESX * 3 / 4), int(RESY * 3 / 4)))
main_surface_x = int(RESX/2) - main_surface.get_width() // 2
main_surface_y = int(RESY/2) - main_surface.get_height() // 2

# Creating the dining room surface according to the window's size
dining_surface = pg.Surface((int(RESX * 3 / 4), int(RESY * 1 / 2)))
dining_surface_x = int(RESX/2) - dining_surface.get_width() // 2
dining_surface_y = int(RESY/2) - dining_surface.get_height() // 2


# Loading the computer desk texture
desk = pg.image.load("textures/desk.png")
desk_width, desk_height = desk.get_size()
desk = pg.transform.scale(desk, (int(desk_width * RESX/1280), int(desk_height * RESY/800)))
desk_width, desk_height = desk.get_size()
NUM_OF_DESKS = 20
desks = []

main_room = MainRoom(main_surface_x, main_surface_y, desk)

# Loading the coffee machine texture
coffee_machine = pg.image.load("textures/coffee-machine.png")
coffee_machine_width, coffee_machine_height = coffee_machine.get_size()
coffee_machine = pg.transform.rotozoom(coffee_machine, 0, 0.45)
# coffee_machine = pg.transform.scale(coffee_machine, (150, 150))
coffee_machine_width, coffee_machine_height = coffee_machine.get_size()

# Loading the coffee machine texture
vending_machine = pg.image.load("textures/vending-machine.png")
vending_machine_width, vending_machine_height = vending_machine.get_size()
vending_machine = pg.transform.rotozoom(vending_machine, 0, 0.45)
#vending_machine = pg.transform.scale(vending_machine, (150, 150))
vending_machine_width, vending_machine_height = vending_machine.get_size()


def blit_floor(res_x, res_y, surface):
    x = 0
    y = 0
    while y < res_y:
        while x < res_x:
            surface.blit(floor_tile, (x, y))
            x += 148
        x = 0
        y += 150


def blit_object(sprite_x, sprite_y, sprite, surface):

    sprite_width, sprite_height = sprite.get_size()

    # Ensuring that the object will not be printed outside of given surface AND that there will be some space
    # between marginal objects and the end of the surface.
    if sprite_x < int(sprite_width / 4) or sprite_x > surface.get_width() - 3 * int(sprite_width / 4):
        raise exceptions.ObjectOutOfAcceptedXBoundsError
    elif sprite_y < int(sprite_height / 4) or sprite_y > surface.get_height() - 3 * int(sprite_height / 4):
        raise exceptions.ObjectOutOfAcceptedYBoundsError
    else:
        surface.blit(sprite, (sprite_x, sprite_y))


# Method blitting all the computer desks in the main room. It is designed in a way so that there's always 20 desks
# (max nr of available workers - threads), no matter the resolution.
def blit_desks():
    blitting = True
    i = 0
    while blitting:
        row_blitting = True
        j = 0
        while row_blitting:
            desk_x = int(desk_width / 2) + j * desk_width + j * int(desk_width / 2)
            desk_y = int(desk_height / 2) + i * desk_height + i * int(desk_height / 2)
            try:
                blit_object(desk_x, desk_y, desk, main_surface)
            except exceptions.ObjectOutOfAcceptedXBoundsError:
                row_blitting = False
            except exceptions.ObjectOutOfAcceptedYBoundsError:
                row_blitting = False
                blitting = False
            else:
                desks.append(DeskInfo(desk_x, desk_y))
            j += 1
        i += 1


def main():

    # Game loop
    run = True
    while run:
        pg.time.delay(100)
        win.fill((0, 0, 0))

        blit_floor(main_surface.get_width(), main_surface.get_height(), main_surface)
        blit_floor(dining_surface.get_width(), dining_surface.get_width(), dining_surface)


        blit_desks()

        blit_object(400, 30, coffee_machine, dining_surface)
        blit_object(600, 30, vending_machine, dining_surface)

        # win.blit(main_surface, (main_surface_x, main_surface_y))
        win.blit(dining_surface, (dining_surface_x, dining_surface_y))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()
        # Key input handling section
        # if keys[pg.K_LEFT]:
            # x -= vel

        pg.display.update()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
