import random
import pygame

class Room():
  def __init__(self, x, y):
    self.rect = pygame.Rect((x, y), (1, 1))

    self.can_expand = True

  def __str__(self):
    return "rect: {0}".format(self.rect)

  def expand(self, other_rooms):
    expanded = self.rect.inflate(2, 2)

    if any(room.rect.colliderect(expanded) for room in other_rooms):
      self.can_expand = False
      return

    self.rect = expanded

def put_hori_wall(spot, grid):
  for i in range(len(grid[0])):
    grid[spot-1][i] = '-'
    grid[spot][i] = ' '
    grid[spot+1][i] = '_'

  return grid

def put_vert_wall(spot, grid):
  for i in range(len(grid)):
    grid[i][spot-1] = ':'
    grid[i][spot] = ' '
    grid[i][spot+1] = ';'

  return grid

def generate(size):
  print 'Generating Level...'
  grid = [['.'] * size for _ in range(size)]

  for i in range(size):
    grid[0][i] = '-'
    grid[size-1][i] = '_'
    grid[i][0] = ';'
    grid[i][size-1] = ':'

    horizontal_wall_count = 5
    vertical_wall_count = 10

  for wall in range(horizontal_wall_count):
    location = wall * (size/horizontal_wall_count)
    grid = put_hori_wall(location, grid)

  for wall in range(vertical_wall_count):
    location = wall * (size/vertical_wall_count)
    grid = put_vert_wall(location, grid)

  with open("bunk/map.txt", "w+") as fout:
      for row in grid:
        fout.write(''.join(row)+'\n')

  return grid

def generate2(size):
  grid = [['.'] * size for _ in range(size)]

  return grid