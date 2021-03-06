import pygame

from pc import PC
from random import randint
from characters.character import Character

import math

target_location = (0, 0)

class NPC(Character):
  def __init__(self, coord, r, screen, npc_filename, level):
    Character.__init__(self, coord, r, screen, npc_filename, level)
    self.spritesheet_x = self.width * int(self.attrib_dict["spritesheet_position"][0])
    self.spritesheet_y = self.height * int(self.attrib_dict["spritesheet_position"][1])
    self.step = 0.0
    self.current_sprite_index = 0
    self.level = level
    self.path = []
    self.paths_original_length = len(self.path)

  def add_path(self, new_path):
    self.paths_original_length = len(new_path)
    if new_path:
      self.target_dest = new_path.pop(0)
    self.path = new_path

  def update(self, elapsed, damage_maps):
    if not self.alive:
      return
    Character.update(self, elapsed, damage_maps)

    if math.hypot(self.center[0]-self.target_dest[0], self.center[1]-self.target_dest[1]) < self.height/4:
      if len(self.path) > 0:
        self.target_dest = self.path.pop(0)


  def update_sprite(self, elapsed):
    self.step += elapsed
    if self.step > 0.3:
      self.current_sprite_index = (self.current_sprite_index + 1) % 2
      self.step = 0.0

    self.curr_sprite_sheet = self.sprite_sheets[self.current_sprite_index]


    self.image.blit(self.curr_sprite_sheet,
                    (0, 0),
                    (self.spritesheet_x, self.spritesheet_y, self.width, self.height)
                  )

  def apply_damage(self, elapsed, damage_maps):
    # npcs take damage with red and do damage with green
    for damage_type, surf in damage_maps.iteritems():
      try:
        damage_done = surf.get_at(tuple(map(int, self.get_int_location()))).r
        damage_done *= elapsed
        self.take_damage(damage_done)
      except IndexError as e:
        logging.warn('NPC off map, apparently. location: {0}'.format(self.center))
        logging.warn(str(e))

  def draw_damage_to_maps(self, damage_maps):
    if self.alive:
      for damage_type, surf in damage_maps.iteritems():
        spot = tuple(map(int, self.center))
        pygame.draw.circle(surf, (0, 10, 0), spot, self.width)

    return damage_maps