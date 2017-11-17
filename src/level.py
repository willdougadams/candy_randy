import pygame

class Level():
  def __init__(self, screen):
    self.grid = []
    self.offset = (0, 0)
    self.screen = screen
    self.tile_size = 16
    self.map_size = 100
    self.current_level = 1

    self.tiles = pygame.image.load("res/DawnLike/Floor.png").convert()

    tile_offsets = {}
    tile_offsets["top_left"]     = (0, 0)
    tile_offsets["top_center"]    = (1, 0)
    tile_offsets["top_right"]      = (2, 0)

    tile_offsets["left_wall"]     = (0, 1)
    tile_offsets["center"]        = (1, 1)
    tile_offsets["right_wall"]    = (2, 1)

    tile_offsets["bottom_left"]  = (0, 2)
    tile_offsets["bottom_center"] = (1, 2)
    tile_offsets["bottom_right"]   = (2, 2)

    tile_offsets["top_hallway"]    = (3, 0)
    tile_offsets["vert_hallway"]   = (3, 1)
    tile_offsets["bottom_hallway"] = (3, 2)

    tile_offsets["left_hallway"]  = (4, 1)
    tile_offsets["hori_hallway"]  = (5, 1)
    tile_offsets["right_hallway"] = (6, 1)

    tile_symbols = {}
    tile_symbols["{"] = "top_right"
    tile_symbols["-"] = "top_center"
    tile_symbols["}"] = "top_left"

    tile_symbols[";"] = "left_wall"
    tile_symbols["."] = "center"
    tile_symbols[":"] = "right_wall"

    tile_symbols["["] = "bottom_left"
    tile_symbols["_"] = "bottom_center"
    tile_symbols["]"] = "bottom_right"

    self.grid.append(list("{" + "-" * (self.map_size-2) + "}"))
    for i in range(self.map_size - 2):
      self.grid.append(list(";" + "." * (self.map_size-2) + ":"))
    self.grid.append(list("[" + "_" * (self.map_size-2) + "]"))

    tilemap_size = self.map_size * self.tile_size
    self.tilemap = pygame.surface.Surface((tilemap_size, tilemap_size))

    for y, row in enumerate(self.grid):
      for x, tile in enumerate(row):
        map_location = (x * self.tile_size, y * self.tile_size)
        tile_x = tile_offsets[tile_symbols[tile]][0]
        tile_y = tile_offsets[tile_symbols[tile]][1] + (self.tile_size * self.current_level * 3)
        tile_rect = (tile_x, tile_y, self.tile_size, self.tile_size)
        self.tilemap.blit(self.tiles, map_location, tile_rect)

  def update(self, new_offset):
    self.offset = new_offset

  def draw(self):
    w, h = self.screen.get_size()
    self.screen.blit(self.tilemap, (0, 0), (0, 0, w, h))
