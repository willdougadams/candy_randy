import pygame
import random
import generate_level

class Level():
  def __init__(self, screen):
    self.grid = []
    self.offset = (0, 0)
    self.screen = screen
    self.tile_size = 16
    self.map_size = 60
    self.current_level = 1
    self.current_world = 0
    self.floor_tile_symbols = ['.', '{', '}', '[', ']', ':', ';', '_', '-']

    self.floor_tilesheet = pygame.image.load("res/DawnLike/Floor.png").convert()
    self.wall_tilesheet = pygame.image.load("res/DawnLike/Wall.png").convert()

    floor_tile_offsets = {}

    floor_tile_offsets["top_left"]       = (0, 0)
    floor_tile_offsets["top_center"]     = (1, 0)
    floor_tile_offsets["top_right"]      = (2, 0)
    floor_tile_offsets["left_edge"]     = (0, 1)
    floor_tile_offsets["center"]        = (1, 1)
    floor_tile_offsets["right_edge"]    = (2, 1)
    floor_tile_offsets["bottom_left"]    = (0, 2)
    floor_tile_offsets["bottom_center"]  = (1, 2)
    floor_tile_offsets["bottom_right"]   = (2, 2)
    floor_tile_offsets["top_hallway"]    = (3, 0)
    floor_tile_offsets["vert_hallway"]   = (3, 1)
    floor_tile_offsets["bottom_hallway"] = (3, 2)
    floor_tile_offsets["left_hallway"]  = (4, 1)
    floor_tile_offsets["hori_hallway"]  = (5, 1)
    floor_tile_offsets["right_hallway"] = (6, 1)

    floor_tile_symbols = {}
    floor_tile_symbols["}"] = "top_right"
    floor_tile_symbols["-"] = "top_center"
    floor_tile_symbols["{"] = "top_left"
    floor_tile_symbols[";"] = "left_edge"
    floor_tile_symbols["."] = "center"
    floor_tile_symbols[":"] = "right_edge"
    floor_tile_symbols["["] = "bottom_left"
    floor_tile_symbols["_"] = "bottom_center"
    floor_tile_symbols["]"] = "bottom_right"
    self.floor_tile_symbols = floor_tile_symbols

    wall_tile_symbols = {}
    wall_tile_symbols['='] = "top_center"
    wall_tile_symbols['('] = "top_left"
    wall_tile_symbols[')'] = "top_right"
    wall_tile_symbols['|'] = 'left_edge'
    wall_tile_symbols['l'] = 'bottom_left'
    wall_tile_symbols['r'] = 'bottom_right'

    tilemap_size = self.map_size * self.tile_size
    self.tilemap = pygame.surface.Surface((tilemap_size, tilemap_size))

    self.grid = generate_level.generate(self.map_size)

    level_offset = (3 * self.tile_size * self.current_level)
    world_offset = (7 * self.tile_size * self.current_world)
    self.tilemap.fill((0, 0, 0))
    for y, row in enumerate(self.grid):
      for x, tile in enumerate(row):
        if not tile in floor_tile_symbols and not tile in wall_tile_symbols:
          continue
        tileset_x = 0
        tileset_y = 0
        if tile in floor_tile_symbols:
          tileset_x = floor_tile_offsets[floor_tile_symbols[tile]][0] * self.tile_size
          tileset_y = floor_tile_offsets[floor_tile_symbols[tile]][1] * self.tile_size
          tile_x = tileset_x + world_offset
          tile_y = tileset_y + level_offset
          map_location = (x * self.tile_size, y * self.tile_size)
          tile_rect = (tile_x, tile_y, self.tile_size, self.tile_size)
          self.tilemap.blit(self.floor_tilesheet, map_location, tile_rect)
        elif tile in wall_tile_symbols:
          if tile == '/':
            tile = '|'
            tileset_x = floor_tile_offsets[wall_tile_symbols[tile]][0] * self.tile_size
            tileset_y = floor_tile_offsets[wall_tile_symbols[tile]][1] * self.tile_size
            tile_x = tileset_x + world_offset
            tile_y = tileset_y + level_offset
            map_location = (x * self.tile_size, y * self.tile_size)
            tile_rect = (tile_x, tile_y, self.tile_size, self.tile_size)
            tile_surface = pygame.Surface((self.tile_size, self.tile_size))
            tile_surface.blit(self.wall_tilesheet, (0, 0), tile_rect)
            self.tilemap.blit(pygame.transform.flip(tile_surface, True, False), map_location, (0, 0, self.tile_size, self.tile_size))
          else:
            tileset_x = floor_tile_offsets[wall_tile_symbols[tile]][0] * self.tile_size
            tileset_y = floor_tile_offsets[wall_tile_symbols[tile]][1] * self.tile_size
            tile_x = tileset_x + world_offset
            tile_y = tileset_y + level_offset
            map_location = (x * self.tile_size, y * self.tile_size)
            tile_rect = (tile_x, tile_y, self.tile_size, self.tile_size)
            self.tilemap.blit(self.wall_tilesheet, map_location, tile_rect)

  def update(self, new_offset):
    self.offset = new_offset

  def draw(self):
    size = self.screen.get_size()
    self.screen.blit(self.tilemap, (0, 0), (0, 0, size[0], size[1]))

  def get_w(self):
    return self.tilemap.get_size()[0]

  def get_h(self):
    return self.tilemap.get_size()[1]
