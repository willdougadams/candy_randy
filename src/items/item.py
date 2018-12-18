import pygame

from core.util import read_config, colors

class Item:
  def __init__(self, item_file, location):
    config = read_config(item_file)
    self.item_file = item_file
    self.durability = 100
    self.location = location #tuple(map(int, config['location']))
    self.uses = int(config['uses'])
    self.equip_slot = config['equip_slot']
    self.weight = int(config['weight'])
    self.value = int(config['value'])
    self.length = int(config['length'])
    self.width = self.height = 16
    self.attack_type = config['attack_type']
    self.image = pygame.Surface((self.width, self.height)).convert()
    self.image.set_colorkey(colors.BLACK)
    item_sheet = pygame.image.load("res/DawnLike/" + config['spritesheet']).convert()
    x, y = tuple(map(int, config['spritesheet_location']))
    self.image.blit(item_sheet, (0, 0), (x*self.width, y*self.height, self.width, self.height))

    self.damages = {}
    for k, v in config.iteritems():
      if k.startswith('damage_'):
        self.damages[k.replace('damage_', '')] = int(v)

  def draw(self, screen):
    x = self.location[0]
    y = self.location[1]
    screen.blit(self.image, (x - self.width/2, y - self.height/2), (0, 0, self.width, self.height))

  def use(self):
    if self.uses > 0:
      self.uses -= 1
    else:
      return False
