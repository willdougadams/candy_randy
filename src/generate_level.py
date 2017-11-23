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


def generate(size):
  grid = [list("x" * size) for i in range(size)]

  rooms = [Room(random.randint(0, size-1), random.randint(0, size-1)) for _ in range(5)]

  while any(room.can_expand for room in rooms):
    for room_i, room in enumerate(rooms):
      if room.can_expand:
        other_rooms = rooms[:]
        other_rooms.pop(room_i)
        room.expand(other_rooms)

  for room in rooms:
    # draw top and bottom
    top = max(0, room.rect.top)
    bottom = min(size-1, room.rect.bottom)
    left = max(0, room.rect.left)
    right = min(size-1, room.rect.right)

    grid[top][left] = "}"
    grid[bottom][left] = "{"
    grid[bottom][right] = "["
    grid[top][left] = "]"

    for tile in range(left+1, right-1):
      grid[top][tile] = "-"
      grid[bottom][tile] = "_"

    for row in range(top+1, bottom-1):
      grid[row][left] = ";"
      for tile in range(left+1, right-1):
        grid[row][tile] = "."
      grid[row][right] = ":"

    with open("bunk/map.txt", "w+") as fout:
      for row in grid:
        fout.write(", ".join(row))

  return grid
