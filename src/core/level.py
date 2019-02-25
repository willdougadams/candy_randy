import pygame
import heapq
import random
import logging
from generate_level import *

from core.util import colors

class Level():
  def __init__(self, level, world):
    self.grid = []
    self.path_weight_grid = []
    self.grid_generated = False
    self.rooms_amt = 10
    self.components_generated = 0
    self.components_total = self.rooms_amt
    self.offset = (0, 0)
    self.tile_size = 16
    self.map_size = 60
    self.current_level = level
    self.current_world = world
    self.h_cost_lookup = {}
    self.h_costs = [[0]*self.map_size for _ in range(self.map_size)]

    self.floor_tilesheet = pygame.image.load("res/DawnLike/Floor.png").convert()
    self.wall_tilesheet = pygame.image.load("res/DawnLike/Wall.png").convert()

    self.floor_tile_offsets = floor_tile_offsets
    self.floor_tile_symbols = floor_tile_symbols
    self.wall_tile_symbols = wall_tile_symbols

    self.tilemap_size = self.map_size * self.tile_size
    self.tilemap = pygame.surface.Surface((self.tilemap_size, self.tilemap_size))
    self.obscured_tilemap = None

  def generate_grid(self):
    grid = [[" "]*self.map_size for _ in range(self.map_size)]
    self.grid = grid

    room_min_size = 3
    room_max_size = 8
    rooms = [pygame.Rect(0, 0, random.randint(room_min_size, room_max_size), random.randint(room_min_size, room_max_size)) for _ in range(self.rooms_amt)]

    for room in rooms:
      grid = place_room(grid, room)
      self.components_generated += 1

    while not all_connected(grid):
      last_grid = grid[:]
      grid = add_hallway(grid)
      if not grid == last_grid:
        self.components_generated += 1

    #grid = apply_walls(grid)

    self.grid = grid

    level_offset = (3 * self.tile_size * self.current_level)
    world_offset = (7 * self.tile_size * self.current_world)
    self.tilemap.fill((0, 0, 0))
    for y, row in enumerate(self.grid):
      for x, tile in enumerate(row):
        if not tile in self.floor_tile_symbols and not tile in self.wall_tile_symbols:
          continue
        tileset_x = 0
        tileset_y = 0
        if tile in self.floor_tile_symbols:
          tileset_x = self.floor_tile_offsets[self.floor_tile_symbols[tile]][1] * self.tile_size
          tileset_y = self.floor_tile_offsets[self.floor_tile_symbols[tile]][0] * self.tile_size
          tile_x = tileset_x + world_offset
          tile_y = tileset_y + level_offset
          map_location = self.surf_to_tile((y, x))#(x * self.tile_size, y * self.tile_size)
          tile_rect = (tile_x, tile_y, self.tile_size, self.tile_size)
          self.tilemap.blit(self.floor_tilesheet, map_location, tile_rect)
        elif tile in self.wall_tile_symbols:
          if tile == '/':
            tile = '|'
            tileset_x = self.floor_tile_offsets[self.wall_tile_symbols[tile]][1] * self.tile_size
            tileset_y = self.floor_tile_offsets[self.wall_tile_symbols[tile]][0] * self.tile_size
            tile_x = tileset_x + world_offset
            tile_y = tileset_y + level_offset
            map_location = self.surf_to_tile((y, x))#(x * self.tile_size, y * self.tile_size)
            tile_rect = (tile_x, tile_y, self.tile_size, self.tile_size)
            tile_surface = pygame.Surface((self.tile_size, self.tile_size))
            tile_surface.blit(self.wall_tilesheet, (0, 0), tile_rect)
            self.tilemap.blit(pygame.transform.flip(tile_surface, True, False), map_location, (0, 0, self.tile_size, self.tile_size))
          else:
            tileset_x = self.floor_tile_offsets[self.wall_tile_symbols[tile]][1] * self.tile_size
            tileset_y = self.floor_tile_offsets[self.wall_tile_symbols[tile]][0] * self.tile_size
            tile_x = tileset_x + world_offset
            tile_y = tileset_y + level_offset
            map_location = self.surf_to_tile((y, x))#(x * self.tile_size, y * self.tile_size)
            tile_rect = (tile_x, tile_y, self.tile_size, self.tile_size)
            self.tilemap.blit(self.wall_tilesheet, map_location, tile_rect)

    if logging.getLogger().getEffectiveLevel() ==logging.debug:
      for i in range(len(self.grid)):
        for j in range(len(self.grid[i])):
          r = pygame.Rect(i*self.tile_size, j*self.tile_size, self.tile_size, self.tile_size)
          pygame.draw.rect(self.tilemap, colors.PINK, r, 1)

    for i, row in enumerate(self.grid):
      for j, cell in enumerate(row):
        if grid[i][j] in self.floor_tile_symbols:
          h = self.manhattan_cost((i, j))
          self.h_cost_lookup[(i, j)] = h

    self.obscured_tilemap = self.tilemap.copy()
    self.obscured_tilemap.set_alpha(156)

    self.grid_generated = True

  def update(self, new_offset):
    self.offset = new_offset

  def draw(self, screen, visible):
    size = screen.get_size()
    screen.blit(self.obscured_tilemap, (0, 0), (0, 0, size[0], size[1]))

    for t in visible:
      x, y = self.surf_to_tile(t)
      screen.blit(self.tilemap, (x, y), (x, y, self.tile_size, self.tile_size))

  def highlight_tile(self, screen, location):
    w, h = screen.get_size()
    tile_x, tile_y = self.surf_to_tile(location)
    pygame.draw.rect(
                      screen,
                      colors.PINK,
                      pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size),
                      2
                    )

  def get_w(self):
    return self.tilemap.get_size()[0]

  def get_h(self):
    return self.tilemap.get_size()[1]

  def get_progress(self):
    return min(0.99, self.components_generated / float(self.components_total))

  def surf_to_tile(self, spot):
    return spot[0]*self.tile_size, spot[1]*self.tile_size

  def surf_to_grid(self, spot):
    """ returns the top right coner or center of the tile this spot is in """
    return int(spot[0])/self.tile_size, int(spot[1])/self.tile_size

  def grid_to_surf(self, spot):
    """ returns the surface location in the middle of the tile """
    return (spot[0]*self.tile_size)+self.tile_size/2, (spot[1]*self.tile_size)+self.tile_size/2
  

  def manhattan_cost(self, start_pos):
    logging.debug("generating manhatten cost for {0}".format(start_pos))
    start_row, start_col = start_pos
    start_cost = 0
    start = ((start_row, start_col), start_cost)
    visited = set()
    visited.add((start_row, start_col))  
    queue = [start]
    costs = [[0]*len(self.grid) for _ in range(len(self.grid[0]))]

    while queue:
      (row, col), cost = queue.pop(0)
      row, col = int(row), int(col)
      costs[row][col] = cost

      neighbors = [
        ((row+1, col), cost+10),
        ((row-1, col), cost+10),
        ((row, col+1), cost+10),
        ((row, col-1), cost+10),

        ((row+1, col+1), cost+14),
        ((row+1, col-1), cost+14),
        ((row-1, col+1), cost+14),
        ((row-1, col-1), cost+14)
      ]

      neighbors = filter(lambda x: x[0][0]>=0 and x[0][1]>=0, neighbors)
      neighbors = filter(lambda x: x[0][0]<len(self.grid) and x[0][1]<len(self.grid[0]), neighbors)
      neighbors = filter(lambda x: x[0] not in visited, neighbors)
      for n in neighbors:
        visited.add(n[0])
        queue.append(n)

    return costs

  def regenerate_h_costs(self, pc_pos):
    logging.debug('Regenerating H costs for manhattan...')
    #self.h_costs = self.manhattan_cost(pc_pos)
    self.h_costs = self.h_cost_lookup[(pc_pos[0], pc_pos[1])]

  def get_path(self, surf_start, surf_end):
    start = self.surf_to_grid(surf_start)
    end = self.surf_to_grid(surf_end)
    logging.debug('calculating path from {0} to {1}...'.format(start, end))
    # A* directly ripped off from rosetta code
    g_cost = {}
    f_cost = {}
    g_cost[start] = 0
    f_cost[start] = self.h_costs[start[0]][start[1]]

    visited = set()
    queue = set([start])
    came_from = {}

    while queue:
      spot = None
      node_f = None
      for q in queue:
        if spot is None or f_cost[q] < node_f:
          node_f = f_cost[q]
          spot = q

      if spot == end:
        path = [surf_end]
        while not spot == start:
          spot = came_from[spot]
          path.append(self.grid_to_surf(spot))
        path.append(self.grid_to_surf(spot))

        return path[::-1]

      queue.remove(spot)
      visited.add(spot)

      r, c = spot
      neighbors = [
        (r+1, c),
        (r-1, c),
        (r, c+1),
        (r, c-1),

        (r+1, c-1),
        (r-1, c-1),
        (r+1, c+1),
        (r-1, c+1)
      ]

      neighbors = filter(lambda x: all(i>=0 for i in x), neighbors)
      neighbors = filter(lambda x: all(i<len(self.grid) for i in x), neighbors)
      neighbors = filter(lambda x: self.grid[x[0]][x[1]] in self.floor_tile_symbols, neighbors)

      for n in neighbors:
        if n in visited:
          continue
        move_cost = 10 if abs(spot[0]-n[0])+abs(spot[1]-n[1])==1 else 14
        g = g_cost[spot] + move_cost

        if n not in queue:
          queue.add(n)
        elif g >= g_cost[n]:
          continue

        came_from[n] = spot
        g_cost[n] = g
        h = self.h_costs[n[0]][n[1]]
        f_cost[n] = g + h

    return []#raise RuntimeError('A* failed to find path :(')

  def get_fov(self, location, orientation, dist=6):
    if dist <= 0:
      return []

    fov = [location]
    orientation_offsets = {
      0: [(-1,  1), ( 0,  1), ( 1,  1)],
      1: [(-1, -1), (-1,  0), (-1,  1)],
      2: [( 1, -1), ( 1,  0), ( 1,  1)],
      3: [(-1, -1), ( 0, -1), ( 1, -1)]
    }

    for o in orientation_offsets[orientation]:
      neighb = location[0]+o[0], location[1]+o[1]

      if self.grid[neighb[0]][neighb[1]] in self.floor_tile_symbols:
        fov.extend(self.get_fov(neighb, orientation, dist-1))
      fov.append(neighb)

    return list(set(fov))








