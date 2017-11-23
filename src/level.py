import pygame
import random
import generate_level

class Level():
  def __init__(self, screen):
    self.grid = []
    self.offset = (0, 0)
    self.screen = screen
    self.tile_size = 16
    self.map_size = 100
    self.current_level = 1

    self.floor_tilesheet = pygame.image.load("res/DawnLike/Floor.png").convert()
    self.wall_tilesheet = pygame.image.load("res/DawnLike/Wall.png").convert()

    floor_tile_offsets = {}
    floor_tile_offsets["top_left"]     = (0, 0)
    floor_tile_offsets["top_center"]    = (1, 0)
    floor_tile_offsets["top_right"]      = (2, 0)

    floor_tile_offsets["left_wall"]     = (0, 1)
    floor_tile_offsets["center"]        = (1, 1)
    floor_tile_offsets["right_wall"]    = (2, 1)

    floor_tile_offsets["bottom_left"]  = (0, 2)
    floor_tile_offsets["bottom_center"] = (1, 2)
    floor_tile_offsets["bottom_right"]   = (2, 2)

    floor_tile_offsets["top_hallway"]    = (3, 0)
    floor_tile_offsets["vert_hallway"]   = (3, 1)
    floor_tile_offsets["bottom_hallway"] = (3, 2)

    floor_tile_offsets["left_hallway"]  = (4, 1)
    floor_tile_offsets["hori_hallway"]  = (5, 1)
    floor_tile_offsets["right_hallway"] = (6, 1)

    floor_tile_symbols = {}
    floor_tile_symbols["{"] = "top_right"
    floor_tile_symbols["-"] = "top_center"
    floor_tile_symbols["}"] = "top_left"

    floor_tile_symbols[";"] = "left_wall"
    floor_tile_symbols["."] = "center"
    floor_tile_symbols[":"] = "right_wall"

    floor_tile_symbols["["] = "bottom_left"
    floor_tile_symbols["_"] = "bottom_center"
    floor_tile_symbols["]"] = "bottom_right"

    tilemap_size = self.map_size * self.tile_size
    self.tilemap = pygame.surface.Surface((tilemap_size, tilemap_size))

    self.grid = generate_level.generate(self.map_size)

    self.tilemap.fill((0, 0, 0))
    for y, row in enumerate(self.grid):
      for x, tile in enumerate(row):
        if not tile in floor_tile_symbols:
          continue
        map_location = (x * self.tile_size, y * self.tile_size)
        tile_x = floor_tile_offsets[floor_tile_symbols[tile]][0]
        tile_y = floor_tile_offsets[floor_tile_symbols[tile]][1] + (self.tile_size * self.current_level * 3)
        tile_rect = (tile_x, tile_y, self.tile_size, self.tile_size)
        self.tilemap.blit(self.floor_tilesheet, map_location, tile_rect)

  def update(self, new_offset):
    self.offset = new_offset

  def draw(self):
    size = self.tilemap.get_size()
    self.screen.blit(self.tilemap, (0, 0), (0, 0, size[0], size[1]))

  def get_w(self):
    return self.tilemap.get_size()[0]

  def get_h(self):
    return self.tilemap.get_size()[1]
