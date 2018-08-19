import random
import pygame

ROOM_BUFFER = 3

def draw_room(grid, room, r, c):
  print "Printing room to grid..."
  for row in range(room.height+ROOM_BUFFER):
    for col in range(room.width+ROOM_BUFFER):
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
  print "Placing room {0}".format(room)
  for r in range(len(grid)):
    for c in range(len(grid)):
      if spot_valid(grid, room, r, c):
        grid = draw_room(grid, room, r, c)
        return grid

  return grid

def generate(size):
  print "Generating grid..."
  grid = [[" "]*size for _ in range(size)]

  rooms_amt = 10
  room_min_size = 5
  room_max_size = 25
  rooms = [pygame.Rect(0, 0, random.randint(room_min_size, room_max_size), random.randint(room_min_size, room_max_size)) for _ in range(rooms_amt)]

  for room in rooms:
    grid = place_room(grid, room)

  return grid