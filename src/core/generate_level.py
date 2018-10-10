import random
import pygame
import copy
import random

ROOM_BUFFER = 3

def print_room_to_grid(grid, room, r, c):
  for row in range(-ROOM_BUFFER, room.height+ROOM_BUFFER):
    for col in range(-ROOM_BUFFER, room.width+ROOM_BUFFER):
      # 'B' does not corresond to a tile, provides buffer
      grid[r+row][c+col] = 'B'

  for row in range(room.height-1):
    for col in range(room.width-1):
      grid[r+row][c+col] = '.'

  return grid

'''
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
'''

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
  while grid[spot[0]][spot[1]] == '.':
    spot = (spot[0]+direction[0], spot[1]+direction[1])

  # then keep going, if new room detected return true, else false
  while not grid[spot[0]][spot[1]] == '.':
    grid[spot[0]][spot[1]] = '.'
    spot = (spot[0]+direction[0], spot[1]+direction[1])

  spot = (spot[0]+direction[0], spot[1]+direction[1])
  grid[spot[0]][spot[1]] = '.'

  return grid

def search_for_room(grid, r=None, c=None, target_tile='.', start=None):
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
    if grid[spot[0]][spot[1]] == target_tile:
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
  while spot and grid[spot[0]][spot[1]] == '.':
    spot = increment_spot(spot)

  while spot and not grid[spot[0]][spot[1]] == '.':
    spot = increment_spot(spot)

  if not spot:
      return False
  good_to_go = (grid[spot[0]][spot[1]] == '.')

  return good_to_go

def add_hallway(grid):
  r, c = search_for_room(grid, start='random')
  unconnected = erase_space(copy.deepcopy(grid), r, c)

  r, c = search_for_room(unconnected, start='random')
  queue = [(r, c)]
  "Starting search for hallway spot"

  checked = {}
  while queue:
    spot = queue.pop() # ok fine its a stack
    checked[spot] = True
    print "checking", spot, 'for hallway potential\r',

    for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
      if scout(grid, spot, direction):
        grid = print_hallway_to_map(grid, spot, direction)
        print 'hallway placed :thumbsup:'
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
    print 'erasing space at', r, c

    while queue:
      r, c = queue.pop()
      #print len(queue), r, c
      grid[r][c] = ' '

      neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
      neighbors = [x for x in neighbors if not x in visited]
      neighbors = [x for x in neighbors if x[0]>=0 and x[0]<len(grid) and x[1]>=0 and x[1]<len(grid[0])]
      neighbors = [x for x in neighbors if grid[x[0]][x[1]] == '.']
      for n in neighbors:
        visited[n] = True
        queue.append(n)

    return grid

def all_connected(grid):
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] == '.':
        erased = erase_space(copy.deepcopy(grid), r, c)
        return not any(t == '.' for row in erased for t in row)
