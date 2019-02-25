import random
import pygame
import copy
import random

ROOM_BUFFER = 3

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
floor_tile_offsets["vert_hallway"]   = (1, 5)
floor_tile_offsets["bottom_hallway"] = (3, 2)
floor_tile_offsets["left_hallway"]  = (4, 1)
floor_tile_offsets["hori_hallway"]  = (1, 3)
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
floor_tile_symbols['h'] = 'hori_hallway'
floor_tile_symbols['v'] = 'vert_hallway'

wall_tile_symbols = {}
wall_tile_symbols['='] = "top_center"
wall_tile_symbols['('] = "top_left"
wall_tile_symbols[')'] = "top_right"
wall_tile_symbols['|'] = 'left_edge'
wall_tile_symbols['l'] = 'bottom_left'
wall_tile_symbols['r'] = 'bottom_right'

def print_room_to_grid(grid, room, r, c):
  for row in range(-ROOM_BUFFER, room.height+ROOM_BUFFER):
    for col in range(-ROOM_BUFFER, room.width+ROOM_BUFFER):
      grid[r+row][c+col] = 'B'

  for row in range(room.height-1):
    for col in range(room.width-1):
      grid[r+row][c+col] = '.'

  for row in range(room.height-1):
    grid[r+row][c-1] = '|'
    grid[r+row][c] = ';'
    grid[r+row][c+room.width-1] = '|'
    grid[r+row][c+room.width-2] = ':'

  for col in range(room.width-1):
    grid[r-1][c+col] = '='
    grid[r][c+col] = '-'
    grid[r+room.height-1][c+col] = '='
    grid[r+room.height-2][c+col] = '_'

  # top left corner
  grid[r-1][c-1] = '('
  grid[r][c] = '{'

  # bottom left corner
  grid[r-1][c+room.width-1] = ')'
  grid[r][c+room.width-2] = '}'

  # top right corner
  grid[r+room.height-1][c-1] = 'l'
  grid[r+room.height-2][c] = '['

  # bottom right corner
  grid[r+room.height-1][c+room.width-1] = 'r'
  grid[r+room.height-2][c+room.width-2] = ']'

  return grid

def spot_valid(grid, room, r, c):
  if r+room.height >= len(grid)-(ROOM_BUFFER*2) or c+room.width>=len(grid[0])-(ROOM_BUFFER*2):
    return False

  for i in range(r, r+room.height+ROOM_BUFFER):
    for j in range(c, c+room.width+ROOM_BUFFER):
      if not grid[i][j] == ' ':
        return False

  return True

def place_room(grid, room):
  visited = {}
  queue = [(len(grid)/2, len(grid[0])/2)]
  r = 0
  c = 0
  while queue:
    r, c = queue.pop(0)
    if spot_valid(grid, room, r, c):
      break

    visited[(r, c)] = True
    around = [
      (r-1, c-1),
      (r-1, c),
      (r-1, c+1),
      (r, c-1),
      (r, c+1),
      (r+1, c-1),
      (r+1, c),
      (r+1, c+1)
    ]

    around = filter(lambda x: all(i>=0 for i in x), around)

    for direction in around:
      if direction in visited:
        continue
      try:
        _ = grid[direction[0]][direction[1]]
        visited[direction] = True
        queue.append(direction)
      except IndexError:
        pass

  grid = print_room_to_grid(grid, room, r, c)
  return grid

def print_hallway_to_map(grid, spot, direction):
  floor_tile = 'h'
  if direction in set([(1, 0), (-1, 0)]):
    floor_tile = 'v'

  while grid[spot[0]][spot[1]] in floor_tile_symbols:
    spot = (spot[0]+direction[0], spot[1]+direction[1])

  while not grid[spot[0]][spot[1]] in floor_tile_symbols:
    grid[spot[0]][spot[1]] = floor_tile
    if floor_tile == 'v':
      grid[spot[0]][spot[1]-1] = '|'
      grid[spot[0]][spot[1]+1] = '|'
    else:
      grid[spot[0]+1][spot[1]] = '='
      grid[spot[0]-1][spot[1]] = '='
    spot = (spot[0]+direction[0], spot[1]+direction[1])

  return grid

