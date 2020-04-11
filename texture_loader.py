def load_textures():
    # Loading the floor texture and calculating the surface according to the window's size
    floor_tile = pg.image.load("textures/office-floor.png")
    floor_width, floor_height = floor_tile.get_size()
    floor_surface = pg.Surface((int(RESX * 3 / 4), int(RESY * 3 / 4)))
    floor_x = int(RESX / 2) - floor_surface.get_width() // 2
    floor_y = int(RESY / 2) - floor_surface.get_height() // 2

    # Loading the computer desk texture
    desk = pg.image.load("textures/computer-desk.png")
    desk_width, desk_height = desk.get_size()