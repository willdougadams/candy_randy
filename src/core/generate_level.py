import random
import pygame
import copy

ROOM_BUFFER = 3

def print_room_to_grid(grid, room, r, c):
  for row in range(room.height+ROOM_BUFFER):
    for col in range(room.width+ROOM_BUFFER):
      # 'B' does not corresond to a tile, provides buffer
      grid[r+row][c+col] = 'B'

  for row in range(room.height-1):
    for col in range(room.width-1):
      grid[r+row][c+col] = '.'

  for i in range(1, room.width):
    grid[r][c+i] = '='
    grid[r+1][c+i] = '-'
    grid[r+room.height-1][c+i] = '='
    grid[r+room.height-2][c+i] = '_'

  for i in range(1, room.height-1):
    grid[r+i][c] = '|'
    grid[r+i][c+1] = ';'
    grid[r+i][c+room.width-1] = '|'
    grid[r+i][c+room.width-2] = ':'

  grid[r][c] = '('
  grid[r+1][c+1] = '{'
  grid[r][c+room.width-1] = ')'
  grid[r+1][c+room.width-2] = '}'
  
  grid[r+room.height-1][c] = 'l'
  grid[r+room.height-2][c+1] = '['
  grid[r+room.height-1][c+room.width-1] = 'r'
  grid[r+room.height-2][c+room.width-2] = ']'

  return grid

def spot_valid(grid, room, r, c):
  valid = True
  if r+room.height >= len(grid) - ROOM_BUFFER or c+room.width>=len(grid[0]) - ROOM_BUFFER:
    return False

  for i in range(r, r+room.height+ROOM_BUFFER):
    for j in range(c, c+room.width+ROOM_BUFFER):
      if not grid[i][j] == ' ':
        valid = False
        break

  return valid

def place_room(grid, room):
  for r in range(len(grid)):
    for c in range(len(grid)):
      if spot_valid(grid, room, r, c):
        print 'Placing room...'
        grid = print_room_to_grid(grid, room, r, c)
        return grid

  return grid

def print_hallway_to_map(grid, spot, direction):
  grid[spot[0]][spot[1]] = '.'
  grid[spot[0]-direction[1]][spot[1]-direction[0]] = '.'
  grid[spot[0]+direction[1]][spot[1]+direction[0]] = '.'

  step = (spot[0]+direction[0], spot[1]+direction[1])
  if (step[0]<len(grid) and step[0]>=0) and (step[1]<len(grid[0]) and step[1]>=0) and (not grid[step[0]][step[1]] == '.'):
    grid = print_hallway_to_map(grid, step, direction)

  return grid

def search_for_room(grid, r, c):
  visited = {}
  stack = [(r, c)]
  while stack:
    spot = stack.pop(0)
    if grid[spot[0]][spot[1]] == '.':
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

    for direction in around:
      if direction in visited:
        continue
      try:
        _ = grid[direction[0]][direction[1]]
        visited[direction] = True
        stack.append(direction)
      except IndexError:
        pass

  return None

def scout(grid, spot, direction):
  print 'Scouting: {0}, {1}\r'.format(spot, direction),
  good_to_go = False
  try:
    # first detect edge of room
    while grid[spot[0]][spot[1]] == '.':
      if spot[0]<0 or spot[1]<0 or spot[0]>=len(grid) or spot[1]>=len(grid[0]):
        return False
      spot = (spot[0]+direction[0], spot[1]+direction[1])

    # then keep going, if new room detected return true, else false
    while not grid[spot[0]][spot[1]] == '.':
      if spot[0]<0 or spot[1]<0 or spot[0]>=len(grid) or spot[1]>=len(grid[0]):
        return False
      spot = (spot[0]+direction[0], spot[1]+direction[1])

    spot = (spot[0]+direction[0], spot[1]+direction[1])
    good_to_go = (grid[spot[0]][spot[1]] == '.')
  except IndexError:
    return False

  return good_to_go

def add_hallway(grid):
  unconnected = [[' ']*len(grid[0]) for _ in range(len(grid))]
  for r in range(len(grid)):
      for c in range(len(grid[0])):
        if grid[r][c] == '.':
          unconnected = erase_space(copy.deepcopy(grid), r, c)

  room_to_add = search_for_room(unconnected, random.randint(0, len(grid)-1), random.randint(0, len(grid)-1))

  if room_to_add is None:
    print 'FATAL ERROR: cannot connect all rooms in level'
    exit()

  for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    if scout(grid, room_to_add, direction):
      grid = print_hallway_to_map(grid, room_to_add, direction)

  return grid

def erase_space(grid, r, c):
    grid[r][c] = " "

    if r > 0 and grid[r-1][c] == ".":
        grid = erase_space(grid, r-1, c)
    if r < len(grid) - 1 and grid[r+1][c] == ".":
        grid = erase_space(grid, r+1, c)
    if c > 0 and grid[r][c-1] == ".":
        grid = erase_space(grid, r, c-1)
    if c < len(grid[0]) - 1 and grid[r][c+1] == ".":
        grid = erase_space(grid, r, c+1)

    return grid

def all_connected(grid):
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] == '.':
        erased = erase_space(copy.deepcopy(grid), r, c)
        return not any(t == '.' for row in erased for t in row)

def connect_rooms(grid):
  while not all_connected(grid):
    grid = add_hallway(grid)
  print 'Rooms connected! Proceeding...'
  return grid

def generate(size):
  grid = [[" "]*size for _ in range(size)]

  rooms_amt = 5
  room_min_size = 10
  room_max_size = 25
  rooms = [pygame.Rect(0, 0, random.randint(room_min_size, room_max_size), random.randint(room_min_size, room_max_size)) for _ in range(rooms_amt)]

  for room in rooms:
    grid = place_room(grid, room)

  grid = connect_rooms(grid)

  return grid