def search_for_room(grid, r=None, c=None, start=None):
  visited = {}
  if r is None:
    r = random.randint(1, len(grid)-1)
  if c is None:
    c = random.randint(1, len(grid)-1)
  if start is not None:
    if start == 'random':
      r = random.randint(1, len(grid)-1)
      c = random.randint(1, len(grid)-1)
    elif start == 'center':
      r = len(grid)/2
      c = len(grid)/2
    else:
      raise Exception('Unrecognized start for search: '+str(start))
  queue = [(r, c)]
  while queue:
    spot = queue.pop(0)
    if grid[spot[0]][spot[1]] in floor_tile_symbols:
      return spot

    visited[spot] = True
    around = [
      (spot[0]-1, spot[1]-1),
      (spot[0]-1, spot[1]),
      (spot[0]-1, spot[1]+1),
      (spot[0], spot[1]-1),
      (spot[0], spot[1]+1),
      (spot[0]+1, spot[1]-1),
      (spot[0]+1, spot[1]),
      (spot[0]+1, spot[1]+1),
    ]

    around = filter(lambda x: not any(i<0 for i in x), around)

    for direction in around:
      if direction in visited:
        continue
      try:
        _ = grid[direction[0]][direction[1]]
        visited[direction] = True
        queue.append(direction)
      except IndexError:
        pass

def scout(grid, spot, direction):
  def increment_spot(spot):
    spot = (spot[0]+direction[0], spot[1]+direction[1])
    if any(s < 0 for s in [spot[0], spot[1]]) or spot[0] >= len(grid) or spot[1] >= len(grid[0]):
      return ()
    return spot

  good_to_go = False
  while spot and grid[spot[0]][spot[1]] in floor_tile_symbols:
    spot = increment_spot(spot)

  while spot and not grid[spot[0]][spot[1]] in floor_tile_symbols:
    spot = increment_spot(spot)

  if not spot:
      return False
  good_to_go = (grid[spot[0]][spot[1]] in floor_tile_symbols)

  return good_to_go

def add_hallway(grid):
  r, c = search_for_room(grid, start='random')
  unconnected = erase_space(copy.deepcopy(grid), r, c)

  r, c = search_for_room(unconnected, start='random')
  queue = [(r, c)]

  checked = {}
  while queue:
    spot = queue.pop() # ok fine its a stack
    checked[spot] = True

    for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
      if scout(grid, spot, direction):
        grid = print_hallway_to_map(grid, spot, direction)
        return grid

    neighbors = [(spot[0]-1, spot[1]), (spot[0]+1, spot[1]), (spot[0], spot[1]-1), (spot[0], spot[1]+1)]
    neighbors = filter(lambda x: x not in checked, neighbors)
    neighbors = filter(lambda x: x[0]>=0 and x[0]<len(grid) and x[1]>=0 and x[1]<len(grid[0]), neighbors)
    neighbors = filter(lambda x: grid[x[0]][x[1]] == '.', neighbors)
    for n in neighbors:
      queue.append(n)

  return grid

def erase_space(grid, r, c):
    queue = [(r, c)]
    visited = {}
    visited[(r, c)] = True

    while queue:
      r, c = queue.pop()
      grid[r][c] = ' '

      neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
      neighbors = [x for x in neighbors if not x in visited]
      neighbors = [x for x in neighbors if x[0]>=0 and x[0]<len(grid) and x[1]>=0 and x[1]<len(grid[0])]
      neighbors = [x for x in neighbors if grid[x[0]][x[1]] in floor_tile_symbols]
      for n in neighbors:
        visited[n] = True
        queue.append(n)

    return grid

def all_connected(grid):
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] in floor_tile_symbols:
        erased = erase_space(copy.deepcopy(grid), r, c)
        return not any(t in floor_tile_symbols for row in erased for t in row)

  raise Exception('Map has no floor')

