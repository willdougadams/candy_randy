import pygame
import logging

CONFIGS = {}

RUNTIME_LOG_LEVEL = logging.getLogger().getEffectiveLevel()

def read_config(filename):
  if filename in CONFIGS:
    return CONFIGS[filename]

  attribute_dict = {}
  with open(filename) as fin:
    lines = fin.readlines()

  for line in lines:
    if (not line.strip()) or line[0] == "#":
      continue

    attribute = line.split(":")[0].strip()
    value = line.split(":")[1].strip()
    attribute_dict[attribute] = (value if len(value.split()) == 1 else value.split())
    if len(attribute_dict[attribute]) == 1:
      attribute_dict[attribute] = attribute_dict[attribute][0]

  CONFIGS[filename] = attribute_dict
  return attribute_dict

class colors():
  BLACK = tuple(map(int, [0, 0, 0]))
  WHITE = tuple(map(int, [255, 255, 255]))
  BLUE  = tuple(map(int, [0, 0, 255]))
  GREEN = tuple(map(int, [0, 255, 0]))
  RED = tuple(map(int, [255, 0, 0]))
  PINK = tuple(map(int, [250, 5, 250]))

def trim_image(image):
  mask = image.get_colorkey()
  min_x = image.get_width()
  min_y = image.get_height()
  max_x = 0
  max_y = 0

  for y in range(image.get_height()):
    for x in range(image.get_width()):
      if not image.get_at((x, y)) == mask:
        if x < min_x:
          min_x = x
        elif x > max_x:
          max_x = x

        if y < min_y:
          min_y = y
        elif y > max_y:
          max_y = y

  height = max_y - min_y
  width = max_x - min_x

  cropped = pygame.Surface((width, height))
  cropped.blit(image, (0, 0), (min_x, min_y, max_x, max_y))

  return cropped
